import json
import hashlib
import time
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from datetime import datetime

from app.models import AIUsageLog, LessonCache
from app.config import settings

class AnalyticsAndCacheService:
    # Gemini 2.5 Flash pricing estimates (per million tokens)
    INPUT_COST_PER_M = 0.075
    OUTPUT_COST_PER_M = 0.30

    @classmethod
    def generate_cache_key(cls, object_name: str, language: str, knowledge_level: str, subject: Optional[str] = None) -> str:
        raw = f"{object_name.strip().lower()}:{language.strip().lower()}:{knowledge_level.strip().lower()}:{subject or 'all'}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @classmethod
    async def get_cached_lesson(cls, db: AsyncSession, cache_key: str) -> Optional[Dict[str, Any]]:
        stmt = select(LessonCache).where(LessonCache.cache_key == cache_key)
        res = await db.execute(stmt)
        record = res.scalars().first()
        if record:
            try:
                return json.loads(record.response_json)
            except Exception:
                return None
        return None

    @classmethod
    async def set_cached_lesson(cls, db: AsyncSession, cache_key: str, lesson_data: Dict[str, Any]):
        try:
            cache_entry = LessonCache(
                cache_key=cache_key,
                response_json=json.dumps(lesson_data, ensure_ascii=False)
            )
            db.add(cache_entry)
            await db.commit()
        except Exception:
            await db.rollback()

    @classmethod
    async def log_ai_usage(
        cls,
        db: AsyncSession,
        endpoint: str,
        model_name: str,
        prompt_chars_or_tokens: int,
        completion_chars_or_tokens: int,
        latency_ms: int,
        cache_hit: bool = False,
        user_id: Optional[int] = None
    ):
        # Approximate tokens if character count given: ~4 chars per token
        prompt_tokens = prompt_chars_or_tokens if prompt_chars_or_tokens < 10000 else int(prompt_chars_or_tokens / 4)
        completion_tokens = completion_chars_or_tokens if completion_chars_or_tokens < 10000 else int(completion_chars_or_tokens / 4)

        if cache_hit:
            cost = 0.0
        else:
            cost = (prompt_tokens * cls.INPUT_COST_PER_M / 1_000_000) + (completion_tokens * cls.OUTPUT_COST_PER_M / 1_000_000)

        log_entry = AIUsageLog(
            user_id=user_id,
            endpoint=endpoint,
            model_name=model_name or settings.GEMINI_MODEL,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            estimated_cost_usd=round(cost, 6),
            latency_ms=latency_ms,
            cache_hit=1 if cache_hit else 0
        )
        db.add(log_entry)
        try:
            await db.commit()
        except Exception:
            await db.rollback()

    @classmethod
    async def get_system_analytics(cls, db: AsyncSession, limit: int = 20) -> Dict[str, Any]:
        stmt = select(AIUsageLog).order_by(AIUsageLog.created_at.desc()).limit(limit)
        res = await db.execute(stmt)
        recent = res.scalars().all()

        total_stmt = select(
            func.count(AIUsageLog.id),
            func.sum(AIUsageLog.prompt_tokens),
            func.sum(AIUsageLog.completion_tokens),
            func.sum(AIUsageLog.estimated_cost_usd),
            func.sum(AIUsageLog.cache_hit),
            func.avg(AIUsageLog.latency_ms)
        )
        total_res = await db.execute(total_stmt)
        row = total_res.first()

        total_calls = row[0] or 0
        p_tokens = int(row[1] or 0)
        c_tokens = int(row[2] or 0)
        total_cost = float(row[3] or 0.0)
        cache_hits = int(row[4] or 0)
        avg_latency = float(row[5] or 0.0)

        hit_rate = round((cache_hits / total_calls * 100), 1) if total_calls > 0 else 0.0

        return {
            "total_api_calls": total_calls,
            "total_prompt_tokens": p_tokens,
            "total_completion_tokens": c_tokens,
            "total_tokens": p_tokens + c_tokens,
            "total_cost_usd": round(total_cost, 4),
            "cache_hits": cache_hits,
            "cache_hit_rate_pct": hit_rate,
            "avg_latency_ms": round(avg_latency, 1),
            "recent_logs": [
                {
                    "endpoint": r.endpoint,
                    "model_name": r.model_name,
                    "prompt_tokens": r.prompt_tokens,
                    "completion_tokens": r.completion_tokens,
                    "estimated_cost_usd": r.estimated_cost_usd,
                    "latency_ms": r.latency_ms,
                    "cache_hit": bool(r.cache_hit),
                    "created_at": r.created_at
                }
                for r in recent
            ]
        }

analytics_service = AnalyticsAndCacheService

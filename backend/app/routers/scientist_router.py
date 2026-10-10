import json
import time
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.dependencies import get_current_user_optional
from app.models import User, ScientistSession
from app.schemas import ScientistInquiryRequest, ScientistInquiryResponse, ExperimentPlanItem
from app.services.gemini_service import gemini_service
from app.services.analytics_service import analytics_service

router = APIRouter(prefix="/scientist", tags=["AI Scientist Mode"])

@router.post("/inquiry", response_model=ScientistInquiryResponse)
async def conduct_scientific_inquiry(
    req: ScientistInquiryRequest,
    user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    start_time = time.time()
    custom_key = user.custom_api_key if user else None

    # Call AI Scientist reasoning
    raw_result = await gemini_service.conduct_scientific_inquiry(
        object_name=req.object_name,
        domain=req.domain or "Physics",
        observation=req.observation,
        hypothesis=req.hypothesis,
        language=req.language or (user.preferred_language if user else "uz"),
        difficulty_level=req.difficulty_level or (user.knowledge_level if user else "intermediate"),
        custom_key=custom_key
    )
    latency_ms = int((time.time() - start_time) * 1000)

    # Log AI usage
    await analytics_service.log_ai_usage(
        db=db,
        endpoint="/scientist/inquiry",
        model_name="gemini-2.5-flash",
        prompt_chars_or_tokens=len(req.observation) + len(req.hypothesis) + 200,
        completion_chars_or_tokens=len(str(raw_result)),
        latency_ms=latency_ms,
        cache_hit=False,
        user_id=user.id if user else None
    )

    exp_plan_data = raw_result.get("experiment_plan", {})
    experiment_plan = ExperimentPlanItem(
        title=exp_plan_data.get("title", f"Safe Lab Inquiry: {req.object_name}"),
        materials=exp_plan_data.get("materials", ["Target object", "Notebook"]),
        steps=exp_plan_data.get("steps", ["1. Observe", "2. Test hypothesis"]),
        safety_guidelines=exp_plan_data.get("safety_guidelines", "Safe for household items."),
        expected_observation=exp_plan_data.get("expected_observation", "Observable physical effect.")
    )

    # Save Session record
    xp_earned = raw_result.get("xp_awarded", 50)
    session = ScientistSession(
        user_id=user.id if user else None,
        object_name=req.object_name,
        domain=req.domain or "Physics",
        observation=req.observation,
        hypothesis=req.hypothesis,
        experiment_plan_json=json.dumps(exp_plan_data, ensure_ascii=False),
        ai_evaluation_json=json.dumps(raw_result, ensure_ascii=False),
        xp_earned=xp_earned
    )
    db.add(session)

    # Award user XP (+50 XP)
    if user:
        user_obj = await db.get(User, user.id)
        if user_obj:
            user_obj.xp = (user_obj.xp or 0) + xp_earned
            db.add(user_obj)

    await db.commit()

    return ScientistInquiryResponse(
        object_name=req.object_name,
        domain=req.domain or "Physics",
        hypothesis_critique=raw_result.get("hypothesis_critique", ""),
        is_valid_hypothesis=raw_result.get("is_valid_hypothesis", True),
        experiment_plan=experiment_plan,
        scientific_principles=raw_result.get("scientific_principles", []),
        ai_guidance=raw_result.get("ai_guidance", "Davom eting!"),
        xp_awarded=xp_earned
    )

@router.get("/history")
async def get_scientist_history(
    user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    if not user:
        return []

    stmt = select(ScientistSession).where(ScientistSession.user_id == user.id).order_by(ScientistSession.created_at.desc()).limit(10)
    res = await db.execute(stmt)
    sessions = res.scalars().all()

    return [
        {
            "id": s.id,
            "object_name": s.object_name,
            "domain": s.domain,
            "observation": s.observation,
            "hypothesis": s.hypothesis,
            "xp_earned": s.xp_earned,
            "created_at": s.created_at
        }
        for s in sessions
    ]

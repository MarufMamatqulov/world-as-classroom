import json
import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from app.database import get_db
from app.dependencies import get_current_user_optional
from app.models import User, Exploration, Lesson, Quiz
from app.schemas import (
    GenerateLessonRequest, LessonDetail, SubjectModule, LessonExperiment,
    FunFact, VocabularyItem, DiscoveryStoryCardResponse
)
from app.services.gemini_service import gemini_service
from app.services.analytics_service import analytics_service

router = APIRouter(prefix="/lessons", tags=["Lessons"])

@router.post("/generate", response_model=LessonDetail)
async def generate_lesson(
    req: GenerateLessonRequest,
    user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    start_time = time.time()

    # Personalization params from user profile or request
    age = user.age if user and user.age else (req.age or 14)
    grade = user.grade if user and user.grade else (req.grade or "8")
    knowledge_level = req.difficulty_level or (user.knowledge_level if user and user.knowledge_level else (req.knowledge_level or "intermediate"))
    language = req.language or (user.preferred_language if user else "uz")
    custom_key = user.custom_api_key if user else None

    # Check Cache first (reduces latency and saves API cost)
    cache_key = analytics_service.generate_cache_key(
        object_name=req.object_name,
        language=language,
        knowledge_level=knowledge_level,
        subject=req.primary_focus_subject
    )
    cached_data = await analytics_service.get_cached_lesson(db, cache_key)
    
    if cached_data:
        raw_lesson = cached_data
        cache_hit = True
        latency_ms = int((time.time() - start_time) * 1000)
        await analytics_service.log_ai_usage(
            db=db,
            endpoint="/lessons/generate",
            model_name="cache",
            prompt_chars_or_tokens=0,
            completion_chars_or_tokens=len(str(raw_lesson)),
            latency_ms=latency_ms,
            cache_hit=True,
            user_id=user.id if user else None
        )
    else:
        cache_hit = False
        raw_lesson = await gemini_service.generate_lesson(
            object_name=req.object_name,
            object_name_en=req.object_name_en,
            language=language,
            age=age,
            grade=grade,
            knowledge_level=knowledge_level,
            custom_key=custom_key
        )
        latency_ms = int((time.time() - start_time) * 1000)
        
        # Save to cache
        await analytics_service.set_cached_lesson(db, cache_key, raw_lesson)
        
        # Log AI generation
        prompt_est_tokens = len(req.object_name) * 10 + 200
        comp_est_tokens = len(str(raw_lesson)) // 4
        await analytics_service.log_ai_usage(
            db=db,
            endpoint="/lessons/generate",
            model_name="gemini-2.5-flash",
            prompt_chars_or_tokens=prompt_est_tokens,
            completion_chars_or_tokens=comp_est_tokens,
            latency_ms=latency_ms,
            cache_hit=False,
            user_id=user.id if user else None
        )

    # 1. Save Exploration record
    primary_subject = req.primary_focus_subject or "Physics"
    if not req.primary_focus_subject and raw_lesson.get("modules") and len(raw_lesson["modules"]) > 0:
        primary_subject = raw_lesson["modules"][0].get("subject", "Physics")

    exploration = Exploration(
        user_id=user.id if user else None,
        object_name=req.object_name,
        object_name_en=req.object_name_en or raw_lesson.get("name_en", req.object_name),
        category=req.category or raw_lesson.get("category", "Science"),
        image_thumbnail=req.image_thumbnail,
        primary_subject=primary_subject,
        language=language
    )
    db.add(exploration)
    await db.flush()  # to obtain exploration.id

    # Award exploration XP (+30 XP) if user is logged in
    if user:
        user_obj = await db.get(User, user.id)
        if user_obj:
            user_obj.xp = (user_obj.xp or 0) + 30
            db.add(user_obj)

    # 2. Save Lesson record
    lesson = Lesson(
        exploration_id=exploration.id,
        title=raw_lesson.get("title", f"Scientific Exploration of {req.object_name}"),
        summary=raw_lesson.get("summary", ""),
        subjects_json=json.dumps(raw_lesson.get("modules", []), ensure_ascii=False),
        experiments_json=json.dumps(raw_lesson.get("experiments", []), ensure_ascii=False),
        fun_facts_json=json.dumps(raw_lesson.get("fun_facts", []), ensure_ascii=False),
        vocabulary_json=json.dumps(raw_lesson.get("vocabulary", []), ensure_ascii=False)
    )
    db.add(lesson)
    await db.flush()

    # 3. Save Quiz record
    raw_quiz = raw_lesson.get("quiz", [])
    quiz = Quiz(
        lesson_id=lesson.id,
        questions_json=json.dumps(raw_quiz, ensure_ascii=False)
    )
    db.add(quiz)
    await db.commit()
    await db.refresh(lesson)

    # Convert to response schema
    modules = [SubjectModule(**m) for m in raw_lesson.get("modules", [])]
    experiments = [LessonExperiment(**e) for e in raw_lesson.get("experiments", [])]
    fun_facts = [FunFact(**f) for f in raw_lesson.get("fun_facts", [])]
    vocabulary = [VocabularyItem(**v) for v in raw_lesson.get("vocabulary", [])]

    return LessonDetail(
        id=lesson.id,
        exploration_id=exploration.id,
        object_name=exploration.object_name,
        object_name_en=exploration.object_name_en,
        title=lesson.title,
        summary=lesson.summary,
        subjects=modules,
        experiments=experiments,
        fun_facts=fun_facts,
        vocabulary=vocabulary,
        language=language,
        created_at=lesson.created_at
    )

@router.get("/{lesson_id}", response_model=LessonDetail)
async def get_lesson(lesson_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Lesson, Exploration).join(Exploration, Lesson.exploration_id == Exploration.id).where(Lesson.id == lesson_id)
    result = await db.execute(stmt)
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    lesson, exploration = row

    modules_raw = json.loads(lesson.subjects_json or "[]")
    experiments_raw = json.loads(lesson.experiments_json or "[]")
    fun_facts_raw = json.loads(lesson.fun_facts_json or "[]")
    vocabulary_raw = json.loads(lesson.vocabulary_json or "[]")

    return LessonDetail(
        id=lesson.id,
        exploration_id=exploration.id,
        object_name=exploration.object_name,
        object_name_en=exploration.object_name_en,
        title=lesson.title,
        summary=lesson.summary,
        subjects=[SubjectModule(**m) for m in modules_raw],
        experiments=[LessonExperiment(**e) for e in experiments_raw],
        fun_facts=[FunFact(**f) for f in fun_facts_raw],
        vocabulary=[VocabularyItem(**v) for v in vocabulary_raw],
        language=exploration.language,
        created_at=lesson.created_at
    )

@router.get("/by-exploration/{exploration_id}", response_model=LessonDetail)
async def get_lesson_by_exploration(exploration_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Lesson, Exploration).join(Exploration, Lesson.exploration_id == Exploration.id).where(Exploration.id == exploration_id)
    result = await db.execute(stmt)
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Lesson not found for this exploration")
    
    lesson, exploration = row

    modules_raw = json.loads(lesson.subjects_json or "[]")
    experiments_raw = json.loads(lesson.experiments_json or "[]")
    fun_facts_raw = json.loads(lesson.fun_facts_json or "[]")
    vocabulary_raw = json.loads(lesson.vocabulary_json or "[]")

    return LessonDetail(
        id=lesson.id,
        exploration_id=exploration.id,
        object_name=exploration.object_name,
        object_name_en=exploration.object_name_en,
        title=lesson.title,
        summary=lesson.summary,
        subjects=[SubjectModule(**m) for m in modules_raw],
        experiments=[LessonExperiment(**e) for e in experiments_raw],
        fun_facts=[FunFact(**f) for f in fun_facts_raw],
        vocabulary=[VocabularyItem(**v) for v in vocabulary_raw],
        language=exploration.language,
        created_at=lesson.created_at
    )

@router.get("/{lesson_id}/story-card", response_model=DiscoveryStoryCardResponse)
async def get_discovery_story_card(
    lesson_id: int,
    user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """Generates a COPPA/GDPR safe, visually shareable discovery card without personal identifiable data."""
    stmt = select(Lesson, Exploration).join(Exploration, Lesson.exploration_id == Exploration.id).where(Lesson.id == lesson_id)
    result = await db.execute(stmt)
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Lesson not found")

    lesson, exploration = row
    modules_raw = json.loads(lesson.subjects_json or "[]")
    
    first_headline = "Real-World Scientific Discovery"
    first_formula = None
    if modules_raw and len(modules_raw) > 0:
        concepts = modules_raw[0].get("concepts", [])
        if concepts and len(concepts) > 0:
            first_headline = concepts[0].get("headline", first_headline)
            first_formula = concepts[0].get("formula")

    # Safe pseudonym/callsign
    callsign = f"Yosh Tadqiqotchi #{exploration.id:04d}"
    if user and user.full_name:
        parts = user.full_name.split()
        callsign = f"{parts[0]} (Tadqiqotchi)"

    return DiscoveryStoryCardResponse(
        exploration_id=exploration.id,
        object_name=exploration.object_name,
        object_name_en=exploration.object_name_en,
        category=exploration.category or "Science Discovery",
        primary_subject=exploration.primary_subject or "Physics",
        key_formula=first_formula,
        core_discovery=first_headline,
        explorer_callsign=callsign,
        xp_earned=80,
        discovery_date=exploration.created_at.strftime("%Y-%m-%d"),
        image_thumbnail=exploration.image_thumbnail,
        verified_badge="Haqiqiy Ilmiy Kashfiyot (Verified)",
        share_url=f"/lesson/{lesson.id}"
    )

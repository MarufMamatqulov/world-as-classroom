import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from app.database import get_db
from app.dependencies import get_current_user_optional
from app.models import User, Exploration, Lesson, Quiz
from app.schemas import GenerateLessonRequest, LessonDetail, SubjectModule, LessonExperiment, FunFact, VocabularyItem
from app.services.gemini_service import gemini_service

router = APIRouter(prefix="/lessons", tags=["Lessons"])

@router.post("/generate", response_model=LessonDetail)
async def generate_lesson(
    req: GenerateLessonRequest,
    user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    # Personalization params from user profile or request
    age = user.age if user and user.age else (req.age or 14)
    grade = user.grade if user and user.grade else (req.grade or "8")
    knowledge_level = user.knowledge_level if user and user.knowledge_level else (req.knowledge_level or "intermediate")
    language = req.language or (user.preferred_language if user else "uz")
    custom_key = user.custom_api_key if user else None

    # Call Gemini
    raw_lesson = await gemini_service.generate_lesson(
        object_name=req.object_name,
        object_name_en=req.object_name_en,
        language=language,
        age=age,
        grade=grade,
        knowledge_level=knowledge_level,
        custom_key=custom_key
    )

    # 1. Save Exploration record
    primary_subject = "Physics"
    if raw_lesson.get("modules") and len(raw_lesson["modules"]) > 0:
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

import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.database import get_db
from app.dependencies import get_current_user_optional
from app.models import User, Quiz, QuizAttempt, Lesson, Exploration
from app.schemas import QuizDetail, QuizQuestion, QuizSubmitRequest, QuizSubmitResponse, AnswerEvaluation

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

@router.get("/by-lesson/{lesson_id}", response_model=QuizDetail)
async def get_quiz_by_lesson(lesson_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Quiz).where(Quiz.lesson_id == lesson_id)
    result = await db.execute(stmt)
    quiz = result.scalars().first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found for this lesson")

    raw_questions = json.loads(quiz.questions_json or "[]")
    questions = []
    for q in raw_questions:
        questions.append(QuizQuestion(
            id=q.get("id", 1),
            question=q.get("question", ""),
            options=q.get("options", []),
            correct_index=q.get("correct_index", 0),
            explanation=q.get("explanation", ""),
            subject=q.get("subject", "Science")
        ))

    return QuizDetail(
        id=quiz.id,
        lesson_id=quiz.lesson_id,
        questions=questions
    )

@router.post("/submit", response_model=QuizSubmitResponse)
async def submit_quiz(
    req: QuizSubmitRequest,
    user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Quiz).where(Quiz.id == req.quiz_id)
    result = await db.execute(stmt)
    quiz = result.scalars().first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    questions = json.loads(quiz.questions_json or "[]")
    total_questions = len(questions)
    if total_questions == 0:
        raise HTTPException(status_code=400, detail="Quiz has no questions")

    score = 0
    evaluations: List[AnswerEvaluation] = []

    for idx, q in enumerate(questions):
        user_choice = req.answers[idx] if idx < len(req.answers) else -1
        correct_choice = q.get("correct_index", 0)
        is_correct = (user_choice == correct_choice)

        if is_correct:
            score += 1

        evaluations.append(AnswerEvaluation(
            question_id=q.get("id", idx + 1),
            question=q.get("question", ""),
            user_answer_index=user_choice,
            correct_answer_index=correct_choice,
            is_correct=is_correct,
            explanation=q.get("explanation", ""),
            subject=q.get("subject", "General Science")
        ))

    percentage = round((score / total_questions) * 100, 1)

    attempt = QuizAttempt(
        user_id=user.id if user else None,
        quiz_id=quiz.id,
        score=score,
        total_questions=total_questions,
        answers_json=json.dumps(req.answers)
    )
    db.add(attempt)

    # Award Quiz XP (25 XP per correct answer + 20 bonus for perfect score)
    earned_xp = score * 25 + (20 if score == total_questions else 0)
    if user:
        user_obj = await db.get(User, user.id)
        if user_obj:
            user_obj.xp = (user_obj.xp or 0) + earned_xp
            db.add(user_obj)

    await db.commit()
    await db.refresh(attempt)

    # Generate supportive pedagogical feedback
    if percentage >= 90:
        feedback = "Ajoyib natija! Siz ushbu mavzuni mukammal darajada o'zlashtirdingiz!"
    elif percentage >= 60:
        feedback = "Yaxshi natija! Xatolaringiz tahlilini ko'rib chiqing va bilimlaringizni yanada mustahkamlang."
    else:
        feedback = "Harakatdan to'xtamang! Dars materialini yana bir bor qayta o'qib chiqib, qayta urinib ko'ring."

    return QuizSubmitResponse(
        attempt_id=attempt.id,
        quiz_id=quiz.id,
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        evaluations=evaluations,
        feedback=feedback
    )

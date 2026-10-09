from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.database import get_db
from app.dependencies import get_current_user_optional
from app.models import User, Exploration, Lesson, Quiz, QuizAttempt, TutorMessage
from app.schemas import DashboardStats, ExplorationSummary, SubjectMastery, Achievement

router = APIRouter(prefix="/dashboard", tags=["Learning Dashboard"])

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    # Base filter by user or all guest explorations if no user
    if user:
        explorations_stmt = select(Exploration).where(
            (Exploration.user_id == user.id) | (Exploration.user_id == None)
        ).order_by(Exploration.created_at.desc())
    else:
        explorations_stmt = select(Exploration).order_by(Exploration.created_at.desc())

    expl_res = await db.execute(explorations_stmt)
    explorations = expl_res.scalars().all()

    total_explorations = len(explorations)

    # Quiz attempts
    if user:
        attempts_stmt = select(QuizAttempt).where(
            (QuizAttempt.user_id == user.id) | (QuizAttempt.user_id == None)
        )
    else:
        attempts_stmt = select(QuizAttempt)

    att_res = await db.execute(attempts_stmt)
    attempts = att_res.scalars().all()

    total_quizzes_completed = len(attempts)
    avg_score = 0.0
    if total_quizzes_completed > 0:
        total_pct = sum((a.score / a.total_questions * 100) for a in attempts if a.total_questions > 0)
        avg_score = round(total_pct / total_quizzes_completed, 1)

    # Subject mastery calculation
    subject_counts = {
        "Physics": 0,
        "Mathematics": 0,
        "Biology": 0,
        "Chemistry": 0,
        "Technology": 0,
        "History": 0
    }
    for e in explorations:
        subj = e.primary_subject or "Physics"
        if subj in subject_counts:
            subject_counts[subj] += 1
        else:
            subject_counts["Physics"] += 1

    subject_mastery: List[SubjectMastery] = [
        SubjectMastery(
            subject=subj,
            points=count * 50 + sum(a.score * 15 for a in attempts),
            lessons_count=count
        )
        for subj, count in subject_counts.items()
    ]

    # Recent explorations summaries
    recent: List[ExplorationSummary] = []
    for e in explorations[:10]:
        # check quiz for this exploration
        lesson_stmt = select(Lesson).where(Lesson.exploration_id == e.id)
        l_res = await db.execute(lesson_stmt)
        l_obj = l_res.scalars().first()

        quiz_completed = False
        best_score = None
        total_q = None

        if l_obj:
            q_stmt = select(Quiz).where(Quiz.lesson_id == l_obj.id)
            q_res = await db.execute(q_stmt)
            q_obj = q_res.scalars().first()
            if q_obj:
                att_q_stmt = select(QuizAttempt).where(QuizAttempt.quiz_id == q_obj.id)
                att_q_res = await db.execute(att_q_stmt)
                user_atts = att_q_res.scalars().all()
                if user_atts:
                    quiz_completed = True
                    best_score = max(a.score for a in user_atts)
                    total_q = user_atts[0].total_questions

        recent.append(ExplorationSummary(
            id=e.id,
            object_name=e.object_name,
            category=e.category,
            primary_subject=e.primary_subject or "Physics",
            language=e.language or "uz",
            image_thumbnail=e.image_thumbnail,
            created_at=e.created_at,
            quiz_completed=quiz_completed,
            best_score=best_score,
            total_questions=total_q
        ))

    # Calculate achievements
    has_perfect_quiz = any(a.score == a.total_questions and a.total_questions > 0 for a in attempts)
    
    achievements: List[Achievement] = [
        Achievement(
            id="first_discovery",
            title="Birinchi Qadam (First Discovery)",
            description="Kamera orqali birinchi ob'ektni o'rganishni boshladingiz",
            icon="Sparkles",
            unlocked=total_explorations >= 1,
            progress=min(total_explorations, 1),
            max_progress=1
        ),
        Achievement(
            id="curious_explorer",
            title="Qiziquvchan Sayohatchi (Curious Explorer)",
            description="Kamida 3 xil real ob'ektni tadqiq qildingiz",
            icon="Compass",
            unlocked=total_explorations >= 3,
            progress=min(total_explorations, 3),
            max_progress=3
        ),
        Achievement(
            id="quiz_master",
            title="Viktorina Ustasi (Quiz Master)",
            description="Viktorinada 100% natijaga erishdingiz",
            icon="Trophy",
            unlocked=has_perfect_quiz,
            progress=1 if has_perfect_quiz else 0,
            max_progress=1
        ),
        Achievement(
            id="polymath",
            title="Yosh Alloma (Young Polymath)",
            description="5 ta darsni muvaffaqiyatli yakunladingiz",
            icon="GraduationCap",
            unlocked=total_explorations >= 5,
            progress=min(total_explorations, 5),
            max_progress=5
        )
    ]

    streak = 1 if total_explorations > 0 else 0

    return DashboardStats(
        total_explorations=total_explorations,
        total_quizzes_completed=total_quizzes_completed,
        average_quiz_score=avg_score,
        current_streak_days=streak,
        subject_mastery=subject_mastery,
        recent_explorations=recent,
        achievements=achievements
    )

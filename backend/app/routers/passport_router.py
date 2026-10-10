from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.dependencies import get_current_user_optional
from app.models import User, Exploration, Lesson, Quiz, QuizAttempt
from app.schemas import KnowledgePassportResponse, RealmStamp, PassportLevelInfo, ExplorationSummary

router = APIRouter(prefix="/passport", tags=["Knowledge Passport"])

REALM_CONFIG = [
    {
        "id": "mechanics",
        "name": "Mexanika & Harakat",
        "domain": "Mechanics",
        "icon": "Cog",
        "color": "from-emerald-500 to-teal-600",
        "target_subjects": ["Physics", "Mechanics"]
    },
    {
        "id": "optics",
        "name": "Optika & Nur Olam",
        "domain": "Optics",
        "icon": "Eye",
        "color": "from-cyan-500 to-blue-600",
        "target_subjects": ["Physics", "Optics"]
    },
    {
        "id": "botany",
        "name": "Biologiya & Tabiat",
        "domain": "Botany",
        "icon": "Leaf",
        "color": "from-green-500 to-emerald-700",
        "target_subjects": ["Biology", "Botany"]
    },
    {
        "id": "chemistry",
        "name": "Kimyo & Moddalar",
        "domain": "Chemistry",
        "icon": "FlaskConical",
        "color": "from-amber-500 to-orange-600",
        "target_subjects": ["Chemistry"]
    },
    {
        "id": "technology",
        "name": "Muhandislik & Texnologiya",
        "domain": "Technology",
        "icon": "Cpu",
        "color": "from-purple-500 to-indigo-600",
        "target_subjects": ["Technology"]
    },
    {
        "id": "history",
        "name": "Kashfiyotlar Tarixi",
        "domain": "History",
        "icon": "Landmark",
        "color": "from-rose-500 to-pink-600",
        "target_subjects": ["History"]
    }
]

def _compute_level(xp: int) -> PassportLevelInfo:
    levels = [
        (1, "Qiziquvchan Sayohatchi (Curious Novice)", 0, 200),
        (2, "Dala Laboranti (Field Apprentice)", 200, 600),
        (3, "Fan Izquvari (Science Explorer)", 600, 1500),
        (4, "Katta Tadqiqotchi (Senior Investigator)", 1500, 3000),
        (5, "Bosh Alloma (Master Polymath)", 3000, 10000),
    ]

    for lvl, title, min_xp, max_xp in levels:
        if xp < max_xp or lvl == 5:
            range_xp = max_xp - min_xp
            curr_progress = max(0, xp - min_xp)
            pct = min(100.0, round((curr_progress / range_xp) * 100, 1)) if range_xp > 0 else 100.0
            return PassportLevelInfo(
                current_level=lvl,
                rank_title=title,
                current_xp=xp,
                next_level_xp=max_xp,
                progress_percentage=pct
            )

    return PassportLevelInfo(
        current_level=5,
        rank_title="Bosh Alloma (Master Polymath)",
        current_xp=xp,
        next_level_xp=10000,
        progress_percentage=100.0
    )

@router.get("/me", response_model=KnowledgePassportResponse)
async def get_my_passport(
    user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    if user:
        explorations_stmt = select(Exploration).where(
            (Exploration.user_id == user.id) | (Exploration.user_id == None)
        ).order_by(Exploration.created_at.desc())
        xp = user.xp or 0
        streak = user.streak_days or 1
        member_since = user.created_at.strftime("%Y-%m-%d")
        callsign = f"{user.full_name} (#{user.id:04d})"
    else:
        explorations_stmt = select(Exploration).order_by(Exploration.created_at.desc())
        xp = 120
        streak = 1
        member_since = "2026-10-09"
        callsign = "Mehmon Tadqiqotchi (Guest Explorer)"

    expl_res = await db.execute(explorations_stmt)
    explorations = expl_res.scalars().all()
    total_discoveries = len(explorations)

    # Subject counts for realm stamps
    subject_counts = {}
    for e in explorations:
        subj = e.primary_subject or "Physics"
        subject_counts[subj] = subject_counts.get(subj, 0) + 1

    stamps: List[RealmStamp] = []
    for realm in REALM_CONFIG:
        count = sum(subject_counts.get(s, 0) for s in realm["target_subjects"])
        unlocked = (count > 0)
        if count >= 5:
            mastery = "Master"
        elif count >= 2:
            mastery = "Adept"
        else:
            mastery = "Novice"

        stamps.append(RealmStamp(
            id=realm["id"],
            name=realm["name"],
            domain=realm["domain"],
            icon=realm["icon"],
            color=realm["color"],
            unlocked=unlocked,
            discoveries_count=count,
            mastery_level=mastery
        ))

    # Recent chronicles
    chronicle: List[ExplorationSummary] = []
    for e in explorations[:15]:
        chronicle.append(ExplorationSummary(
            id=e.id,
            object_name=e.object_name,
            category=e.category,
            primary_subject=e.primary_subject or "Physics",
            language=e.language or "uz",
            image_thumbnail=e.image_thumbnail,
            created_at=e.created_at
        ))

    level_info = _compute_level(xp)

    return KnowledgePassportResponse(
        explorer_callsign=callsign,
        member_since=member_since,
        level_info=level_info,
        total_discoveries=total_discoveries,
        streak_days=streak,
        stamps=stamps,
        recent_chronicle=chronicle
    )

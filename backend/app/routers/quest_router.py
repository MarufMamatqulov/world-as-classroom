import json
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.dependencies import get_current_user_optional
from app.models import User, Quest, UserQuestProgress, Exploration
from app.schemas import QuestResponse, QuestSubmitRequest, QuestSubmitResponse, UserBadgeResponse

router = APIRouter(prefix="/quests", tags=["Real World Quests"])

DEFAULT_QUESTS = [
    {
        "id": 1,
        "title": "Mexanika Siri: Aylanuvchi Harakat",
        "title_en": "Secret of Mechanics: Rotational Motion",
        "description": "Atrofdan aylanma yoki tishli mexanizmga ega bo'lgan ob'ektni toping (masalan: velosiped, soat, mikser yoki ventilator). Uning burchak tezligini va kuch uzatilishini o'rganing.",
        "description_en": "Find an object utilizing rotational or gear mechanisms (e.g. bicycle, clock, mixer). Explore torque and angular motion.",
        "domain": "Mechanics",
        "target_keyword": "bicycle",
        "xp_reward": 150,
        "badge_icon": "Cog",
        "badge_title": "Mexanika Ustasi (Gear Master)",
        "validation_question": "Tishli uzatmada (gear) oldingi tishli g'ildirak orqadagisidan 2 barobar katta bo'lsa, orqa g'ildirak qanday aylanadi?",
        "validation_options": [
            "2 marta tezroq aylanadi",
            "2 marta sekinroq aylanadi",
            "Aylanish tezligi o'zgarmaydi",
            "Harakat to'xtaydi"
        ],
        "correct_option_index": 0,
        "validation_explanation": "Katta g'ildirak 1 marta aylanganda, 2 barobar kichik orqa tishli g'ildirak 2 marta to'liq aylanadi (Gear ratio = 2:1)."
    },
    {
        "id": 2,
        "title": "Optika va Nur: Yorug'lik Sinishi",
        "title_en": "Optics & Light: Refraction and Lenses",
        "description": "Yorug'likni sindiruvchi, aks ettiruvchi yoki fokuslovchi buyumni toping (masalan: ko'zoynak, lupa, shisha prizma yoki ko'zgu).",
        "description_en": "Capture a transparent lens, magnifying glass, or optical surface that manipulates light rays.",
        "domain": "Optics",
        "target_keyword": "microscope",
        "xp_reward": 180,
        "badge_icon": "Eye",
        "badge_title": "Nur Kashfiyotchisi (Optic Pioneer)",
        "validation_question": "Yorug'lik nuri havodan shishaga yoki suvga o'tganda nima sodir bo'ladi?",
        "validation_options": [
            "Tezligi kamayadi va tarqalish yo'nalishi sinadi",
            "Tezligi ortadi va rangi o'zgaradi",
            "Yorug'lik butunlay yutilib yo'qoladi",
            "Hech qanday o'zgarish bo'lmaydi"
        ],
        "correct_option_index": 0,
        "validation_explanation": "Yorug'lik zichroq optik muhitga o'tganda (Snell qonuni), yorug'lik tezligi pasayadi va nur normal tomon sinadi."
    },
    {
        "id": 3,
        "title": "Fotosintez Sehri: Tirik Tabiat Nanofabrikasi",
        "title_en": "Magic of Photosynthesis: Nature's Nanofactory",
        "description": "Yashil o'simlik bargini toping va skanerlang. Quyosh energiyasi qanday qilib oziq moddalarga aylanayotganini tahlil qiling.",
        "description_en": "Discover a living plant leaf and inspect nature's solar power conversion.",
        "domain": "Botany",
        "target_keyword": "plant",
        "xp_reward": 140,
        "badge_icon": "Leaf",
        "badge_title": "Tabiat Bilimdoni (Bio Explorer)",
        "validation_question": "O'simlik bargiga yashil rang beruvchi va fotonlarni ushlab qoluvchi pigment qaysi?",
        "validation_options": [
            "Xlorofill (Chlorophyll)",
            "Gemoglobin",
            "Melanin",
            "Karotin"
        ],
        "correct_option_index": 0,
        "validation_explanation": "Xlorofill molekulasi qizil va ko'k yorug'lik to'lqinlarini yutadi va yashil yorug'likni qaytaradi."
    },
    {
        "id": 4,
        "title": "Tebranishlar va Vaqt: Pyezoelektr Kvars",
        "title_en": "Oscillations & Time: Piezoelectric Quartz",
        "description": "Kvars soat yoki tebranma harakat qiluvchi qurilmani toping. Bir maromdagi tebranishlar qanday qilib vaqtni aniq o'lchashini tekshiring.",
        "description_en": "Explore an electronic clock or mechanical pendulum demonstrating stable periodic oscillations.",
        "domain": "Thermodynamics",
        "target_keyword": "clock",
        "xp_reward": 160,
        "badge_icon": "Clock",
        "badge_title": "Vaqt Sayohatchisi (Chronos Master)",
        "validation_question": "Kvars soatlaridagi kichik kvars kristalli bir sekundda necha marta tebranadi?",
        "validation_options": [
            "32,768 marta (Hz)",
            "60 marta",
            "1,000 marta",
            "1 marta"
        ],
        "correct_option_index": 0,
        "validation_explanation": "32,768 soni 2 ning 15-darajasi (2^15) bo'lib, ikkilik raqamli bo'lgichlar orqali aniq 1 soniyaga bo'linadi."
    }
]

async def _ensure_seed_quests(db: AsyncSession):
    stmt = select(Quest)
    res = await db.execute(stmt)
    existing = res.scalars().all()
    if len(existing) == 0:
        for q in DEFAULT_QUESTS:
            new_q = Quest(
                id=q["id"],
                title=q["title"],
                title_en=q["title_en"],
                description=q["description"],
                description_en=q["description_en"],
                domain=q["domain"],
                target_keyword=q["target_keyword"],
                xp_reward=q["xp_reward"],
                badge_icon=q["badge_icon"],
                badge_title=q["badge_title"],
                validation_question=q["validation_question"],
                validation_options_json=json.dumps(q["validation_options"], ensure_ascii=False),
                correct_option_index=q["correct_option_index"],
                validation_explanation=q["validation_explanation"],
                is_daily=1
            )
            db.add(new_q)
        await db.commit()

@router.get("/daily", response_model=List[QuestResponse])
async def get_daily_quests(
    user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    await _ensure_seed_quests(db)

    stmt = select(Quest).order_by(Quest.id.asc())
    res = await db.execute(stmt)
    quests = res.scalars().all()

    # Get user completed quest IDs if authenticated
    completed_map = {}
    if user:
        p_stmt = select(UserQuestProgress).where(UserQuestProgress.user_id == user.id)
        p_res = await db.execute(p_stmt)
        for p in p_res.scalars().all():
            completed_map[p.quest_id] = p

    response = []
    for q in quests:
        prog = completed_map.get(q.id)
        options = json.loads(q.validation_options_json or "[]")
        status = prog.status if prog else "active"
        completed_at = prog.completed_at if prog else None

        response.append(QuestResponse(
            id=q.id,
            title=q.title,
            title_en=q.title_en,
            description=q.description,
            domain=q.domain,
            target_keyword=q.target_keyword,
            xp_reward=q.xp_reward,
            badge_icon=q.badge_icon,
            badge_title=q.badge_title,
            validation_question=q.validation_question,
            validation_options=options,
            is_daily=bool(q.is_daily),
            status=status,
            completed_at=completed_at
        ))

    return response

@router.post("/submit", response_model=QuestSubmitResponse)
async def submit_quest(
    req: QuestSubmitRequest,
    user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    quest = await db.get(Quest, req.quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")

    is_correct = (req.selected_option_index == quest.correct_option_index)

    if not is_correct:
        return QuestSubmitResponse(
            quest_id=quest.id,
            success=False,
            message="Javobingiz noaniq bo'ldi. Darsdagi fizik qonuniyatlarni yana bir bor ko'rib chiqing va qayta urinib ko'ring!",
            xp_awarded=0,
            badge_awarded=None,
            explanation=quest.validation_explanation
        )

    # Award Quest
    xp_awarded = quest.xp_reward
    if user:
        # Check if already completed
        p_stmt = select(UserQuestProgress).where(
            (UserQuestProgress.user_id == user.id) & (UserQuestProgress.quest_id == quest.id)
        )
        p_res = await db.execute(p_stmt)
        existing_prog = p_res.scalars().first()

        if existing_prog and existing_prog.status == "completed":
            return QuestSubmitResponse(
                quest_id=quest.id,
                success=True,
                message="Ushbu missiyani avval muvaffaqiyatli bajargansiz!",
                xp_awarded=0,
                badge_awarded=quest.badge_title,
                explanation=quest.validation_explanation
            )

        if not existing_prog:
            prog = UserQuestProgress(
                user_id=user.id,
                quest_id=quest.id,
                exploration_id=req.exploration_id,
                status="completed",
                earned_xp=xp_awarded,
                completed_at=datetime.utcnow()
            )
            db.add(prog)
        else:
            existing_prog.status = "completed"
            existing_prog.earned_xp = xp_awarded
            existing_prog.completed_at = datetime.utcnow()
            db.add(existing_prog)

        user_obj = await db.get(User, user.id)
        if user_obj:
            user_obj.xp = (user_obj.xp or 0) + xp_awarded
            db.add(user_obj)

        await db.commit()

    return QuestSubmitResponse(
        quest_id=quest.id,
        success=True,
        message=f"Tabriklaymiz! Ilmiy missiya tasdiqlandi. Sizga +{xp_awarded} XP va '{quest.badge_title}' nishoni berildi!",
        xp_awarded=xp_awarded,
        badge_awarded=quest.badge_title,
        explanation=quest.validation_explanation
    )

@router.get("/badges", response_model=List[UserBadgeResponse])
async def get_user_badges(
    user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    await _ensure_seed_quests(db)

    badges = []
    if user:
        stmt = select(UserQuestProgress, Quest).join(Quest, UserQuestProgress.quest_id == Quest.id).where(
            (UserQuestProgress.user_id == user.id) & (UserQuestProgress.status == "completed")
        )
        res = await db.execute(stmt)
        for prog, q in res.all():
            badges.append(UserBadgeResponse(
                id=f"badge_{q.id}",
                title=q.badge_title,
                icon=q.badge_icon,
                domain=q.domain,
                unlocked_at=prog.completed_at or prog.created_at,
                xp=q.xp_reward
            ))
    
    # If no user or empty, return at least sample unlocked or demo badge
    if len(badges) == 0:
        badges.append(UserBadgeResponse(
            id="badge_starter",
            title="Kashfiyotchi Dastlabki Qadami (Explorer Initiate)",
            icon="Compass",
            domain="General Science",
            unlocked_at=datetime.utcnow(),
            xp=50
        ))

    return badges

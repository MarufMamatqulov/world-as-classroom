from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.database import get_db
from app.dependencies import get_current_user_optional
from app.models import User, Exploration, Lesson, TutorMessage
from app.schemas import TutorChatRequest, TutorChatResponse, TutorMessageSchema
from app.services.gemini_service import gemini_service

router = APIRouter(prefix="/tutor", tags=["Interactive AI Tutor"])

@router.post("/chat", response_model=TutorChatResponse)
async def chat_with_tutor(
    req: TutorChatRequest,
    user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    # Retrieve Exploration & Lesson context
    stmt = select(Exploration).where(Exploration.id == req.exploration_id)
    result = await db.execute(stmt)
    exploration = result.scalars().first()
    if not exploration:
        raise HTTPException(status_code=404, detail="Exploration not found")

    lesson_stmt = select(Lesson).where(Lesson.exploration_id == exploration.id)
    lesson_res = await db.execute(lesson_stmt)
    lesson = lesson_res.scalars().first()
    lesson_summary = lesson.summary if lesson else ""

    # Fetch last 8 messages
    history_stmt = select(TutorMessage).where(
        TutorMessage.exploration_id == exploration.id
    ).order_by(TutorMessage.created_at.asc())
    history_res = await db.execute(history_stmt)
    all_msgs = history_res.scalars().all()

    chat_history = [{"role": m.role, "content": m.content} for m in all_msgs[-8:]]

    # Save user message
    user_msg_db = TutorMessage(
        exploration_id=exploration.id,
        user_id=user.id if user else None,
        role="user",
        content=req.message
    )
    db.add(user_msg_db)
    await db.commit()

    # Call AI Tutor
    custom_key = user.custom_api_key if user else None
    ai_response = await gemini_service.tutor_chat(
        object_name=exploration.object_name,
        lesson_summary=lesson_summary,
        chat_history=chat_history,
        user_message=req.message,
        language=req.language or exploration.language or "uz",
        custom_key=custom_key
    )

    reply_text = ai_response.get("reply", "Ajoyib savol!")
    suggested_prompts = ai_response.get("suggested_prompts", [])

    # Save assistant message
    bot_msg_db = TutorMessage(
        exploration_id=exploration.id,
        user_id=user.id if user else None,
        role="assistant",
        content=reply_text
    )
    db.add(bot_msg_db)
    await db.commit()

    return TutorChatResponse(
        reply=reply_text,
        suggested_prompts=suggested_prompts
    )

@router.get("/history/{exploration_id}", response_model=List[TutorMessageSchema])
async def get_chat_history(exploration_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(TutorMessage).where(
        TutorMessage.exploration_id == exploration_id
    ).order_by(TutorMessage.created_at.asc())
    result = await db.execute(stmt)
    messages = result.scalars().all()

    return [
        TutorMessageSchema(
            id=m.id,
            role=m.role,
            content=m.content,
            created_at=m.created_at
        )
        for m in messages
    ]

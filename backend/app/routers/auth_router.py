from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import User
from app.schemas import UserRegister, UserLogin, UserProfileUpdate, UserResponse, TokenResponse
from app.auth import hash_password, verify_password, create_access_token
from app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
async def register(req: UserRegister, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    stmt = select(User).where(User.email == req.email.lower())
    result = await db.execute(stmt)
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    user = User(
        email=req.email.lower(),
        hashed_password=hash_password(req.password),
        full_name=req.full_name,
        age=req.age or 14,
        grade=req.grade or "8",
        knowledge_level=req.knowledge_level or "intermediate",
        preferred_language=req.preferred_language or "uz",
        custom_api_key=None
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token({"sub": str(user.id), "email": user.email})
    user_res = UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        age=user.age,
        grade=user.grade,
        knowledge_level=user.knowledge_level,
        preferred_language=user.preferred_language,
        has_custom_api_key=bool(user.custom_api_key),
        created_at=user.created_at
    )
    return TokenResponse(access_token=token, user=user_res)

@router.post("/login", response_model=TokenResponse)
async def login(req: UserLogin, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == req.email.lower())
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    token = create_access_token({"sub": str(user.id), "email": user.email})
    user_res = UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        age=user.age,
        grade=user.grade,
        knowledge_level=user.knowledge_level,
        preferred_language=user.preferred_language,
        has_custom_api_key=bool(user.custom_api_key),
        created_at=user.created_at
    )
    return TokenResponse(access_token=token, user=user_res)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        age=current_user.age,
        grade=current_user.grade,
        knowledge_level=current_user.knowledge_level,
        preferred_language=current_user.preferred_language,
        has_custom_api_key=bool(current_user.custom_api_key),
        created_at=current_user.created_at
    )

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    req: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if req.full_name is not None:
        current_user.full_name = req.full_name
    if req.age is not None:
        current_user.age = req.age
    if req.grade is not None:
        current_user.grade = req.grade
    if req.knowledge_level is not None:
        current_user.knowledge_level = req.knowledge_level
    if req.preferred_language is not None:
        current_user.preferred_language = req.preferred_language
    if req.custom_api_key is not None:
        current_user.custom_api_key = req.custom_api_key.strip() if req.custom_api_key.strip() else None

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        age=current_user.age,
        grade=current_user.grade,
        knowledge_level=current_user.knowledge_level,
        preferred_language=current_user.preferred_language,
        has_custom_api_key=bool(current_user.custom_api_key),
        created_at=current_user.created_at
    )

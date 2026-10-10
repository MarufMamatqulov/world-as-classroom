from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user_optional
from app.models import User
from app.schemas import SystemCostAnalytics, AnalyticsOverview
from app.services.analytics_service import analytics_service
from app.routers.dashboard_router import get_dashboard_stats
from app.routers.passport_router import get_my_passport

router = APIRouter(prefix="/analytics", tags=["Learning Analytics & Cost Monitoring"])

@router.get("/system", response_model=SystemCostAnalytics)
async def get_system_cost_analytics(
    user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """Returns AI API call metrics, token consumption, estimated USD expenses, and caching efficiency."""
    data = await analytics_service.get_system_analytics(db, limit=25)
    return SystemCostAnalytics(**data)

@router.get("/overview", response_model=AnalyticsOverview)
async def get_full_analytics_overview(
    user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """Aggregates student learning progress, passport stamps, and AI resource monitoring."""
    stats = await get_dashboard_stats(user, db)
    passport = await get_my_passport(user, db)
    system_data = await analytics_service.get_system_analytics(db, limit=10)

    return AnalyticsOverview(
        student_stats=stats,
        passport=passport,
        system_monitoring=SystemCostAnalytics(**system_data)
    )

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import init_db, db_url
from app.routers import (
    auth_router,
    scan_router,
    lesson_router,
    quiz_router,
    tutor_router,
    dashboard_router
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database tables...")
    await init_db()
    logger.info("Database initialized successfully.")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="World as a Classroom — Turn any real-world object into an interactive educational experience using AI.",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_router.router, prefix=settings.API_PREFIX)
app.include_router(scan_router.router, prefix=settings.API_PREFIX)
app.include_router(lesson_router.router, prefix=settings.API_PREFIX)
app.include_router(quiz_router.router, prefix=settings.API_PREFIX)
app.include_router(tutor_router.router, prefix=settings.API_PREFIX)
app.include_router(dashboard_router.router, prefix=settings.API_PREFIX)

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": "postgresql" if "postgresql" in db_url else "sqlite",
        "gemini_configured": bool(settings.GEMINI_API_KEY)
    }

@app.get("/")
async def root():
    return {
        "message": "Welcome to World as a Classroom API. Explore the world through AI-powered interactive education!",
        "docs": "/docs"
    }

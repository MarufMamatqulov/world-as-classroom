import time
import logging
from collections import defaultdict
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db, db_url
from app.routers import (
    auth_router,
    scan_router,
    lesson_router,
    quiz_router,
    tutor_router,
    dashboard_router,
    quest_router,
    scientist_router,
    passport_router,
    analytics_router
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sliding-window IP Rate Limiter
_rate_limits = defaultdict(list)
RATE_LIMIT_WINDOW = 60  # seconds
MAX_REQUESTS_PER_MINUTE = 30  # max 30 requests per minute per IP

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

# CORS Middleware restricted to wordbox.uz domains and development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"^https?://(.*\.)?wordbox\.uz(:\d+)?$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

@app.middleware("http")
async def security_and_rate_limit_middleware(request: Request, call_next):
    # Allow CORS preflight requests
    if request.method == "OPTIONS":
        return await call_next(request)

    path = request.url.path
    client_ip = request.client.host if request.client else "unknown"

    # Public health check and documentation endpoints
    if path in ["/", "/docs", "/openapi.json", "/api/health"]:
        return await call_next(request)

    # 1. IP Rate Limiting (Protects OpenAI quota from brute-force scripts)
    now = time.time()
    recent = [t for t in _rate_limits[client_ip] if now - t < RATE_LIMIT_WINDOW]
    if len(recent) >= MAX_REQUESTS_PER_MINUTE:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Limit is 30 requests per minute per IP."}
        )
    recent.append(now)
    _rate_limits[client_ip] = recent

    # 2. Strict Access Control for Protected Education & AI APIs (/api/...)
    if path.startswith("/api"):
        is_internal_vps = client_ip in ["127.0.0.1", "localhost", "::1"]
        client_key = (
            request.headers.get("x-wordbox-key") or
            request.headers.get("x-api-key") or
            ""
        ).strip()
        origin = request.headers.get("origin", "").lower()
        referer = request.headers.get("referer", "").lower()

        is_wordbox_origin = (
            "wordbox.uz" in origin or
            "wordbox.uz" in referer or
            "localhost" in origin or
            "127.0.0.1" in origin
        )
        is_valid_secret = bool(settings.WORDBOX_API_SECRET and client_key == settings.WORDBOX_API_SECRET)

        # Allow only if:
        # a) Internal VPS call (localhost)
        # b) Valid X-Wordbox-Key header is passed
        # c) Request originated directly from wordbox.uz
        if not (is_internal_vps or is_valid_secret or is_wordbox_origin):
            logger.warning(f"Blocked unauthorized external script access: IP={client_ip}, path={path}, Origin={origin}")
            return JSONResponse(
                status_code=403,
                content={
                    "detail": "Access forbidden: Unauthorized client. Only wordbox.uz and authorized clients with X-Wordbox-Key can access this API."
                }
            )

    return await call_next(request)

# Register API Routers
app.include_router(auth_router.router, prefix=settings.API_PREFIX)
app.include_router(scan_router.router, prefix=settings.API_PREFIX)
app.include_router(lesson_router.router, prefix=settings.API_PREFIX)
app.include_router(quiz_router.router, prefix=settings.API_PREFIX)
app.include_router(tutor_router.router, prefix=settings.API_PREFIX)
app.include_router(dashboard_router.router, prefix=settings.API_PREFIX)
app.include_router(quest_router.router, prefix=settings.API_PREFIX)
app.include_router(scientist_router.router, prefix=settings.API_PREFIX)
app.include_router(passport_router.router, prefix=settings.API_PREFIX)
app.include_router(analytics_router.router, prefix=settings.API_PREFIX)

@app.get("/api/health")
async def health_check():
    db_url = settings.DATABASE_URL
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": "postgresql" if "postgresql" in db_url else "sqlite",
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "openai_configured": bool(settings.OPENAI_API_KEY)
    }

@app.get("/")
async def root():
    return {
        "message": "Welcome to World as a Classroom API. Explore the world through AI-powered interactive education!",
        "docs": "/docs"
    }

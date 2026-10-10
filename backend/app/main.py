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
MAX_REQUESTS_PER_MINUTE = 60  # max 60 requests per minute per real user IP

def get_real_client_ip(request: Request) -> str:
    """
    Extracts the true client IP address, handling reverse proxies (Vercel, Cloudflare, Nginx).
    The leftmost IP in X-Forwarded-For is the original client.
    """
    xff = request.headers.get("x-forwarded-for")
    if xff:
        parts = [p.strip() for p in xff.split(",") if p.strip()]
        if parts:
            return parts[0]
    x_real_ip = request.headers.get("x-real-ip")
    if x_real_ip and x_real_ip.strip():
        return x_real_ip.strip()
    if request.client and request.client.host:
        return request.client.host
    return "127.0.0.1"

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

# CORS Middleware restricted to wordbox.uz and aimarafon.uz domains and development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"^https?://(.*\.)?(wordbox\.uz|aimarafon\.uz)(:\d+)?$",
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

    # Public health check and documentation endpoints
    if path in ["/", "/docs", "/openapi.json", "/api/health"]:
        return await call_next(request)

    # Extract real client IP through reverse proxies (Vercel / Nginx)
    real_ip = get_real_client_ip(request)

    # Check if this is a direct internal call (localhost without proxy headers e.g. local pytest)
    is_internal_vps_direct = (
        request.client and
        request.client.host in ["127.0.0.1", "localhost", "::1"] and
        not request.headers.get("x-forwarded-for") and
        not request.headers.get("x-real-ip")
    )

    # 1. STRICT ACCESS CONTROL FOR PROTECTED APIS (/api/...)
    # Origin header alone is NO LONGER allowed to bypass the key!
    # All external requests MUST supply a valid X-Wordbox-Key.
    if path.startswith("/api"):
        client_key = (
            request.headers.get("x-wordbox-key") or
            request.headers.get("x-api-key") or
            ""
        ).strip()
        is_valid_secret = bool(settings.WORDBOX_API_SECRET and client_key == settings.WORDBOX_API_SECRET)

        if not (is_internal_vps_direct or is_valid_secret):
            logger.warning(f"Rejected unauthorized API request: IP={real_ip}, path={path}, has_key={bool(client_key)}")
            return JSONResponse(
                status_code=403,
                content={
                    "detail": "Access forbidden: Invalid or missing X-Wordbox-Key. Origin header alone is not authorized."
                }
            )

    # 2. IP RATE LIMITING (Per real end-user IP from X-Forwarded-For)
    now = time.time()
    recent = [t for t in _rate_limits[real_ip] if now - t < RATE_LIMIT_WINDOW]
    if len(recent) >= MAX_REQUESTS_PER_MINUTE:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Limit is 60 requests per minute per user."}
        )
    recent.append(now)
    _rate_limits[real_ip] = recent

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

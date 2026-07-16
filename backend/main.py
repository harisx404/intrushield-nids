from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio

from backend.core.config import settings
from backend.api.v1.api import api_router
from backend.core.exceptions import BaseNIDSError
from backend.middleware.rate_limiter import RateLimiterMiddleware
from backend.middleware.request_logger import RequestLoggerMiddleware
from backend.middleware.error_handler import global_exception_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background tasks
    print("Starting background tasks...")
    yield
    # Shutdown background tasks
    print("Shutting down...")

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="CodeAlpha Network Intrusion Detection System API",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

origins = settings.CORS_ORIGINS.split(",") if hasattr(settings, "CORS_ORIGINS") else ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimiterMiddleware)
app.add_middleware(RequestLoggerMiddleware)

@app.exception_handler(BaseNIDSError)
async def custom_exception_handler(request: Request, exc: BaseNIDSError):
    return JSONResponse(status_code=exc.status_code, content={"error": "Error", "detail": exc.message})

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return await global_exception_handler(request, exc)

app.include_router(api_router, prefix="/api/v1")

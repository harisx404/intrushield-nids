from fastapi import Request
from fastapi.responses import JSONResponse
import structlog

logger = structlog.get_logger("error_handler")

async def global_exception_handler(request: Request, exc: Exception):
    """Global exception boundary to catch unhandled errors and format them securely."""
    logger.error(
        "unhandled_exception",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        error_type=exc.__class__.__name__
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please contact support."
        }
    )

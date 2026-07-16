import time
from typing import Dict, Tuple
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# Simple in-memory rate limiter: IP -> (request_count, window_start_time)
_RATE_LIMIT_CACHE: Dict[str, Tuple[int, float]] = {}
RATE_LIMIT_WINDOW = 60.0  # 1 minute
MAX_REQUESTS_PER_WINDOW = 100

class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        
        # Skip rate limiting for local tests/healthchecks
        if request.url.path == "/api/v1/health":
            return await call_next(request)

        now = time.time()
        count, start_time = _RATE_LIMIT_CACHE.get(client_ip, (0, now))

        # If window expired, reset
        if now - start_time > RATE_LIMIT_WINDOW:
            count = 0
            start_time = now

        count += 1
        _RATE_LIMIT_CACHE[client_ip] = (count, start_time)

        if count > MAX_REQUESTS_PER_WINDOW:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too Many Requests",
                    "message": "Rate limit exceeded. Please try again later.",
                    "retry_after": int(RATE_LIMIT_WINDOW - (now - start_time))
                }
            )

        response = await call_next(request)
        return response

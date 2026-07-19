import time

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger("api")


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        client_ip = request.client.host if request.client else "unknown"

        logger.info(
            "http_request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            client_ip=client_ip,
            duration_ms=round(process_time, 2),
        )

        return response

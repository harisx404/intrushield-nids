"""Log response handler — writes alert details to response log file."""

import json
from datetime import UTC, datetime
from pathlib import Path

import aiofiles
import structlog
from backend.core.config import settings
from backend.response.base_handler import BaseResponseHandler, ResponseResult
from backend.schemas.alert import AlertResponse

log = structlog.get_logger(__name__)
LOG_DIR = Path("logs/responses")


class LogHandler(BaseResponseHandler):
    """Writes every alert to a dated response log file in JSON format."""

    @property
    def name(self) -> str:
        return "LogHandler"

    def should_handle(self, alert: AlertResponse) -> bool:
        return settings.ENABLE_LOG_RESPONSE

    async def handle(self, alert: AlertResponse) -> ResponseResult:
        """Append alert to today's response log file."""
        try:
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            date_str = datetime.now(UTC).strftime("%Y-%m-%d")
            log_file = LOG_DIR / f"response_{date_str}.log"

            entry = {
                "timestamp": datetime.now(UTC).isoformat(),
                "alert_id": alert.id,
                "severity": alert.severity,
                "signature": alert.signature,
                "src_ip": alert.src_ip,
                "dst_ip": alert.dst_ip,
            }

            async with aiofiles.open(log_file, "a", encoding="utf-8") as f:
                await f.write(json.dumps(entry) + "\n")

            return ResponseResult(
                handler_name=self.name,
                action="logged_to_file",
                status="SUCCESS",
                details={"file": str(log_file)},
            )
        except Exception as exc:
            log.error("log_handler_failed", error=str(exc))
            return ResponseResult(
                handler_name=self.name,
                action="logged_to_file",
                status="FAILED",
                details={"error": str(exc)},
            )

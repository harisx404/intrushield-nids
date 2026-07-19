"""Email response handler — notifies operators of critical alerts."""

import logging

from backend.core.config import settings
from backend.response.base_handler import BaseResponseHandler, ResponseResult
from backend.schemas.alert import AlertResponse

logger = logging.getLogger(__name__)


class EmailHandler(BaseResponseHandler):
    @property
    def name(self) -> str:
        return "EmailHandler"

    def should_handle(self, alert: AlertResponse) -> bool:
        return alert.severity == "CRITICAL" and bool(settings.SMTP_HOST)

    async def handle(self, alert: AlertResponse) -> ResponseResult:
        # Delivery is stubbed until SMTP credentials are wired up; log the intent
        # so the action is still auditable.
        logger.info(
            "Simulating email notification for CRITICAL alert: %s", alert.signature
        )
        return ResponseResult(
            handler_name=self.name,
            action="email_notification",
            status="SUCCESS",
            details={"signature": alert.signature, "severity": alert.severity},
        )

"""Webhook response handler — posts high-severity alerts to a chat webhook."""
import logging

import httpx

from backend.core.config import settings
from backend.response.base_handler import BaseResponseHandler, ResponseResult
from backend.schemas.alert import AlertResponse

logger = logging.getLogger(__name__)

_PLACEHOLDER_URL = "https://hooks.slack.com/services/DUMMY/WEBHOOK/URL"


class WebhookHandler(BaseResponseHandler):
    @property
    def name(self) -> str:
        return "WebhookHandler"

    def __init__(self) -> None:
        self.webhook_url = settings.WEBHOOK_URL

    def should_handle(self, alert: AlertResponse) -> bool:
        return (
            alert.severity in ("HIGH", "CRITICAL")
            and bool(self.webhook_url)
            and self.webhook_url != _PLACEHOLDER_URL
        )

    async def handle(self, alert: AlertResponse) -> ResponseResult:
        payload = {
            "text": (
                f"🚨 NIDS Alert: {alert.signature} 🚨\n"
                f"Severity: {alert.severity}\n"
                f"Source: {alert.src_ip} -> Dest: {alert.dst_ip}"
            )
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.webhook_url, json=payload, timeout=5.0)
            if response.status_code >= 400:
                logger.error("Webhook failed: %s", response.text)
                return ResponseResult(
                    handler_name=self.name,
                    action="webhook_post",
                    status="FAILED",
                    details={"status_code": response.status_code},
                )
            return ResponseResult(
                handler_name=self.name,
                action="webhook_post",
                status="SUCCESS",
                details={"status_code": response.status_code},
            )
        except Exception as exc:
            logger.error("Error sending webhook: %s", exc)
            return ResponseResult(
                handler_name=self.name,
                action="webhook_post",
                status="FAILED",
                details={"error": str(exc)},
            )

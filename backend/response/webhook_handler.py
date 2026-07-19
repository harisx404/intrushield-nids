import httpx
import logging
from typing import Dict, Any
from backend.response.base_handler import BaseResponseHandler
from backend.core.config import settings

logger = logging.getLogger(__name__)

class WebhookHandler(BaseResponseHandler):
    @property
    def name(self) -> str:
        return "WebhookHandler"

    def __init__(self):
        self.webhook_url = settings.WEBHOOK_URL

    async def should_handle(self, alert_data: Dict[str, Any]) -> bool:
        alert_info = alert_data.get('alert', {})
        severity = alert_info.get("severity", "")
        return severity in ["HIGH", "CRITICAL"] and bool(self.webhook_url) and self.webhook_url != "https://hooks.slack.com/services/DUMMY/WEBHOOK/URL"

    async def handle(self, alert_data: Dict[str, Any]) -> None:
        alert_info = alert_data.get('alert', {})
        payload = {
            "text": f"🚨 NIDS Alert: {alert_info.get('signature')} 🚨\n"
                    f"Severity: {alert_info.get('severity')}\n"
                    f"Source: {alert_info.get('src_ip')} -> Dest: {alert_info.get('dest_ip')}"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.webhook_url, json=payload, timeout=5.0)
                if response.status_code >= 400:
                    logger.error(f"Webhook failed: {response.text}")
        except Exception as e:
            logger.error(f"Error sending webhook: {e}")

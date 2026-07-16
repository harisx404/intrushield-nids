import logging
from typing import Dict, Any
from backend.response.base_handler import BaseResponseHandler
from backend.core.config import settings

logger = logging.getLogger(__name__)

class EmailHandler(BaseResponseHandler):
    def __init__(self):
        super().__init__(name="EmailHandler")

    async def should_handle(self, alert_data: Dict[str, Any]) -> bool:
        alert_info = alert_data.get('alert', {})
        return alert_info.get("severity") == "CRITICAL" and bool(settings.SMTP_SERVER)

    async def handle(self, alert_data: Dict[str, Any]) -> None:
        alert_info = alert_data.get('alert', {})
        logger.info(f"Simulating Email sent for CRITICAL alert: {alert_info.get('signature')}")

import logging
from typing import Dict, Any
from backend.response.base_handler import BaseResponseHandler

logger = logging.getLogger("nids.response.log")

class LogHandler(BaseResponseHandler):
    def __init__(self):
        super().__init__(name="LogHandler")

    async def should_handle(self, alert_data: Dict[str, Any]) -> bool:
        return True

    async def handle(self, alert_data: Dict[str, Any]) -> None:
        alert_info = alert_data.get('alert', {})
        logger.info(f"INCIDENT LOGGED: Alert ID {alert_data.get('alert_id')} - {alert_info.get('signature')}")

import asyncio
import logging
from typing import Dict, Any, List
from backend.core.event_bus import event_bus
from backend.response.base_handler import BaseResponseHandler
from backend.response.log_handler import LogHandler
from backend.response.webhook_handler import WebhookHandler
from backend.response.email_handler import EmailHandler

logger = logging.getLogger(__name__)

class ResponseEngine:
    def __init__(self):
        self.handlers: List[BaseResponseHandler] = [
            LogHandler(),
            WebhookHandler(),
            EmailHandler()
        ]
        
    def start(self):
        """Subscribe to the event bus."""
        event_bus.subscribe("new_alert", self.process_alert)
        logger.info("Response Engine started and subscribed to new_alert events.")

    async def process_alert(self, alert_data: Dict[str, Any]) -> None:
        """Process an incoming alert through all registered handlers."""
        tasks = []
        for handler in self.handlers:
            try:
                if await handler.should_handle(alert_data):
                    tasks.append(asyncio.create_task(handler.handle(alert_data)))
            except Exception as e:
                logger.error(f"Handler {handler.name} failed during should_handle: {e}")
                
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for handler, result in zip(self.handlers, results):
                if isinstance(result, Exception):
                    logger.error(f"Handler {handler.name} failed during handle: {result}")

response_engine = ResponseEngine()

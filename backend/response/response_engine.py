import asyncio
import logging

from backend.core.database import AsyncSessionLocal
from backend.core.event_bus import event_bus
from backend.repositories import response_repo
from backend.response.base_handler import BaseResponseHandler, ResponseResult
from backend.response.email_handler import EmailHandler
from backend.response.log_handler import LogHandler
from backend.response.webhook_handler import WebhookHandler
from backend.schemas.alert import AlertResponse

logger = logging.getLogger(__name__)


class ResponseEngine:
    def __init__(self):
        self.handlers: list[BaseResponseHandler] = [
            LogHandler(),
            WebhookHandler(),
            EmailHandler(),
        ]

    def start(self):
        """Subscribe to the event bus."""
        event_bus.subscribe("new_alert", self.process_alert)
        logger.info("Response Engine started and subscribed to new_alert events.")

    async def process_alert(self, alert: AlertResponse) -> None:
        """Process an incoming alert through all registered handlers."""
        # Pair each task with its handler so results are attributed correctly
        # (only handlers whose should_handle() returned True are scheduled).
        selected: list[BaseResponseHandler] = []
        tasks = []
        for handler in self.handlers:
            try:
                if handler.should_handle(alert):
                    selected.append(handler)
                    tasks.append(asyncio.create_task(handler.handle(alert)))
            except Exception as e:
                logger.error(f"Handler {handler.name} failed during should_handle: {e}")

        if not tasks:
            return

        results = await asyncio.gather(*tasks, return_exceptions=True)
        completed: list[ResponseResult] = []
        for handler, result in zip(selected, results, strict=True):
            if isinstance(result, Exception):
                logger.error(f"Handler {handler.name} failed during handle: {result}")
            else:
                completed.append(result)

        if completed:
            await self._persist_results(alert.id, completed)

    async def _persist_results(
        self, alert_id: int | None, results: list[ResponseResult]
    ) -> None:
        """Record each handler's outcome so responses are auditable."""
        try:
            async with AsyncSessionLocal() as session:
                for result in results:
                    await response_repo.record_result(
                        session, alert_id=alert_id, result=result
                    )
        except Exception as exc:  # never let persistence break alert processing
            logger.error(f"Failed to persist response results: {exc}")


response_engine = ResponseEngine()

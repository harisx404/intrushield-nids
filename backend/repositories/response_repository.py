"""Repository for persisting response-handler execution records."""

from typing import TYPE_CHECKING

from backend.models.response_log import ResponseLog
from backend.repositories.base import BaseRepository
from backend.schemas.response_log import ResponseLogCreate
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from backend.response.base_handler import ResponseResult


class ResponseRepository(
    BaseRepository[ResponseLog, ResponseLogCreate, ResponseLogCreate]
):
    async def record_result(
        self, db: AsyncSession, *, alert_id: int | None, result: "ResponseResult"
    ) -> ResponseLog:
        """Persist a single handler's ResponseResult as a response log row."""
        obj_in = ResponseLogCreate(
            alert_id=alert_id,
            handler_name=result.handler_name,
            action_taken=result.action,
            status=result.status,
            details=result.details,
        )
        return await self.create(session=db, obj_in=obj_in)


response_repo = ResponseRepository(ResponseLog)

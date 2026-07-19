"""Pydantic schemas for response-handler execution records."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ResponseLogBase(BaseModel):
    alert_id: int | None = None
    handler_name: str
    action_taken: str
    status: str
    details: dict[str, Any] | None = None


class ResponseLogCreate(ResponseLogBase):
    pass


class ResponseLogResponse(ResponseLogBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

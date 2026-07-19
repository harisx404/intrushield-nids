from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class NetworkEventBase(BaseModel):
    timestamp: datetime
    event_type: str
    src_ip: str
    src_port: int | None = None
    dest_ip: str
    dest_port: int | None = None
    protocol: str
    flow_id: int | None = None
    content: dict[str, Any] = Field(default_factory=dict)


class NetworkEventCreate(NetworkEventBase):
    pass


class NetworkEventResponse(NetworkEventBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

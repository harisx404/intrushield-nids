from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Dict, Any, Optional

class NetworkEventBase(BaseModel):
    timestamp: datetime
    event_type: str
    src_ip: str
    src_port: Optional[int] = None
    dest_ip: str
    dest_port: Optional[int] = None
    protocol: str
    flow_id: Optional[int] = None
    content: Dict[str, Any] = Field(default_factory=dict)

class NetworkEventCreate(NetworkEventBase):
    pass

class NetworkEventResponse(NetworkEventBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

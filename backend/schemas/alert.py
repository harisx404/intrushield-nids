from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Dict, Any, Optional

class AlertBase(BaseModel):
    timestamp: datetime
    src_ip: str
    src_port: Optional[int] = None
    dest_ip: str
    dest_port: Optional[int] = None
    protocol: str
    signature: str
    signature_id: int
    severity: str
    category: Optional[str] = None
    flow_id: Optional[int] = None
    payload_printable: Optional[str] = None
    src_country: Optional[str] = None
    status: str = "NEW"
    raw_eve: Dict[str, Any] = Field(default_factory=dict)

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    status: Optional[str] = None

class AlertResponse(AlertBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

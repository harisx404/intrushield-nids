from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AuditLogBase(BaseModel):
    action: str
    details: str
    alert_id: Optional[int] = None
    user_id: Optional[int] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogResponse(AuditLogBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

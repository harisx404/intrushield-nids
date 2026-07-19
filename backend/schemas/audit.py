from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogBase(BaseModel):
    action: str
    details: str
    alert_id: int | None = None
    user_id: int | None = None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogResponse(AuditLogBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

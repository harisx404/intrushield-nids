from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DetectionRuleBase(BaseModel):
    sid: int
    name: str
    body: str
    severity: str
    category: str
    is_active: bool = True
    is_custom: bool = True


class DetectionRuleCreate(DetectionRuleBase):
    pass


class DetectionRuleUpdate(BaseModel):
    name: str | None = None
    body: str | None = None
    severity: str | None = None
    category: str | None = None
    is_active: bool | None = None


class DetectionRuleResponse(DetectionRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

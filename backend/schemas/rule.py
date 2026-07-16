from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

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
    name: Optional[str] = None
    body: Optional[str] = None
    severity: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None

class DetectionRuleResponse(DetectionRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

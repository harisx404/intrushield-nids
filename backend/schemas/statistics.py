from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TrafficStatisticsBase(BaseModel):
    timestamp: datetime
    alerts_total: int = 0
    alerts_critical: int = 0
    alerts_high: int = 0
    bytes_in: int = 0
    bytes_out: int = 0
    packets_in: int = 0
    packets_out: int = 0

class TrafficStatisticsCreate(TrafficStatisticsBase):
    pass

class TrafficStatisticsResponse(TrafficStatisticsBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

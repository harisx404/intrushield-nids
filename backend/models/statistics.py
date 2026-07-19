from datetime import datetime

from backend.models.base import Base
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime


class TrafficStatistics(Base):
    __tablename__ = "statistics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True, unique=True
    )

    # Aggregated stats
    alerts_total: Mapped[int] = mapped_column(Integer, default=0)
    alerts_critical: Mapped[int] = mapped_column(Integer, default=0)
    alerts_high: Mapped[int] = mapped_column(Integer, default=0)

    bytes_in: Mapped[int] = mapped_column(Integer, default=0)
    bytes_out: Mapped[int] = mapped_column(Integer, default=0)
    packets_in: Mapped[int] = mapped_column(Integer, default=0)
    packets_out: Mapped[int] = mapped_column(Integer, default=0)

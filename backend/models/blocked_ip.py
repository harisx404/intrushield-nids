from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.types import DateTime
from typing import Optional

from backend.models.base import Base, TimestampMixin

class BlockedIP(Base, TimestampMixin):
    __tablename__ = "blocked_ips"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ip_address: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    reason: Mapped[str] = mapped_column(String(255))
    
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

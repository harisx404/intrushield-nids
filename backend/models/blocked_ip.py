from datetime import datetime

from backend.models.base import Base, TimestampMixin
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime


class BlockedIP(Base, TimestampMixin):
    __tablename__ = "blocked_ips"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ip_address: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    reason: Mapped[str] = mapped_column(String(255))

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

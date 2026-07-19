from backend.models.base import Base, TimestampMixin
from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column


class DetectionRule(Base, TimestampMixin):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sid: Mapped[int] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))

    # Suricata rule body
    body: Mapped[str] = mapped_column(Text)

    # Metadata
    severity: Mapped[str] = mapped_column(String(20))
    category: Mapped[str] = mapped_column(String(100))

    # State
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_custom: Mapped[bool] = mapped_column(Boolean, default=True)

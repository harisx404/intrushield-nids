from typing import Any

from backend.models.base import Base, TimestampMixin
from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class ResponseLog(Base, TimestampMixin):
    __tablename__ = "response_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    alert_id: Mapped[int | None] = mapped_column(
        ForeignKey("alerts.id", ondelete="SET NULL"), nullable=True
    )

    handler_name: Mapped[str] = mapped_column(String(50))  # email, iptables, webhook
    action_taken: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20))  # success, failed

    details: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

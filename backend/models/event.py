from datetime import datetime
from typing import Any

from backend.models.base import Base, TimestampMixin
from sqlalchemy import JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime


class NetworkEvent(Base, TimestampMixin):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    event_type: Mapped[str] = mapped_column(
        String(50), index=True
    )  # flow, dns, http, tls

    src_ip: Mapped[str] = mapped_column(String(50), index=True)
    src_port: Mapped[int | None] = mapped_column(Integer, nullable=True)
    dest_ip: Mapped[str] = mapped_column(String(50), index=True)
    dest_port: Mapped[int | None] = mapped_column(Integer, nullable=True)

    protocol: Mapped[str] = mapped_column(String(20))
    flow_id: Mapped[int | None] = mapped_column(index=True, nullable=True)

    # Event-specific content
    content: Mapped[dict[str, Any]] = mapped_column(JSON)

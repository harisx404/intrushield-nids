from sqlalchemy import String, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.types import DateTime

from backend.models.base import Base, TimestampMixin

class NetworkEvent(Base, TimestampMixin):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    event_type: Mapped[str] = mapped_column(String(50), index=True) # flow, dns, http, tls
    
    src_ip: Mapped[str] = mapped_column(String(50), index=True)
    src_port: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    dest_ip: Mapped[str] = mapped_column(String(50), index=True)
    dest_port: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    protocol: Mapped[str] = mapped_column(String(20))
    flow_id: Mapped[Optional[int]] = mapped_column(index=True, nullable=True)
    
    # Event-specific content
    content: Mapped[Dict[str, Any]] = mapped_column(JSON)

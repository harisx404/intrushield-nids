from sqlalchemy import String, Integer, JSON, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.types import DateTime

from backend.models.base import Base, TimestampMixin

class Alert(Base, TimestampMixin):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    src_ip: Mapped[str] = mapped_column(String(50), index=True)
    src_port: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    dest_ip: Mapped[str] = mapped_column(String(50), index=True)
    dest_port: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    protocol: Mapped[str] = mapped_column(String(20))
    
    # Alert specifics
    signature: Mapped[str] = mapped_column(String(255))
    signature_id: Mapped[int] = mapped_column(index=True)
    severity: Mapped[str] = mapped_column(String(20), index=True)  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Flow and context
    flow_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    payload_printable: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Enrichment
    src_country: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    
    # State
    status: Mapped[str] = mapped_column(String(20), default="NEW", index=True)
    
    # Raw JSON from EVE
    raw_eve: Mapped[Dict[str, Any]] = mapped_column(JSON)
    
    # Relationships
    audit_logs = relationship("AuditLog", back_populates="alert")

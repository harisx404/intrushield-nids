from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from typing import Dict, Any, Optional

from backend.models.base import Base, TimestampMixin

class ResponseLog(Base, TimestampMixin):
    __tablename__ = "response_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    alert_id: Mapped[Optional[int]] = mapped_column(ForeignKey("alerts.id", ondelete="SET NULL"), nullable=True)
    
    handler_name: Mapped[str] = mapped_column(String(50)) # email, iptables, webhook
    action_taken: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20)) # success, failed
    
    details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

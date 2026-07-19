from backend.models.base import Base, TimestampMixin
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    alert_id: Mapped[int | None] = mapped_column(
        ForeignKey("alerts.id", ondelete="CASCADE"), nullable=True
    )

    action: Mapped[str] = mapped_column(
        String(100)
    )  # e.g., "status_change", "rule_updated"
    details: Mapped[str] = mapped_column(String(500))

    user = relationship("User")
    alert = relationship("Alert")

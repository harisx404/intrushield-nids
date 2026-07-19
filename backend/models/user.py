from backend.models.base import Base, TimestampMixin
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    role: Mapped[str] = mapped_column(String(20), default="analyst")  # admin, analyst
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

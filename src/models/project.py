from sqlalchemy import String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, TimestampMixin
import enum
from typing import Optional

class ProjectStatus(enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("active", "completed", "paused", "cancelled", name="project_status"),
        default="active"
    )
    client_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    repository_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
from sqlalchemy import String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin
import enum

class ProjectStatus(enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus),
        default=ProjectStatus.ACTIVE
    )
    client_info: Mapped[str] = mapped_column(Text, nullable=True)
    repository_url: Mapped[str] = mapped_column(String(500), nullable=True)

    # Relationships
    conversations: Mapped[list["Conversation"]] = relationship("Conversation", back_populates="project")

    def __init__(self, **kwargs):
        if 'status' in kwargs and isinstance(kwargs['status'], str):
            kwargs['status'] = ProjectStatus(kwargs['status'])
        super().__init__(**kwargs)
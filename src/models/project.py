from sqlalchemy import String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column
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

    def __init__(self, **kwargs):
        # Handle string to enum conversion for status
        if 'status' in kwargs and isinstance(kwargs['status'], str):
            status_str = kwargs['status']
            for status_enum in ProjectStatus:
                if status_enum.value == status_str:
                    kwargs['status'] = status_enum
                    break
            else:
                raise ValueError(f"Invalid status: {status_str}")
        super().__init__(**kwargs)
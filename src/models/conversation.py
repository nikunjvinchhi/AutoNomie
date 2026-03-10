from sqlalchemy import String, Text, Float, Integer, JSON, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin
import enum

class ConversationPhase(enum.Enum):
    INTRODUCTION = "introduction"
    CORE_REQUIREMENTS = "core_requirements"
    ADAPTIVE_FOLLOWUP = "adaptive_followup"
    VALIDATION = "validation"
    COMPLETED = "completed"

class ConversationStatus(enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    FAILED = "failed"

class Conversation(Base, TimestampMixin):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    current_phase: Mapped[ConversationPhase] = mapped_column(
        Enum(ConversationPhase),
        default=ConversationPhase.INTRODUCTION
    )
    completion_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    participant_info: Mapped[dict] = mapped_column(JSON, nullable=True)
    conversation_context: Mapped[dict] = mapped_column(JSON, nullable=True)
    status: Mapped[ConversationStatus] = mapped_column(
        Enum(ConversationStatus),
        default=ConversationStatus.ACTIVE
    )

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="conversations")
    requirements: Mapped[list["Requirement"]] = relationship("Requirement", back_populates="conversation")
    specifications: Mapped[list["Specification"]] = relationship("Specification", back_populates="conversation")
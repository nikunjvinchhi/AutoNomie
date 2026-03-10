from sqlalchemy import String, Text, JSON, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin
import enum

class ApprovalStatus(enum.Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"

class Specification(Base, TimestampMixin):
    __tablename__ = "specifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1)
    json_data: Mapped[dict] = mapped_column(JSON)
    markdown_content: Mapped[str] = mapped_column(Text)
    approval_status: Mapped[ApprovalStatus] = mapped_column(
        Enum(ApprovalStatus),
        default=ApprovalStatus.DRAFT
    )
    reviewer_feedback: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="specifications")
    project: Mapped["Project"] = relationship("Project", back_populates="specifications")
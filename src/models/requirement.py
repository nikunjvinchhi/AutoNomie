from sqlalchemy import String, Text, JSON, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin
import enum

class RequirementCategory(enum.Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    TECHNICAL = "technical"
    BUSINESS = "business"

class RequirementPriority(enum.Enum):
    MUST_HAVE = "must_have"
    SHOULD_HAVE = "should_have"
    COULD_HAVE = "could_have"
    WONT_HAVE = "wont_have"

class Requirement(Base, TimestampMixin):
    __tablename__ = "requirements"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), nullable=False)
    category: Mapped[RequirementCategory] = mapped_column(Enum(RequirementCategory))
    priority: Mapped[RequirementPriority] = mapped_column(Enum(RequirementPriority))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    extracted_data: Mapped[dict] = mapped_column(JSON)
    validation_status: Mapped[str] = mapped_column(String(50), default="pending")

    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="requirements")
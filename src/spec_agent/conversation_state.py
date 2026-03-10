from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from ..models.conversation import ConversationPhase, ConversationStatus

@dataclass
class ConversationState:
    """Manages conversation state and context."""

    conversation_id: int
    project_id: int
    current_phase: ConversationPhase
    status: ConversationStatus
    completion_percentage: float
    context: Dict[str, Any]
    message_history: List[Dict[str, Any]]

    def update_context(self, updates: Dict[str, Any]) -> None:
        """Update conversation context with new data."""
        self.context.update(updates)

    def add_message(self, message: Dict[str, Any]) -> None:
        """Add message to conversation history."""
        self.message_history.append(message)

    def advance_phase(self, next_phase: ConversationPhase) -> None:
        """Advance to next conversation phase."""
        self.current_phase = next_phase
        self.update_completion_percentage()

    def update_completion_percentage(self) -> None:
        """Update completion percentage based on current phase."""
        phase_percentages = {
            ConversationPhase.INTRODUCTION: 20.0,
            ConversationPhase.CORE_REQUIREMENTS: 50.0,
            ConversationPhase.ADAPTIVE_FOLLOWUP: 80.0,
            ConversationPhase.VALIDATION: 95.0,
            ConversationPhase.COMPLETED: 100.0
        }
        self.completion_percentage = phase_percentages.get(self.current_phase, 0.0)
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from .input_processors import ChatInputProcessor, InputProcessor
from .conversation_state import ConversationState
from .requirement_extractor import RequirementExtractor
from ..models.conversation import Conversation, ConversationPhase, ConversationStatus
from ..models.project import Project

class SpecAgent:
    """Main orchestrator for requirement gathering conversations."""

    def __init__(self, db_session: Session, input_processor: Optional[InputProcessor] = None):
        self.db_session = db_session
        self.input_processor = input_processor or ChatInputProcessor()
        self.requirement_extractor = RequirementExtractor()

    def start_conversation(self, project_id: int, client_info: Dict[str, Any]) -> Dict[str, Any]:
        """Start a new requirement gathering conversation."""
        # Create conversation record
        conversation = Conversation(
            project_id=project_id,
            current_phase=ConversationPhase.INTRODUCTION,
            completion_percentage=0.0,
            participant_info=client_info,
            conversation_context={},
            status=ConversationStatus.ACTIVE
        )

        self.db_session.add(conversation)
        self.db_session.commit()
        self.db_session.refresh(conversation)

        # Get initial message
        initial_message = self.input_processor.get_next_question(
            ConversationPhase.INTRODUCTION, {}
        )

        return {
            "conversation_id": conversation.id,
            "initial_message": initial_message,
            "current_phase": conversation.current_phase.value,
            "completion_percentage": conversation.completion_percentage
        }

    def process_message(self, conversation_id: int, message: str, sender_type: str = "client") -> Dict[str, Any]:
        """Process incoming message and return AI response."""
        # Get conversation
        conversation = self.db_session.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")

        # Create conversation state
        state = ConversationState(
            conversation_id=conversation.id,
            project_id=conversation.project_id,
            current_phase=conversation.current_phase,
            status=conversation.status,
            completion_percentage=conversation.completion_percentage,
            context=conversation.conversation_context or {},
            message_history=[]
        )

        # Process message through input processor
        response = self.input_processor.process_message(message, state.context)

        # Update conversation state
        state.update_context(response.get("context_updates", {}))
        state.add_message({
            "sender": sender_type,
            "content": message,
            "timestamp": "now"  # Will use actual timestamp in real implementation
        })

        # Check for phase completion and advancement
        if response.get("phase_complete", False):
            next_phase = self._get_next_phase(state.current_phase)
            if next_phase:
                state.advance_phase(next_phase)

        # Update database
        conversation.conversation_context = state.context
        conversation.completion_percentage = state.completion_percentage
        conversation.current_phase = state.current_phase
        self.db_session.commit()

        return {
            "ai_response": response["response"],
            "conversation_state": {
                "current_phase": state.current_phase.value,
                "completion_percentage": state.completion_percentage
            },
            "next_question": self.input_processor.get_next_question(
                state.current_phase, state.context
            )
        }

    def _get_next_phase(self, current_phase: ConversationPhase) -> Optional[ConversationPhase]:
        """Get next conversation phase."""
        phase_order = [
            ConversationPhase.INTRODUCTION,
            ConversationPhase.CORE_REQUIREMENTS,
            ConversationPhase.ADAPTIVE_FOLLOWUP,
            ConversationPhase.VALIDATION,
            ConversationPhase.COMPLETED
        ]

        try:
            current_index = phase_order.index(current_phase)
            if current_index < len(phase_order) - 1:
                return phase_order[current_index + 1]
        except ValueError:
            pass

        return None
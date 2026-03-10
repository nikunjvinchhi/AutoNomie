from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from ..models.conversation import ConversationPhase

class InputProcessor(ABC):
    """Abstract interface for processing different types of input."""

    @abstractmethod
    def process_message(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming message and return structured response."""
        pass

    @abstractmethod
    def get_next_question(self, phase: ConversationPhase, context: Dict[str, Any]) -> Optional[str]:
        """Get next question based on current phase and context."""
        pass

    @abstractmethod
    def extract_requirements(self, conversation_history: List[Dict]) -> List[Dict[str, Any]]:
        """Extract structured requirements from conversation history."""
        pass

class ChatInputProcessor(InputProcessor):
    """Processes text-based chat conversations."""

    def __init__(self):
        self.structured_questions = {
            ConversationPhase.INTRODUCTION: [
                "What type of software are you looking to build?",
                "Who is your target audience or primary users?",
                "What's the main problem you're trying to solve?"
            ],
            ConversationPhase.CORE_REQUIREMENTS: [
                "What are the must-have features for your first version?",
                "How many users do you expect to support?",
                "Are there any specific technologies or platforms you require?"
            ]
        }

    def process_message(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process chat message and return response with context updates."""
        # Basic implementation - will be enhanced with OpenAI integration
        return {
            "response": "Thank you for that information. Let me ask you more details.",
            "context_updates": {"last_message": message},
            "phase_complete": False
        }

    def get_next_question(self, phase: ConversationPhase, context: Dict[str, Any]) -> Optional[str]:
        """Get next structured question for current phase."""
        questions = self.structured_questions.get(phase, [])
        asked_count = context.get("questions_asked", 0)

        if asked_count < len(questions):
            return questions[asked_count]
        return None

    def extract_requirements(self, conversation_history: List[Dict]) -> List[Dict[str, Any]]:
        """Extract requirements from conversation - placeholder implementation."""
        return []
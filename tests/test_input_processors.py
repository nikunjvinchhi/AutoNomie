import pytest
from src.spec_agent.input_processors import InputProcessor, ChatInputProcessor
from src.spec_agent.conversation_state import ConversationState
from src.models.conversation import ConversationPhase

def test_input_processor_interface():
    # Test that InputProcessor is abstract and cannot be instantiated
    with pytest.raises(TypeError):
        InputProcessor()

def test_chat_input_processor_creation():
    processor = ChatInputProcessor()
    assert processor is not None
    assert hasattr(processor, 'process_message')
    assert hasattr(processor, 'get_next_question')
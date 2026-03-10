import pytest
from unittest.mock import Mock, patch, MagicMock
from src.spec_agent.spec_agent import SpecAgent
from src.spec_agent.input_processors import ChatInputProcessor
from src.models.conversation import ConversationPhase

@pytest.fixture
def mock_db_session():
    return Mock()

def test_spec_agent_creation():
    agent = SpecAgent(db_session=Mock())
    assert agent is not None
    assert isinstance(agent.input_processor, ChatInputProcessor)

@patch('src.spec_agent.spec_agent.Conversation')
def test_start_conversation(mock_conversation_class, mock_db_session):
    # Mock the conversation instance
    mock_conversation = MagicMock()
    mock_conversation.id = 1
    mock_conversation.current_phase = ConversationPhase.INTRODUCTION
    mock_conversation.completion_percentage = 0.0
    mock_conversation_class.return_value = mock_conversation

    # Mock the input processor
    mock_input_processor = Mock()
    mock_input_processor.get_next_question.return_value = "Hello! Let's start gathering your requirements."

    agent = SpecAgent(db_session=mock_db_session, input_processor=mock_input_processor)
    result = agent.start_conversation(project_id=1, client_info={"name": "Test Client"})

    assert "conversation_id" in result
    assert "initial_message" in result
    assert result["current_phase"] == ConversationPhase.INTRODUCTION.value
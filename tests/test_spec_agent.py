import pytest
from unittest.mock import Mock, patch
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

def test_start_conversation(mock_db_session):
    agent = SpecAgent(db_session=mock_db_session)
    result = agent.start_conversation(project_id=1, client_info={"name": "Test Client"})

    assert "conversation_id" in result
    assert "initial_message" in result
    assert result["current_phase"] == ConversationPhase.INTRODUCTION.value
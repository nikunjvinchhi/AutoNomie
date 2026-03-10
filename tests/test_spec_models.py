import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.models.project import Project  # Need to import to create the table
from src.models.conversation import Conversation, ConversationPhase, ConversationStatus

@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_conversation_creation(test_db):
    conversation = Conversation(
        project_id=1,
        current_phase=ConversationPhase.INTRODUCTION,
        completion_percentage=0.0,
        participant_info={"client_name": "Test Client"},
        conversation_context={},
        status=ConversationStatus.ACTIVE
    )
    test_db.add(conversation)
    test_db.commit()

    assert conversation.id is not None
    assert conversation.current_phase == ConversationPhase.INTRODUCTION
    assert conversation.status == ConversationStatus.ACTIVE
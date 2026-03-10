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
    # Create a project first
    project = Project(
        name="Test Project",
        description="Test description"
    )
    test_db.add(project)
    test_db.commit()

    conversation = Conversation(
        project_id=project.id,
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
    assert conversation.project_id == project.id

def test_conversation_with_null_fields(test_db):
    # Create a project first
    project = Project(
        name="Test Project",
        description="Test description"
    )
    test_db.add(project)
    test_db.commit()

    # Test with nullable JSON fields set to None
    conversation = Conversation(
        project_id=project.id,
        current_phase=ConversationPhase.INTRODUCTION,
        completion_percentage=50.0,
        participant_info=None,
        conversation_context=None,
        status=ConversationStatus.ACTIVE
    )
    test_db.add(conversation)
    test_db.commit()

    assert conversation.id is not None
    assert conversation.participant_info is None
    assert conversation.conversation_context is None
    assert conversation.completion_percentage == 50.0
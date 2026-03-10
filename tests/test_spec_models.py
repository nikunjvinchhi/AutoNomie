import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.models.project import Project  # Need to import to create the table
from src.models.conversation import Conversation, ConversationPhase, ConversationStatus
from src.models.requirement import Requirement, RequirementCategory, RequirementPriority
from src.models.specification import Specification, ApprovalStatus  # Import specification model

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

def test_requirement_creation(test_db):
    requirement = Requirement(
        conversation_id=1,
        category=RequirementCategory.FUNCTIONAL,
        priority=RequirementPriority.MUST_HAVE,
        content="User should be able to login",
        extracted_data={"feature": "authentication"},
        validation_status="pending"
    )
    test_db.add(requirement)
    test_db.commit()

    assert requirement.id is not None
    assert requirement.category == RequirementCategory.FUNCTIONAL
    assert requirement.priority == RequirementPriority.MUST_HAVE

def test_specification_creation(test_db):
    # Create a project first
    project = Project(
        name="Test Project",
        description="Test description"
    )
    test_db.add(project)
    test_db.commit()

    specification = Specification(
        conversation_id=1,
        project_id=project.id,
        version=1,
        json_data={"features": ["login", "dashboard"]},
        markdown_content="# Project Specification",
        approval_status=ApprovalStatus.DRAFT,
        reviewer_feedback=None
    )
    test_db.add(specification)
    test_db.commit()

    assert specification.id is not None
    assert specification.approval_status == ApprovalStatus.DRAFT
    assert specification.version == 1
    assert specification.project_id == project.id
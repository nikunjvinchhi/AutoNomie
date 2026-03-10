import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import create_tables, SessionLocal
from src.models.project import Project, ProjectStatus

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    """Set up test database with required data."""
    create_tables()
    db = SessionLocal()

    # Create test project
    test_project = Project(
        name="Test Project",
        description="A test project",
        status=ProjectStatus.ACTIVE,
        client_info="Test client info"
    )
    db.add(test_project)
    db.commit()
    db.refresh(test_project)

    # Store project_id for tests to use
    global test_project_id
    test_project_id = test_project.id

    db.close()
    yield
    # Cleanup would go here if needed

client = TestClient(app)

def test_start_conversation():
    # Create a test project first (assuming project creation endpoint exists)
    conversation_data = {
        "project_id": test_project_id,
        "client_info": {"name": "Test Client", "email": "test@example.com"}
    }
    response = client.post("/spec-agent/conversations/", json=conversation_data)
    assert response.status_code == 201
    assert "conversation_id" in response.json()
    assert "initial_message" in response.json()

def test_send_message():
    # First start a conversation
    conversation_data = {"project_id": test_project_id, "client_info": {"name": "Test Client"}}
    conv_response = client.post("/spec-agent/conversations/", json=conversation_data)
    conversation_id = conv_response.json()["conversation_id"]

    # Send message
    message_data = {"message_text": "I want to build a web application"}
    response = client.post(f"/spec-agent/conversations/{conversation_id}/messages/", json=message_data)
    assert response.status_code == 200
    assert "ai_response" in response.json()
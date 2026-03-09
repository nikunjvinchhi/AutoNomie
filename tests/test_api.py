import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_project():
    project_data = {
        "name": "Test Project",
        "description": "Test description",
        "client_info": "Test Client"
    }
    response = client.post("/projects/", json=project_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Project"
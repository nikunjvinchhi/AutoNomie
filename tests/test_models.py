import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.models.project import Project, ProjectStatus

@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_project_creation(test_db):
    project = Project(
        name="Test Project",
        description="Test description",
        status=ProjectStatus.ACTIVE
    )
    test_db.add(project)
    test_db.commit()

    assert project.id is not None
    assert project.name == "Test Project"
    assert project.created_at is not None
# AutoNomie Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build MVP of AutoNomie's Spec Agent with basic orchestrator for autonomous requirement gathering and specification generation.

**Architecture:** Modular agent system with FastAPI backend, React frontend, PostgreSQL database, and OpenAI integration for AI agent capabilities.

**Tech Stack:** Python/FastAPI, React/TypeScript, PostgreSQL, OpenAI API, Docker, Git integration

---

## Phase 1: Project Foundation & Setup

### Task 1: Project Structure Setup

**Files:**
- Create: `README.md`
- Create: `requirements.txt`
- Create: `docker-compose.yml`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `src/`
- Create: `tests/`
- Create: `frontend/`

**Step 1: Create project README**

Create comprehensive README with project overview:

```markdown
# AutoNomie - Autonomous Development Agent Ecosystem

End-to-end autonomous software development with human oversight.

## Quick Start
\`\`\`bash
cp .env.example .env
docker-compose up -d
\`\`\`

## Architecture
- Spec Agent: Requirement gathering and specification generation
- Code Agent: Supervised autonomous development (Phase 2)
- Test Agent: Comprehensive testing (Phase 3)
- Demo Agent: Stakeholder demos (Phase 4)
```

**Step 2: Create requirements.txt**

```text
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
openai==1.3.5
langchain==0.0.340
pydantic==2.5.0
python-multipart==0.0.6
python-dotenv==1.0.0
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

**Step 3: Create docker-compose.yml**

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: autonomie
      POSTGRES_USER: autonomie
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://autonomie:dev_password@db:5432/autonomie
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
    volumes:
      - .:/app

volumes:
  postgres_data:
```

**Step 4: Create environment template**

```bash
# .env.example
OPENAI_API_KEY=your_openai_key_here
DATABASE_URL=postgresql://autonomie:dev_password@localhost:5432/autonomie
SECRET_KEY=your_secret_key_here
DEBUG=true
```

**Step 5: Create .gitignore**

```text
__pycache__/
*.pyc
.env
.venv/
venv/
node_modules/
.DS_Store
*.log
.pytest_cache/
.coverage
build/
dist/
*.egg-info/
```

**Step 6: Commit foundation**

```bash
git add .
git commit -m "feat: project foundation setup

- Add README with project overview
- Configure Docker and dependencies
- Set up environment template and gitignore"
```

### Task 2: Database Models & Schema

**Files:**
- Create: `src/models/__init__.py`
- Create: `src/models/base.py`
- Create: `src/models/project.py`
- Create: `src/models/agent.py`
- Create: `src/database.py`
- Create: `alembic.ini`
- Create: `alembic/env.py`

**Step 1: Write database base model test**

Create `tests/test_models.py`:

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.models.project import Project

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
        status="active"
    )
    test_db.add(project)
    test_db.commit()

    assert project.id is not None
    assert project.name == "Test Project"
    assert project.created_at is not None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_models.py -v`
Expected: FAIL with "no module named src.models"

**Step 3: Create base model**

Create `src/models/base.py`:

```python
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
```

**Step 4: Create project model**

Create `src/models/project.py`:

```python
from sqlalchemy import String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, TimestampMixin
import enum

class ProjectStatus(enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus),
        default=ProjectStatus.ACTIVE
    )
    client_info: Mapped[str] = mapped_column(Text)
    repository_url: Mapped[str] = mapped_column(String(500))
```

**Step 5: Create database setup**

Create `src/database.py`:

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.base import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://autonomie:dev_password@localhost:5432/autonomie")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
```

**Step 6: Run test to verify it passes**

Run: `pytest tests/test_models.py -v`
Expected: PASS

**Step 7: Commit database models**

```bash
git add src/models/ src/database.py tests/test_models.py
git commit -m "feat: database models and schema

- Add base model with timestamp mixin
- Create Project model with status enum
- Set up database connection and session management
- Add basic model tests"
```

### Task 3: FastAPI Application Setup

**Files:**
- Create: `src/main.py`
- Create: `src/api/__init__.py`
- Create: `src/api/routes/__init__.py`
- Create: `src/api/routes/projects.py`
- Create: `src/schemas/project.py`
- Create: `Dockerfile`

**Step 1: Write API endpoint test**

Create `tests/test_api.py`:

```python
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
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_api.py -v`
Expected: FAIL with "no module named src.main"

**Step 3: Create main FastAPI app**

Create `src/main.py`:

```python
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .database import create_tables
from .api.routes import projects

app = FastAPI(
    title="AutoNomie API",
    description="Autonomous Development Agent Ecosystem",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(projects.router, prefix="/projects", tags=["projects"])
```

**Step 4: Create project schemas**

Create `src/schemas/project.py`:

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.project import ProjectStatus

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    client_info: Optional[str] = None
    repository_url: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: ProjectStatus
    client_info: Optional[str]
    repository_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

**Step 5: Create project routes**

Create `src/api/routes/projects.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...models.project import Project
from ...schemas.project import ProjectCreate, ProjectResponse

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProjectResponse)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
```

**Step 6: Create Dockerfile**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Step 7: Run tests to verify they pass**

Run: `pytest tests/test_api.py -v`
Expected: PASS

**Step 8: Commit FastAPI setup**

```bash
git add src/main.py src/api/ src/schemas/ Dockerfile tests/test_api.py
git commit -m "feat: FastAPI application setup

- Create main FastAPI app with CORS middleware
- Add project CRUD endpoints
- Implement Pydantic schemas for validation
- Add Dockerfile for containerization
- Add API endpoint tests"
```

---

## Phase 1 Complete

The foundation is ready! Next phase involves implementing the Spec Agent core functionality.

**Estimated completion time:** 2-3 days for experienced developer

**Next steps:**
- Implement OpenAI integration for Spec Agent
- Add requirement gathering conversation flows
- Create specification generation logic
- Build web interface for client interactions
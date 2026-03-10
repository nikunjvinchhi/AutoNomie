import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.base import Base
# Import all models to ensure they're registered with SQLAlchemy
from .models import Project, Conversation, Requirement, Specification

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

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
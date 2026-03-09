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
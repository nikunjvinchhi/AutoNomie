from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List
from ..models.conversation import ConversationPhase, ConversationStatus

class ConversationCreate(BaseModel):
    project_id: int
    client_info: Dict[str, Any]

class MessageCreate(BaseModel):
    message_text: str
    sender_type: str = "client"

class ConversationResponse(BaseModel):
    conversation_id: int
    initial_message: str
    current_phase: str
    completion_percentage: float

class MessageResponse(BaseModel):
    ai_response: str
    conversation_state: Dict[str, Any]
    next_question: Optional[str] = None

class ConversationStatus(BaseModel):
    id: int
    project_id: int
    current_phase: str
    completion_percentage: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
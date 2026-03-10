from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...spec_agent.spec_agent import SpecAgent
from ...schemas.spec_agent import (
    ConversationCreate, MessageCreate, ConversationResponse,
    MessageResponse, ConversationStatus
)
from ...models.conversation import Conversation

router = APIRouter()

@router.post("/conversations/", status_code=status.HTTP_201_CREATED, response_model=ConversationResponse)
async def start_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    """Start a new requirement gathering conversation."""
    try:
        spec_agent = SpecAgent(db_session=db)
        result = spec_agent.start_conversation(
            project_id=conversation.project_id,
            client_info=conversation.client_info
        )
        return ConversationResponse(**result)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start conversation: {str(e)}"
        )

@router.post("/conversations/{conversation_id}/messages/", response_model=MessageResponse)
async def send_message(
    conversation_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    """Send a message in an existing conversation."""
    try:
        spec_agent = SpecAgent(db_session=db)
        result = spec_agent.process_message(
            conversation_id=conversation_id,
            message=message.message_text,
            sender_type=message.sender_type
        )
        return MessageResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )

@router.get("/conversations/{conversation_id}/", response_model=ConversationStatus)
async def get_conversation_status(conversation_id: int, db: Session = Depends(get_db)):
    """Get current status of a conversation."""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return ConversationStatus.from_orm(conversation)
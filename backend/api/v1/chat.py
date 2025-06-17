"""
Chat API endpoints following RESTful principles
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from schemas.chat_schemas import ChatReq, Msg
from services.chat_service import ChatService

# RESTful resource-based router for conversations
router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_conversation_message(req: ChatReq):
    """Create a new conversation message and get AI response.

    Follows RESTful principle: POST /conversations creates a new conversation message.
    Returns 201 Created on successful message creation and processing.
    """
    try:
        chat_service = ChatService()
        answer = await chat_service.process_chat(req)
        return {"answer": answer}

    except Exception as e:
        print(f"❌ Error in conversation endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/", response_model=List[Msg])
async def list_conversation_history(limit: int = 20):
    """Retrieve conversation history.

    Follows RESTful principle: GET /conversations retrieves collection of conversation messages.
    Supports pagination via limit query parameter.
    """
    try:
        chat_service = ChatService()
        return chat_service.get_chat_history(limit)
    except Exception as e:
        print(f"❌ Error in conversation history endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

"""
Chat API endpoints
"""

from typing import List
from fastapi import APIRouter, HTTPException
from schemas.chat_schemas import ChatReq, Msg
from services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat(req: ChatReq):
    """Run the multi-agent system, store conversation, return response."""
    try:
        chat_service = ChatService()
        answer = await chat_service.process_chat(req)
        return {"answer": answer}

    except Exception as e:
        print(f"❌ Error in chat endpoint: {str(e)}")
        raise HTTPException(500, str(e))


@router.get("/history", response_model=List[Msg])
async def history(limit: int = 20):
    """Return the latest `limit` rows in ascending order."""
    try:
        chat_service = ChatService()
        return chat_service.get_chat_history(limit)
    except Exception as e:
        print(f"❌ Error in history endpoint: {str(e)}")
        raise HTTPException(500, str(e))

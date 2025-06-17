"""
CV API endpoints
"""

from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from schemas.cv_schemas import CVUploadResponse, CVListItem
from services.cv_service import CVService
from services.cv_status_service import get_status_for_frontend

router = APIRouter(prefix="/cv", tags=["cv"])


@router.post("/upload", response_model=CVUploadResponse)
async def upload_cv(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Handle CV file uploads, store them in Postgres, and process with agent system."""
    cv_service = CVService()
    return await cv_service.upload_cv(file, background_tasks)


@router.get("/list", response_model=List[CVListItem])
async def list_cvs():
    """Get list of uploaded CVs (for testing/debugging)."""
    cv_service = CVService()
    return cv_service.list_cvs()


@router.get("/status/{session_id}")
async def get_cv_status(session_id: str):
    """Get the current processing status for a CV upload session."""
    try:
        print(f"🔍 [STATUS API] Received request for session: {session_id}")
        status_data = get_status_for_frontend(session_id)
        print(f"📊 [STATUS API] Returning status: {status_data}")
        return status_data
    except Exception as e:
        print(f"❌ [STATUS API] Error retrieving status for {session_id}: {str(e)}")
        raise HTTPException(500, f"Error retrieving status: {str(e)}")

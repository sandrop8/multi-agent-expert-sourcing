"""
CV API endpoints following RESTful principles
"""

from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks, status
from schemas.cv_schemas import CVUploadResponse, CVListItem
from services.cv_service import CVService
from services.cv_status_service import get_status_for_frontend

# RESTful resource-based router for CVs
router = APIRouter(prefix="/cvs", tags=["cvs"])

# Processing sessions router for CV processing status
processing_router = APIRouter(prefix="/cv-processing-sessions", tags=["cv-processing"])


@router.post("/", response_model=CVUploadResponse, status_code=status.HTTP_201_CREATED)
async def create_cv(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Create a new CV resource by uploading a file.

    Follows RESTful principle: POST /cvs creates a new CV resource.
    Returns 201 Created on successful resource creation.
    """
    cv_service = CVService()
    return await cv_service.upload_cv(file, background_tasks)


@router.get("/", response_model=List[CVListItem])
async def list_cvs():
    """Retrieve list of CV resources.

    Follows RESTful principle: GET /cvs retrieves collection of CV resources.
    """
    cv_service = CVService()
    return cv_service.list_cvs()


@processing_router.get("/{session_id}")
async def get_processing_session(session_id: str):
    """Retrieve CV processing session status by ID.

    Follows RESTful principle: GET /cv-processing-sessions/{id} retrieves specific resource.
    """
    try:
        print(f"🔍 [PROCESSING API] Received request for session: {session_id}")
        status_data = get_status_for_frontend(session_id)
        print(f"📊 [PROCESSING API] Returning status: {status_data}")
        return status_data
    except Exception as e:
        print(f"❌ [PROCESSING API] Error retrieving status for {session_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving processing session: {str(e)}",
        )


# Export both routers for import in main.py
__all__ = [
    "router",
    "processing_router",
    "create_cv",
    "list_cvs",
    "get_processing_session",
]

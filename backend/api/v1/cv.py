"""
CV API endpoints
"""

from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File
from schemas.cv_schemas import CVUploadResponse, CVListItem
from services.cv_service import CVService

router = APIRouter(prefix="/cv", tags=["cv"])

@router.post("/upload", response_model=CVUploadResponse)
async def upload_cv(file: UploadFile = File(...)):
    """Handle CV file uploads, store them in Postgres, and process with agent system."""
    cv_service = CVService()
    return await cv_service.upload_cv(file)

@router.get("/list", response_model=List[CVListItem])
async def list_cvs():
    """Get list of uploaded CVs (for testing/debugging)."""
    cv_service = CVService()
    return cv_service.list_cvs() 
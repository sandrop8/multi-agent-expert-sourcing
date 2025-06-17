"""
CV service - business logic for CV upload and processing
"""

from typing import List
from fastapi import HTTPException, UploadFile, BackgroundTasks
import sqlalchemy as sa
from app_agents.cv_agents import process_cv_workflow
from models.base import get_engine
from models.cv_models import cvs
from schemas.cv_schemas import CVUploadResponse, CVListItem
from core.config import ALLOWED_FILE_TYPES, MAX_FILE_SIZE
from services.cv_status_service import (
    generate_session_id,
    log_status_update,
    CVProcessingStage,
)


class CVService:
    """Service class for CV-related business logic"""

    def __init__(self):
        self.engine = get_engine()

    async def upload_cv(
        self, file: UploadFile, background_tasks: BackgroundTasks
    ) -> CVUploadResponse:
        """
        Handle CV file upload, validation, and processing with status updates.
        The actual processing is run in a background task.
        """

        # Generate session ID for status tracking
        session_id = generate_session_id(file.filename or "")

        # IMMEDIATELY create initial status to prevent "session not found" errors
        log_status_update(
            session_id,
            CVProcessingStage.UPLOAD_STARTED,
            f"Starting upload for {file.filename}",
        )
        print(f"📊 [SERVICE] Initial status created for session: {session_id}")

        try:
            # Validate file type
            if file.content_type not in ALLOWED_FILE_TYPES:
                log_status_update(
                    session_id, CVProcessingStage.ERROR, "Invalid file type"
                )
                raise HTTPException(400, "Only PDF and Word documents are allowed")

            # Validate file size
            file_content = await file.read()
            if len(file_content) > MAX_FILE_SIZE:
                log_status_update(session_id, CVProcessingStage.ERROR, "File too large")
                raise HTTPException(400, "File size exceeds 10MB limit")

            print(
                f"📁 Processing CV upload: {file.filename} ({len(file_content)} bytes) - Session: {session_id}"
            )

            # Status Update: File validation passed
            log_status_update(
                session_id,
                CVProcessingStage.FILE_PREPARATION,
                f"File validated: {file.filename}",
            )

            # Store file in database
            with self.engine.begin() as conn:
                result = conn.execute(
                    cvs.insert(),
                    [
                        {
                            "filename": file.filename,
                            "original_filename": file.filename,
                            "file_size": len(file_content),
                            "content_type": file.content_type,
                            "file_data": file_content,
                            "processed": False,
                        }
                    ],
                )

            print("💾 CV stored successfully in database")

            # Get the CV ID from the inserted record
            cv_id = result.inserted_primary_key[0]
            print(f"📁 Processing stored CV with ID: {cv_id}")

            # Schedule the long-running CV processing in the background
            background_tasks.add_task(
                process_cv_workflow, f"stored_cv_id:{cv_id}", session_id
            )
            print(
                f"🤖 Scheduled CV processing workflow in background - Session: {session_id}"
            )

            # Immediately return a response to the client
            return CVUploadResponse(
                message="CV upload started. Our AI will now analyze it.",
                filename=file.filename,
                size=len(file_content),
                agent_feedback="Processing has started. You will receive feedback soon.",
                processing_status="processing_started",
                session_id=session_id,
            )

        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ Error in upload: {str(e)}")
            log_status_update(
                session_id, CVProcessingStage.ERROR, f"Upload failed: {str(e)}"
            )
            raise HTTPException(500, f"Upload failed: {str(e)}")

    def list_cvs(self) -> List[CVListItem]:
        """Get list of uploaded CVs"""
        try:
            with self.engine.connect() as conn:
                rows = conn.execute(
                    sa.select(
                        cvs.c.id,
                        cvs.c.filename,
                        cvs.c.file_size,
                        cvs.c.content_type,
                        cvs.c.uploaded_at,
                        cvs.c.processed,
                    ).order_by(cvs.c.uploaded_at.desc())
                )
                return [CVListItem(**dict(r._mapping)) for r in rows]
        except Exception as e:
            print(f"❌ Error listing CVs: {str(e)}")
            raise HTTPException(500, str(e))

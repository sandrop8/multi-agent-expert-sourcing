"""
CV service - business logic for CV upload and processing
"""

from typing import List
from fastapi import HTTPException, UploadFile
import sqlalchemy as sa
from agents import Runner
from app_agents.cv_agents import freelancer_profile_manager
from models.base import get_engine
from models.cv_models import cvs
from schemas.cv_schemas import CVUploadResponse, CVListItem
from core.config import ALLOWED_FILE_TYPES, MAX_FILE_SIZE

class CVService:
    """Service class for CV-related business logic"""
    
    def __init__(self):
        self.engine = get_engine()
    
    async def upload_cv(self, file: UploadFile) -> CVUploadResponse:
        """Handle CV file upload, validation, and processing"""
        try:
            # Validate file type
            if file.content_type not in ALLOWED_FILE_TYPES:
                raise HTTPException(400, "Only PDF and Word documents are allowed")
            
            # Validate file size
            file_content = await file.read()
            if len(file_content) > MAX_FILE_SIZE:
                raise HTTPException(400, "File size exceeds 10MB limit")
            
            print(f"📁 Processing CV upload: {file.filename} ({len(file_content)} bytes)")

            # Store file in database
            with self.engine.begin() as conn:
                result = conn.execute(cvs.insert(), [{
                    "filename": file.filename,
                    "original_filename": file.filename,
                    "file_size": len(file_content),
                    "content_type": file.content_type,
                    "file_data": file_content,
                    "processed": False
                }])
                
            print(f"💾 CV stored successfully in database")
            
            # Process CV with freelancer agent system
            try:
                print(f"🤖 Processing CV with freelancer agent system...")
                cv_description = f"CV file uploaded: {file.filename} ({file.content_type}, {len(file_content)} bytes). Please analyze this CV upload and coordinate the profile creation workflow."
                
                # Use freelancer_profile_manager as entry point to CV processing system
                result = await Runner.run(freelancer_profile_manager, cv_description)
                
                agent_response = result.final_output if result.final_output else "CV processed successfully"
                print(f"✅ Agent Response: {agent_response}")
                
                # CV was successfully processed by agents - confirmed as valid CV
                return CVUploadResponse(
                    message="CV uploaded successfully! Our AI will analyze it and provide feedback soon.",
                    filename=file.filename,
                    size=len(file_content),
                    agent_feedback=agent_response,
                    processing_status="validated"
                )
                
            except Exception as agent_error:
                print(f"⚠️ Agent processing error: {str(agent_error)}")
                # Handle agent errors gracefully - file is still stored
                if "guardrail" in str(agent_error).lower():
                    return CVUploadResponse(
                        message="File uploaded successfully, but we're still analyzing if it's a proper CV. We'll provide feedback soon.",
                        filename=file.filename,
                        size=len(file_content),
                        agent_feedback="Our AI is analyzing the content to determine if this is a professional CV/resume.",
                        processing_status="analyzing"
                    )
                else:
                    return CVUploadResponse(
                        message="File uploaded successfully, but our AI analysis encountered an issue. We'll review it manually.",
                        filename=file.filename,
                        size=len(file_content),
                        agent_feedback="Automated processing encountered an issue, but your file has been saved for manual review.",
                        processing_status="manual_review"
                    )
        
        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ Error in upload: {str(e)}")
            raise HTTPException(500, f"Upload failed: {str(e)}")
    
    def list_cvs(self) -> List[CVListItem]:
        """Get list of uploaded CVs"""
        try:
            with self.engine.connect() as conn:
                rows = conn.execute(
                    sa.select(
                        cvs.c.id, cvs.c.filename, cvs.c.file_size, 
                        cvs.c.content_type, cvs.c.uploaded_at, cvs.c.processed
                    ).order_by(cvs.c.uploaded_at.desc())
                )
                return [CVListItem(**dict(r._mapping)) for r in rows]
        except Exception as e:
            print(f"❌ Error listing CVs: {str(e)}")
            raise HTTPException(500, str(e)) 
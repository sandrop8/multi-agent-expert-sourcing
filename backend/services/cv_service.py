"""
CV service - business logic for CV upload and processing
"""

import os
import tempfile
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
            
            # Process CV with freelancer agent system using stored file data
            try:
                print(f"🤖 Processing CV with freelancer agent system using stored file...")
                
                # Get the CV ID from the inserted record
                cv_id = result.inserted_primary_key[0]
                print(f"📁 Processing stored CV with ID: {cv_id}")
                
                try:
                    # Use freelancer_profile_manager with the stored CV ID
                    result = await Runner.run(freelancer_profile_manager, f"stored_cv_id:{cv_id}")
                    
                    agent_response = result.final_output if result.final_output else "CV processed successfully"
                    print(f"✅ Agent Response: {agent_response}")
                    
                    # CV was successfully processed by agents - confirmed as valid CV
                    return CVUploadResponse(
                        message="CV uploaded and analyzed successfully! Our AI has processed your CV.",
                        filename=file.filename,
                        size=len(file_content),
                        agent_feedback=str(agent_response) if agent_response else "CV processed successfully",
                        processing_status="completed"
                    )
                    
                except Exception as agent_error:
                    print(f"⚠️ Agent processing error: {str(agent_error)}")
                    # Handle agent errors gracefully - file is still stored
                    if "guardrail" in str(agent_error).lower() or "tripwire" in str(agent_error).lower():
                        return CVUploadResponse(
                            message="File uploaded successfully, but our AI determined this may not be a standard CV format. We'll review it manually.",
                            filename=file.filename,
                            size=len(file_content),
                            agent_feedback="Our AI analysis suggests this document may not follow standard CV/resume format. Manual review recommended.",
                            processing_status="needs_review"
                        )
                    else:
                        return CVUploadResponse(
                            message="File uploaded successfully, but our AI analysis encountered an issue. We'll review it manually.",
                            filename=file.filename,
                            size=len(file_content),
                            agent_feedback=f"AI processing error: {str(agent_error)[:200]}...",
                            processing_status="manual_review"
                        )
                except Exception as agent_processing_error:
                    print(f"❌ Error in agent processing: {str(agent_processing_error)}")
                    raise HTTPException(500, f"Agent processing failed: {str(agent_processing_error)}")
            
            except Exception as processing_error:
                print(f"❌ Error in CV processing: {str(processing_error)}")
                raise HTTPException(500, f"CV processing failed: {str(processing_error)}")
        
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
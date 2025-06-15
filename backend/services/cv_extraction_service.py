"""
CV Extraction Tools - OpenAI Agents SDK Function Tools
Provides CV extraction as tools that agents can call using OpenAI's responses API
"""

import json
import os
import tempfile
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from pydantic import BaseModel
from agents import function_tool, RunContextWrapper
import sqlalchemy as sa
from models.base import get_engine
from models.cv_models import cvs

class CVTextExtractionResult(BaseModel):
    """Result from CV text extraction tool"""
    extracted_text: str
    confidence_score: float
    extraction_notes: list[str]
    processing_status: str

def get_stored_cv_file_path(cv_identifier: str) -> str:
    """
    Get file path for a stored CV by creating a temporary file from stored data.
    
    Args:
        cv_identifier: Either a file path or stored_cv_id:123 format
        
    Returns:
        File path to use for processing
    """
    if cv_identifier.startswith("stored_cv_id:"):
        cv_id = int(cv_identifier.split(":")[1])
        
        # Retrieve CV data from database
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(
                sa.select(cvs.c.file_data, cvs.c.original_filename, cvs.c.content_type)
                .where(cvs.c.id == cv_id)
            ).first()
            
            if not result:
                raise FileNotFoundError(f"Stored CV with ID {cv_id} not found")
            
            # Create temporary file from stored data
            file_extension = os.path.splitext(result.original_filename)[1]
            with tempfile.NamedTemporaryFile(mode='wb', suffix=file_extension, delete=False) as temp_file:
                temp_file.write(result.file_data)
                temp_file_path = temp_file.name
                
            print(f"📁 Created temporary file from stored CV ID {cv_id}: {temp_file_path}")
            return temp_file_path
    else:
        # Regular file path - return as is
        return cv_identifier

@function_tool
async def extract_cv_text_with_responses_api(
    ctx: RunContextWrapper[Any], 
    pdf_file_path: str,
    extraction_focus: str = "comprehensive"
) -> str:
    """Extract text content from a CV/resume using OpenAI's official PDF processing.
    
    This tool follows the official OpenAI documentation for PDF file processing
    by uploading directly to the Files API and using the file_id.
    
    Args:
        ctx: Agent runtime context
        pdf_file_path: Path to the PDF file to process or stored_cv_id:123
        extraction_focus: Type of extraction - 'validation', 'summary', or 'comprehensive'
        
    Returns:
        JSON string with extracted CV information
    """
    
    temp_file_path = None
    try:
        # Initialize OpenAI client
        client = AsyncOpenAI()
        
        print(f"🔍 Processing CV with OpenAI Files API - focus: {extraction_focus}")
        print(f"📁 File identifier: {pdf_file_path}")
        
        # Get actual file path (handles both regular paths and stored CV IDs)
        actual_file_path = get_stored_cv_file_path(pdf_file_path)
        if pdf_file_path.startswith("stored_cv_id:"):
            temp_file_path = actual_file_path  # Track for cleanup
        
        # Check if file exists before processing
        if not os.path.exists(actual_file_path):
            raise FileNotFoundError(f"CV file not found: {actual_file_path}")
            
        # Upload the PDF file to OpenAI Files API (official method)
        print(f"📤 Uploading file to OpenAI Files API...")
        with open(actual_file_path, "rb") as file:
            uploaded_file = await client.files.create(
                file=file,
                purpose="assistants"  # Official purpose for file processing
            )
        
        print(f"✅ File uploaded successfully with ID: {uploaded_file.id}")
        
        # Define extraction prompts based on focus
        prompts = {
            "validation": """
            Analyze this document and determine if it's a CV/resume. Provide:
            1. Is this a CV/resume? (yes/no)
            2. Confidence level (0-1)
            3. Document type if not a CV
            4. Brief reasoning
            
            Return as JSON: {"is_cv": boolean, "confidence": float, "document_type": "string", "reasoning": "string"}
            """,
            
            "summary": """
            Extract key summary information from this CV:
            1. Full name
            2. Professional title/role
            3. Years of experience
            4. Top 3 skills
            5. Current/most recent position
            
            Return as JSON with these fields.
            """,
            
            "comprehensive": """
            Extract comprehensive CV information in this JSON structure. 
            Use empty strings for missing text fields, empty arrays for missing lists:
            
            {
                "personal_info": {
                    "full_name": "string",
                    "email": "string", 
                    "phone": "string",
                    "location": "string",
                    "linkedin": "string",
                    "portfolio": "string"
                },
                "professional_summary": "string",
                "employment_history": [
                    {
                        "company": "string",
                        "position": "string", 
                        "start_date": "string",
                        "end_date": "string",
                        "description": "string",
                        "achievements": ["string"]
                    }
                ],
                "education": [
                    {
                        "institution": "string",
                        "degree": "string",
                        "field": "string",
                        "graduation_date": "string",
                        "gpa": "string"
                    }
                ],
                "skills": {
                    "technical": ["string"],
                    "soft": ["string"],
                    "languages": ["string"]
                },
                "certifications": [
                    {
                        "name": "string",
                        "issuer": "string", 
                        "date": "string",
                        "expiry": "string"
                    }
                ],
                "projects": [
                    {
                        "name": "string",
                        "description": "string",
                        "technologies": ["string"],
                        "url": "string"
                    }
                ],
                "extraction_confidence": 0.95,
                "processing_notes": ["Successfully extracted CV data"]
            }
            
            IMPORTANT: Extract actual information from the CV document.
            """
        }
        
        # Get the appropriate prompt
        prompt = prompts.get(extraction_focus, prompts["comprehensive"])
        
        # Process the file with OpenAI Chat Completions API using file_id (official method)
        print(f"🤖 Processing file with Chat Completions API...")
        response = await client.chat.completions.create(
            model="gpt-4.1",  # Using gpt-4.1 as it supports file inputs
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "file",
                            "file": {
                                "file_id": uploaded_file.id,
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt,
                        },
                    ]
                }
            ]
        )
        
        print(f"✅ CV extraction completed successfully")
        
        # Clean up - delete the uploaded file from OpenAI
        try:
            await client.files.delete(uploaded_file.id)
            print(f"🗑️ OpenAI file {uploaded_file.id} deleted")
        except Exception as cleanup_error:
            print(f"⚠️ Warning: Could not delete OpenAI file: {cleanup_error}")
        
        # Clean up temporary file if it was created from stored CV
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                print(f"🗑️ Temporary file cleaned up: {temp_file_path}")
            except Exception as cleanup_error:
                print(f"⚠️ Warning: Could not clean up temporary file: {cleanup_error}")
        
        # Return the extracted text from the Chat Completions response
        extracted_content = response.choices[0].message.content
        
        # Validate response content
        if not extracted_content:
            raise ValueError("No content returned from OpenAI")
        
        # Try to parse as JSON to validate structure
        try:
            json.loads(extracted_content)
            print(f"📄 Successfully extracted and validated JSON content")
            return extracted_content
        except json.JSONDecodeError:
            print(f"⚠️ Content is not valid JSON, wrapping in structured response")
            # If not valid JSON, wrap in a structured response
            return json.dumps({
                "extracted_text": extracted_content,
                "confidence_score": 0.8,
                "extraction_notes": [f"Successfully processed with {extraction_focus} focus"],
                "processing_status": "completed"
            })
            
    except FileNotFoundError as fe:
        error_msg = f"File not found: {str(fe)}"
        print(f"❌ {error_msg}")
        
        return json.dumps({
            "extracted_text": "",
            "confidence_score": 0.0,
            "extraction_notes": [error_msg],
            "processing_status": "file_not_found"
        })
        
    except Exception as e:
        error_msg = f"CV extraction failed: {str(e)}"
        print(f"❌ {error_msg}")
        
        # Return structured error response
        return json.dumps({
            "extracted_text": "",
            "confidence_score": 0.0,
            "extraction_notes": [error_msg],
            "processing_status": "failed"
        })

@function_tool
async def prepare_cv_file_for_processing(
    ctx: RunContextWrapper[Any],
    uploaded_file_path: str
) -> str:
    """Prepare an uploaded CV file for OpenAI processing.
    
    This tool validates the file and returns the file path for processing.
    
    Args:
        ctx: Agent runtime context
        uploaded_file_path: Path to the uploaded CV file or stored_cv_id:123
        
    Returns:
        JSON string with file preparation status
    """
    
    try:
        print(f"📋 Preparing CV file for processing: {uploaded_file_path}")
        
        # Get actual file path (handles both regular paths and stored CV IDs)
        actual_file_path = get_stored_cv_file_path(uploaded_file_path)
        
        # Check if file exists
        if not os.path.exists(actual_file_path):
            raise FileNotFoundError(f"File not found: {actual_file_path}")
            
        # Get file size
        file_size = os.path.getsize(actual_file_path)
        
        # Check file extension
        file_ext = os.path.splitext(actual_file_path)[1].lower()
        supported_formats = ['.pdf', '.doc', '.docx']
        
        if file_ext not in supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}. Supported: {supported_formats}")
            
        print(f"✅ File validated: {uploaded_file_path} ({file_size} bytes, {file_ext})")
        
        return json.dumps({
            "file_path": uploaded_file_path,
            "file_size": file_size,
            "file_format": file_ext,
            "status": "ready_for_processing",
            "processing_notes": [f"File validated and ready for OpenAI processing - {file_size} bytes"]
        })
        
    except Exception as e:
        error_msg = f"File preparation failed: {str(e)}"
        print(f"❌ {error_msg}")
        
        return json.dumps({
            "file_path": "",
            "file_size": 0,
            "file_format": "",
            "status": "preparation_failed", 
            "processing_notes": [error_msg]
        })

# For testing the tools directly
async def test_cv_extraction_tools():
    """Test function for the CV extraction tools"""
    
    print("🧪 Testing CV extraction tools...")
    
    # Test file preparation
    test_file = "test-cv.pdf"
    if os.path.exists(test_file):
        print(f"📄 Testing with file: {test_file}")
        
        # Mock context for testing
        class MockContext:
            pass
        
        ctx = MockContext()
        
        # Test file preparation
        print("📋 Testing file preparation...")
        prep_result = await prepare_cv_file_for_processing(ctx, test_file)
        print(f"📋 Preparation result: {prep_result}")
        
        # Test extraction with validation focus (smaller/faster)
        print("🔍 Testing extraction (validation focus)...")
        extraction_result = await extract_cv_text_with_responses_api(ctx, test_file, "validation")
        print(f"🔍 Extraction result: {extraction_result}")
        
    else:
        print(f"⚠️ Test file {test_file} not found - create a test CV file for testing")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_cv_extraction_tools()) 
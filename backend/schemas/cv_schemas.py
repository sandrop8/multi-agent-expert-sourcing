"""
CV-related Pydantic schemas for API requests and responses
"""

import datetime as dt
from pydantic import BaseModel
from typing import Optional


# ---- Agent Output Schemas --------------------------------------------------
class CVValidationOutput(BaseModel):
    """Output schema for CV validation guardrail"""

    is_valid_cv: bool
    reasoning: str


# ---- Response Schemas ------------------------------------------------------
class CVUploadResponse(BaseModel):
    """Response schema for CV upload endpoint"""

    message: str
    filename: str
    size: int
    agent_feedback: str
    processing_status: str
    session_id: Optional[str] = None


class CVListItem(BaseModel):
    """Schema for CV list items"""

    id: int
    filename: str
    file_size: int
    content_type: str
    uploaded_at: dt.datetime
    processed: bool


# TODO: Phase 2 - Add comprehensive CV content schemas
# - CVPersonalInfoSchema, CVEmploymentSchema, CVSkillSchema, etc.
# - These will support the new ORM models

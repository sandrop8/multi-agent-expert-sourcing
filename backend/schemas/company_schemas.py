"""
Pydantic schemas for Company Registration API
"""

from pydantic import BaseModel
from typing import Optional


class CompanyRegistrationRequest(BaseModel):
    """Request model for company registration endpoint"""

    website_url: str
    linkedin_url: Optional[str] = None

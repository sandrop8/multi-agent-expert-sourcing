"""
Chat-related Pydantic schemas for API requests and responses
"""

import datetime as dt
from pydantic import BaseModel


# ---- Request Schemas -------------------------------------------------------
class ChatReq(BaseModel):
    """Request schema for chat endpoint"""

    prompt: str


# ---- Response Schemas ------------------------------------------------------
class Msg(BaseModel):
    """Message schema for chat history"""

    id: int
    role: str
    content: str
    ts: dt.datetime


# ---- Agent Output Schemas --------------------------------------------------
class ExpertSourcingOutput(BaseModel):
    """Output schema for expert sourcing guardrail"""

    is_expert_sourcing: bool
    reasoning: str

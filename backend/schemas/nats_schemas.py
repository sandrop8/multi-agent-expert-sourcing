"""
Pydantic schemas for NATS messaging events
Following project schema patterns for type safety and validation
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class BaseNATSEvent(BaseModel):
    """Base schema for all NATS events"""

    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    event_type: str


class CVUploadedEvent(BaseNATSEvent):
    """CV upload event schema"""

    event_type: str = "cv.uploaded"
    cv_id: int
    filename: str
    user_id: Optional[str] = None
    file_size: Optional[int] = None


class CVProcessingEvent(BaseNATSEvent):
    """CV processing status event schema"""

    cv_id: int
    session_id: str
    status: str = Field(..., description="processing, completed, or failed")


class CVProcessingStartedEvent(CVProcessingEvent):
    """CV processing started event"""

    event_type: str = "cv.processing.started"
    status: str = "processing"


class CVProcessingCompletedEvent(CVProcessingEvent):
    """CV processing completed event"""

    event_type: str = "cv.processing.completed"
    success: bool
    error_message: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None


class ChatMessageEvent(BaseNATSEvent):
    """Chat message created event schema"""

    event_type: str = "chat.message.created"
    message_id: int
    role: str = Field(..., description="user, assistant, or system")
    content: str = Field(..., max_length=1000, description="Truncated message content")
    conversation_id: Optional[str] = None


class AgentTaskEvent(BaseNATSEvent):
    """Agent task coordination event schema"""

    agent_id: str
    task_id: str
    task_type: str


class AgentTaskStartedEvent(AgentTaskEvent):
    """Agent task started event"""

    event_type: str = "agent.task.started"
    task_data: Dict[str, Any]


class AgentTaskCompletedEvent(AgentTaskEvent):
    """Agent task completed event"""

    event_type: str = "agent.task.completed"
    result: Dict[str, Any]
    success: bool = True
    processing_time_ms: Optional[int] = None


class HealthCheckEvent(BaseNATSEvent):
    """Health check event schema"""

    event_type: str = "system.health.check"
    service_name: str
    status: str = Field(..., description="healthy, degraded, or unhealthy")
    details: Optional[Dict[str, Any]] = None


# Request-Response schemas for NATS RPC patterns
class NATSRequest(BaseModel):
    """Base request schema for NATS RPC"""

    request_id: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    timeout_seconds: Optional[float] = 5.0


class NATSResponse(BaseModel):
    """Base response schema for NATS RPC"""

    request_id: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class CVAnalysisRequest(NATSRequest):
    """Request CV analysis via NATS"""

    cv_id: int
    analysis_type: str = Field(
        default="full", description="full, quick, or extract_only"
    )


class CVAnalysisResponse(NATSResponse):
    """CV analysis response"""

    cv_id: int
    analysis_result: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None


# Event publishing helper schemas
class EventPublishRequest(BaseModel):
    """Request to publish an event"""

    subject: str = Field(..., description="NATS subject")
    event_data: Dict[str, Any]
    persistent: bool = False


class EventPublishResponse(BaseModel):
    """Response from event publishing"""

    success: bool
    subject: str
    message: Optional[str] = None

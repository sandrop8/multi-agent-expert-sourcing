"""
NATS messaging API endpoints
Following project API patterns for RESTful design
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
import logging
from nats.aio.client import Client as NATS

from core.nats import get_nats, get_jetstream, get_nats_safe
from services.nats_service import NATSService, EventPublisher
from schemas.nats_schemas import EventPublishRequest, EventPublishResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/nats", tags=["nats"])


@router.get("/health")
async def nats_health_check(nats_client: Optional[NATS] = Depends(get_nats_safe)):
    """Check NATS connection health"""
    try:
        if nats_client is None or not nats_client.is_connected:
            return {
                "status": "disconnected",
                "connected": False,
                "message": "NATS client not initialized or connection failed during startup.",
                "server_info": None,
            }

        # If connected, try a simple connectivity test
        await nats_client.publish("health.ping", b"ping")

        return {
            "status": "healthy",
            "connected": True,
            "server_info": {
                "connected_url": str(nats_client.connected_url)
                if nats_client.connected_url
                else None,
                "is_connected": nats_client.is_connected,
            },
        }
    except Exception as e:
        logger.error(f"NATS health check failed: {e}")
        is_connected = nats_client.is_connected if nats_client else False
        return {
            "status": "error",
            "connected": is_connected,
            "message": f"NATS health check failed: {str(e)}",
            "server_info": None,
        }


@router.post("/publish", response_model=EventPublishResponse)
async def publish_event(request: EventPublishRequest, nats_client=Depends(get_nats)):
    """
    Publish an event to NATS
    Useful for testing and manual event triggering
    """
    try:
        nats_service = NATSService(nats_client)

        success = await nats_service.publish_event(
            subject=request.subject,
            data=request.event_data,
            persistent=request.persistent,
        )

        if success:
            return EventPublishResponse(
                success=True,
                subject=request.subject,
                message=f"Event published to {request.subject}",
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to publish event")

    except Exception as e:
        logger.error(f"Failed to publish event: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/cv-uploaded")
async def publish_cv_uploaded_event(
    cv_id: int, filename: str, nats_client=Depends(get_nats)
):
    """Test CV uploaded event publishing"""
    try:
        nats_service = NATSService(nats_client)
        event_publisher = EventPublisher(nats_service)

        success = await event_publisher.cv_uploaded(
            cv_id=cv_id, filename=filename, user_id="test_user"
        )

        if success:
            return {
                "message": f"CV uploaded event published for CV {cv_id}",
                "event_subject": "events.cv.uploaded",
            }
        else:
            raise HTTPException(
                status_code=500, detail="Failed to publish CV uploaded event"
            )

    except Exception as e:
        logger.error(f"Failed to publish CV uploaded event: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/chat-message")
async def publish_chat_message_event(
    message_id: int, role: str, content: str, nats_client=Depends(get_nats)
):
    """Test chat message event publishing"""
    try:
        nats_service = NATSService(nats_client)
        event_publisher = EventPublisher(nats_service)

        success = await event_publisher.chat_message_created(
            message_id=message_id, role=role, content=content
        )

        if success:
            return {
                "message": f"Chat message event published for message {message_id}",
                "event_subject": "events.chat.message.created",
            }
        else:
            raise HTTPException(
                status_code=500, detail="Failed to publish chat message event"
            )

    except Exception as e:
        logger.error(f"Failed to publish chat message event: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/agent-task")
async def publish_agent_task_event(
    agent_id: str, task_id: str, result: Dict[str, Any], nats_client=Depends(get_nats)
):
    """Test agent task completion event"""
    try:
        nats_service = NATSService(nats_client)
        event_publisher = EventPublisher(nats_service)

        success = await event_publisher.agent_task_completed(
            agent_id=agent_id, task_id=task_id, result=result
        )

        if success:
            return {
                "message": f"Agent task completion event published for {agent_id}",
                "event_subject": f"agent.task.completed.{agent_id}",
            }
        else:
            raise HTTPException(
                status_code=500, detail="Failed to publish agent task event"
            )

    except Exception as e:
        logger.error(f"Failed to publish agent task event: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test/request-response")
async def demo_request_response(
    test_data: str = "Hello NATS!", nats_client=Depends(get_nats)
):
    """Test NATS request-response pattern"""
    try:
        nats_service = NATSService(nats_client)

        # This will timeout unless there's a responder
        response = await nats_service.request_response(
            subject="test.echo", data={"message": test_data}, timeout=2.0
        )

        if response:
            return {
                "message": "Request-response test successful",
                "request": test_data,
                "response": response,
            }
        else:
            return {
                "message": "No responder available for test.echo",
                "note": "This is expected if no service is listening on 'test.echo' subject",
            }

    except Exception as e:
        logger.error(f"Request-response test failed: {e}")
        return {
            "message": "Request-response test failed",
            "error": str(e),
            "note": "This is expected if NATS server is not running",
        }


@router.get("/streams")
async def list_jetstream_streams(jetstream=Depends(get_jetstream)):
    """List JetStream streams (for debugging)"""
    try:
        if jetstream is None:
            return {
                "message": "JetStream is not available on this NATS server",
                "streams": [],
                "note": "JetStream may not be enabled on the server. Core NATS functionality is still available.",
            }

        # This is a simplified version - real implementation would use JS management API
        return {
            "message": "JetStream is available",
            "streams": [
                "EVENTS (events.>)",
                "AGENT_TASKS (agent.task.>)",
                "CV_PROCESSING (cv.processing.>)",
            ],
            "note": "Streams are auto-created when first used",
        }
    except Exception as e:
        logger.error(f"Failed to check JetStream: {e}")
        return {
            "message": "JetStream status unknown",
            "streams": [],
            "note": f"Error checking JetStream: {str(e)}",
        }


# Background event subscriber example
async def setup_event_subscribers(nats_client):
    """
    Setup background event subscribers
    This would typically be called during app startup
    """
    nats_service = NATSService(nats_client)

    # Example: Subscribe to CV events
    async def handle_cv_events(subject: str, data: Dict[str, Any], msg):
        logger.info(f"🎯 Received CV event on {subject}: {data}")
        # Add your CV event handling logic here

    # Example: Subscribe to chat events
    async def handle_chat_events(subject: str, data: Dict[str, Any], msg):
        logger.info(f"💬 Received chat event on {subject}: {data}")
        # Add your chat event handling logic here

    # Subscribe to events
    await nats_service.subscribe_to_events("events.cv.*", handle_cv_events)
    await nats_service.subscribe_to_events("events.chat.*", handle_chat_events)

    logger.info("📡 NATS event subscribers setup complete")

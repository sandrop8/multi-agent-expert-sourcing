"""
Example integration of NATS with existing CV service
Shows how to add event publishing to existing workflows
"""

import logging
from typing import Optional

from services.nats_service import EventPublisher, NATSService
from core.nats import get_nats

logger = logging.getLogger(__name__)


class CVEventIntegration:
    """
    Integration layer to add NATS events to CV processing workflows
    This shows how to retrofit existing services with event publishing
    """

    def __init__(self):
        self.event_publisher: Optional[EventPublisher] = None

    async def _get_event_publisher(self) -> Optional[EventPublisher]:
        """Get event publisher, handling NATS unavailability gracefully"""
        if self.event_publisher is None:
            try:
                nats_client = await get_nats()
                nats_service = NATSService(nats_client)
                self.event_publisher = EventPublisher(nats_service)
            except Exception as e:
                logger.warning(f"NATS not available for events: {e}")
                return None

        return self.event_publisher

    async def on_cv_uploaded(
        self, cv_id: int, filename: str, user_id: Optional[str] = None
    ) -> None:
        """
        Called when a CV is uploaded - publishes event
        This can be integrated into existing CV upload workflow
        """
        try:
            publisher = await self._get_event_publisher()
            if publisher:
                success = await publisher.cv_uploaded(
                    cv_id=cv_id, filename=filename, user_id=user_id
                )
                if success:
                    logger.info(f"📤 Published CV uploaded event for CV {cv_id}")
                else:
                    logger.warning(
                        f"Failed to publish CV uploaded event for CV {cv_id}"
                    )
        except Exception as e:
            logger.error(f"Error publishing CV uploaded event: {e}")

    async def on_cv_processing_started(self, cv_id: int, session_id: str) -> None:
        """Called when CV processing starts"""
        try:
            publisher = await self._get_event_publisher()
            if publisher:
                success = await publisher.cv_processing_started(cv_id, session_id)
                if success:
                    logger.info(
                        f"📤 Published CV processing started event for CV {cv_id}"
                    )
        except Exception as e:
            logger.error(f"Error publishing CV processing started event: {e}")

    async def on_cv_processing_completed(
        self, cv_id: int, session_id: str, success: bool
    ) -> None:
        """Called when CV processing completes"""
        try:
            publisher = await self._get_event_publisher()
            if publisher:
                event_success = await publisher.cv_processing_completed(
                    cv_id, session_id, success
                )
                if event_success:
                    logger.info(
                        f"📤 Published CV processing completed event for CV {cv_id}"
                    )
        except Exception as e:
            logger.error(f"Error publishing CV processing completed event: {e}")

    async def on_chat_message_created(
        self, message_id: int, role: str, content: str
    ) -> None:
        """Called when a chat message is created"""
        try:
            publisher = await self._get_event_publisher()
            if publisher:
                success = await publisher.chat_message_created(
                    message_id, role, content
                )
                if success:
                    logger.info(
                        f"📤 Published chat message event for message {message_id}"
                    )
        except Exception as e:
            logger.error(f"Error publishing chat message event: {e}")


# Global instance for easy integration
cv_events = CVEventIntegration()


# Example of how to integrate with existing services:
"""
In your existing CV service, you would add calls like this:

# In cv_service.py - after successful CV upload:
from services.cv_nats_integration import cv_events

class CVService:
    async def upload_cv(self, file: UploadFile, background_tasks: BackgroundTasks):
        # ... existing upload logic ...

        # Add event publishing
        background_tasks.add_task(
            cv_events.on_cv_uploaded,
            cv_file.id,
            cv_file.filename,
            "user_123"  # or get actual user ID
        )

        return response

# In cv processing logic - when processing starts:
await cv_events.on_cv_processing_started(cv_id, session_id)

# In cv processing logic - when processing completes:
await cv_events.on_cv_processing_completed(cv_id, session_id, success=True)

# In chat service - when message is created:
await cv_events.on_chat_message_created(message.id, message.role, message.content)
"""

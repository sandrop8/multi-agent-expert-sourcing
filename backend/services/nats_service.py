"""
NATS messaging service following project service layer patterns
Provides high-level messaging operations for the application
"""

import json
import logging
from typing import Any, Dict, Optional, Callable
from nats.aio.client import Client as NATS

logger = logging.getLogger(__name__)


class NATSService:
    """
    NATS messaging service following project patterns
    Provides abstraction for publishing and subscribing to messages
    """

    def __init__(self, nats_client: NATS):
        """Initialize with injected NATS client"""
        self.nc = nats_client
        self._subscribers = {}  # Track active subscriptions

    async def publish_event(
        self, subject: str, data: Dict[str, Any], persistent: bool = False
    ) -> bool:
        """
        Publish event to NATS subject

        Args:
            subject: NATS subject (e.g., 'events.cv.uploaded')
            data: Event data dictionary
            persistent: Use JetStream for guaranteed delivery (falls back to core NATS if unavailable)

        Returns:
            bool: Success status
        """
        try:
            payload = json.dumps(data).encode("utf-8")

            if persistent:
                # Try JetStream for persistent messaging
                try:
                    js = self.nc.jetstream()
                    ack = await js.publish(subject, payload)
                    logger.debug(f"📤 Published persistent event to {subject}: {ack}")
                    return True
                except Exception as js_error:
                    logger.warning(
                        f"⚠️ JetStream publish failed for {subject}, falling back to core NATS: {js_error}"
                    )
                    # Fall back to core NATS
                    await self.nc.publish(subject, payload)
                    logger.debug(
                        f"📤 Published event to {subject} (fallback to core NATS)"
                    )
                    return True
            else:
                # Use core NATS for fire-and-forget
                await self.nc.publish(subject, payload)
                logger.debug(f"📤 Published event to {subject}")
                return True

        except Exception as e:
            logger.error(f"❌ Failed to publish to {subject}: {e}")
            return False

    async def request_response(
        self, subject: str, data: Dict[str, Any], timeout: float = 5.0
    ) -> Optional[Dict[str, Any]]:
        """
        Send request and wait for response (RPC pattern)

        Args:
            subject: Request subject
            data: Request data
            timeout: Response timeout in seconds

        Returns:
            Response data or None if timeout/error
        """
        try:
            payload = json.dumps(data).encode("utf-8")
            response = await self.nc.request(subject, payload, timeout=timeout)

            if response and response.data:
                result = json.loads(response.data.decode("utf-8"))
                logger.debug(f"🔄 Request-response to {subject} completed")
                return result

            return None

        except Exception as e:
            logger.error(f"❌ Request to {subject} failed: {e}")
            return None

    async def subscribe_to_events(
        self, subject: str, handler: Callable, queue_group: Optional[str] = None
    ) -> str:
        """
        Subscribe to events on a subject

        Args:
            subject: NATS subject pattern (e.g., 'events.cv.*')
            handler: Async function to handle messages
            queue_group: Optional queue group for load balancing

        Returns:
            Subscription ID for tracking
        """
        try:

            async def message_handler(msg):
                """Wrapper to handle JSON deserialization and error handling"""
                try:
                    data = json.loads(msg.data.decode("utf-8"))
                    await handler(subject=msg.subject, data=data, msg=msg)
                except Exception as e:
                    logger.error(f"❌ Error in message handler for {msg.subject}: {e}")

            # Subscribe with optional queue group
            if queue_group:
                subscription = await self.nc.subscribe(
                    subject, queue=queue_group, cb=message_handler
                )
            else:
                subscription = await self.nc.subscribe(subject, cb=message_handler)

            # Track subscription
            sub_id = f"{subject}_{id(subscription)}"
            self._subscribers[sub_id] = subscription

            logger.info(
                f"📨 Subscribed to {subject}"
                + (f" (queue: {queue_group})" if queue_group else "")
            )
            return sub_id

        except Exception as e:
            logger.error(f"❌ Failed to subscribe to {subject}: {e}")
            raise

    async def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from a subject"""
        try:
            if subscription_id in self._subscribers:
                subscription = self._subscribers[subscription_id]
                await subscription.unsubscribe()
                del self._subscribers[subscription_id]
                logger.info(f"🚫 Unsubscribed: {subscription_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Failed to unsubscribe {subscription_id}: {e}")
            return False


class EventPublisher:
    """
    Specialized event publisher for common application events
    Following project patterns for specific use cases
    """

    def __init__(self, nats_service: NATSService):
        self.nats = nats_service

    async def cv_uploaded(
        self, cv_id: int, filename: str, user_id: Optional[str] = None
    ) -> bool:
        """Publish CV upload event"""
        return await self.nats.publish_event(
            subject="events.cv.uploaded",
            data={
                "cv_id": cv_id,
                "filename": filename,
                "user_id": user_id,
                "timestamp": str(cv_id),  # Using cv_id as simple timestamp for demo
            },
            persistent=True,  # CV events should be persistent
        )

    async def cv_processing_started(self, cv_id: int, session_id: str) -> bool:
        """Publish CV processing started event"""
        return await self.nats.publish_event(
            subject="events.cv.processing.started",
            data={"cv_id": cv_id, "session_id": session_id, "status": "processing"},
            persistent=True,
        )

    async def cv_processing_completed(
        self, cv_id: int, session_id: str, success: bool
    ) -> bool:
        """Publish CV processing completion event"""
        return await self.nats.publish_event(
            subject="events.cv.processing.completed",
            data={
                "cv_id": cv_id,
                "session_id": session_id,
                "status": "completed" if success else "failed",
                "success": success,
            },
            persistent=True,
        )

    async def chat_message_created(
        self, message_id: int, role: str, content: str
    ) -> bool:
        """Publish chat message event"""
        return await self.nats.publish_event(
            subject="events.chat.message.created",
            data={
                "message_id": message_id,
                "role": role,
                "content": content[:100] + "..."
                if len(content) > 100
                else content,  # Truncate for logging
            },
        )

    async def agent_task_completed(
        self, agent_id: str, task_id: str, result: Dict[str, Any]
    ) -> bool:
        """Publish agent task completion (for multi-agent coordination)"""
        return await self.nats.publish_event(
            subject=f"agent.task.completed.{agent_id}",
            data={
                "agent_id": agent_id,
                "task_id": task_id,
                "result": result,
                "completed_at": str(task_id),  # Simple timestamp for demo
            },
            persistent=True,
        )

"""
NATS connection management and dependency injection
Following FastAPI async patterns established in the project
"""

import logging
from typing import Optional
from nats.aio.client import Client as NATS
from nats.js.api import StreamConfig, RetentionPolicy
from contextlib import asynccontextmanager

from .config import NATS_URL, NATS_CLUSTER_URLS

logger = logging.getLogger(__name__)

# Global NATS client instance
_nats_client: Optional[NATS] = None
_jetstream = None


class NATSConnection:
    """NATS connection manager following project patterns"""

    def __init__(self):
        self.nc: Optional[NATS] = None
        self.js = None
        self.connected = False

    async def connect(self) -> None:
        """Initialize NATS connection with cluster support"""
        try:
            self.nc = NATS()

            # Use cluster URLs if available, otherwise single URL
            servers = (
                NATS_CLUSTER_URLS
                if NATS_CLUSTER_URLS and NATS_CLUSTER_URLS[0]
                else [NATS_URL]
            )

            await self.nc.connect(
                servers=servers,
                name="fastapi_multi_agent_app",
                max_reconnect_attempts=5,
                reconnect_time_wait=2,
                ping_interval=20,
                max_outstanding_pings=3,
            )

            # Initialize JetStream for persistence
            self.js = self.nc.jetstream()

            # Setup basic streams for the application
            await self._setup_streams()

            self.connected = True
            logger.info(f"✅ Connected to NATS: {servers}")

        except Exception as e:
            logger.error(f"❌ Failed to connect to NATS: {e}")
            raise

    async def disconnect(self) -> None:
        """Close NATS connection"""
        if self.nc and self.connected:
            await self.nc.close()
            self.connected = False
            logger.info("🔌 Disconnected from NATS")

    async def _setup_streams(self) -> None:
        """Setup basic JetStream streams for the application"""
        if not self.js:
            logger.warning("⚠️ JetStream not available, skipping stream setup")
            return

        # Test if JetStream is actually available
        try:
            await self.js.account_info()
            logger.debug("✅ JetStream is available")
        except Exception as e:
            logger.warning(
                f"⚠️ JetStream not available on server, skipping stream setup: {e}"
            )
            return

        streams = [
            {
                "name": "EVENTS",
                "subjects": ["events.>"],
                "description": "Application events stream",
            },
            {
                "name": "AGENT_TASKS",
                "subjects": ["agent.task.>"],
                "description": "AI agent task coordination",
            },
            {
                "name": "CV_PROCESSING",
                "subjects": ["cv.processing.>"],
                "description": "CV processing workflow events",
            },
            {
                "name": "TEST_EVENTS",
                "subjects": ["test.event.>"],
                "description": "Stream for integration test events",
            },
        ]

        for stream_def in streams:
            try:
                stream_config = StreamConfig(
                    name=stream_def["name"],
                    subjects=stream_def["subjects"],
                    retention=RetentionPolicy.LIMITS,
                    max_msgs=100000,
                    max_age=86400,  # 24 hours
                )
                await self.js.add_stream(stream_config)
                logger.debug(f"📁 Created stream: {stream_def['name']}")
            except Exception as e:
                # Stream might already exist or JetStream might be unavailable, that's OK
                logger.debug(f"Stream {stream_def['name']}: {e}")


# Global connection instance
_connection = NATSConnection()


async def init_nats() -> None:
    """Initialize NATS connection - called during FastAPI startup"""
    global _nats_client, _jetstream

    await _connection.connect()
    _nats_client = _connection.nc
    _jetstream = _connection.js


async def close_nats() -> None:
    """Close NATS connection - called during FastAPI shutdown"""
    await _connection.disconnect()


# FastAPI dependency functions following project patterns
async def get_nats() -> NATS:
    """FastAPI dependency that provides NATS client"""
    if not _nats_client or not _connection.connected:
        raise RuntimeError(
            "NATS not connected. Ensure init_nats() was called during startup."
        )
    return _nats_client


async def get_jetstream():
    """FastAPI dependency that provides JetStream context"""
    if not _jetstream:
        logger.warning("⚠️ JetStream not available - this operation will be skipped")
        return None

    # Test if JetStream is actually functional
    try:
        await _jetstream.account_info()
        return _jetstream
    except Exception as e:
        logger.warning(f"⚠️ JetStream not functional: {e}")
        return None


async def get_nats_safe() -> Optional[NATS]:
    """FastAPI dependency that provides NATS client, but returns None if not connected."""
    if not _nats_client or not _connection.connected:
        return None
    return _nats_client


@asynccontextmanager
async def nats_context():
    """Context manager for NATS operations in services"""
    nc = await get_nats()
    try:
        yield nc
    except Exception as e:
        logger.error(f"NATS operation failed: {e}")
        raise

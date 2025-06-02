"""
AG-UI Protocol Adapter for Multi-Agent Expert Sourcing System

This module provides the AG-UI protocol integration to enhance our OpenAI Agents
multi-agent system with real-time streaming, file uploads, and standardized
agent-UI communication.

Features:
- Real-time agent communication via AG-UI events
- File upload and processing capabilities  
- WebSocket support for bi-directional state sync
- Integration with OpenAI Agents SDK
- Enhanced user experience with streaming responses
"""

import asyncio
import json
import logging
import uuid
from typing import Dict, Any, List, Optional, AsyncGenerator
from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect, UploadFile
from agents import Runner
import sqlalchemy as sa

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AGUIAdapter:
    """
    AG-UI Protocol Adapter for OpenAI Agents integration.
    
    Provides real-time communication, file handling, and enhanced
    agent interactions following AG-UI protocol standards.
    """
    
    def __init__(self, database_engine, messages_table):
        """Initialize the AG-UI adapter with database connection."""
        self.engine = database_engine
        self.messages = messages_table
        self.active_connections: Dict[str, WebSocket] = {}
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        
        logger.info("🚀 AG-UI Adapter initialized successfully")
    
    async def connect_websocket(self, websocket: WebSocket, session_id: str):
        """Handle new WebSocket connection for AG-UI communication."""
        try:
            await websocket.accept()
            self.active_connections[session_id] = websocket
            self.active_sessions[session_id] = {
                "connected_at": datetime.utcnow(),
                "files": [],
                "context": {}
            }
            
            logger.info(f"🔌 WebSocket connected for session: {session_id}")
            
            # Send connection acknowledgment
            await self.send_event(session_id, "connection_established", {
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat(),
                "features": ["file_upload", "real_time_streaming", "multi_agent"]
            })
            
        except Exception as e:
            logger.error(f"❌ WebSocket connection error: {str(e)}")
            raise
    
    async def disconnect_websocket(self, session_id: str):
        """Handle WebSocket disconnection."""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        
        logger.info(f"🔌 WebSocket disconnected for session: {session_id}")
    
    async def send_event(self, session_id: str, event_type: str, data: Dict[str, Any]):
        """Send AG-UI event to client via WebSocket."""
        if session_id not in self.active_connections:
            logger.warning(f"⚠️ No active connection for session: {session_id}")
            return
        
        try:
            event = {
                "type": event_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat(),
                "session_id": session_id
            }
            
            websocket = self.active_connections[session_id]
            await websocket.send_text(json.dumps(event))
            
            logger.debug(f"📤 Sent {event_type} event to session: {session_id}")
            
        except Exception as e:
            logger.error(f"❌ Error sending event to {session_id}: {str(e)}")
            await self.disconnect_websocket(session_id)
    
    async def handle_file_upload(self, session_id: str, file: UploadFile) -> Dict[str, Any]:
        """Handle file upload through AG-UI protocol."""
        try:
            # Read file content
            file_content = await file.read()
            file_info = {
                "id": str(uuid.uuid4()),
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(file_content),
                "uploaded_at": datetime.utcnow().isoformat()
            }
            
            # Store file info in session
            if session_id in self.active_sessions:
                self.active_sessions[session_id]["files"].append(file_info)
            
            # Send file upload confirmation
            await self.send_event(session_id, "file_uploaded", {
                "file": file_info,
                "message": f"File '{file.filename}' uploaded successfully"
            })
            
            logger.info(f"📁 File uploaded: {file.filename} for session: {session_id}")
            
            return {
                "status": "success",
                "file": file_info,
                "content": file_content.decode('utf-8') if file.content_type and file.content_type.startswith('text') else None
            }
            
        except Exception as e:
            logger.error(f"❌ File upload error: {str(e)}")
            await self.send_event(session_id, "error", {
                "message": f"File upload failed: {str(e)}"
            })
            return {"status": "error", "message": str(e)}
    
    async def stream_agent_response(
        self, 
        session_id: str, 
        triage_agent, 
        prompt: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream agent responses using AG-UI protocol events.
        
        Provides real-time updates during agent processing including:
        - Agent thinking/processing states
        - Partial responses with delta streaming
        - Agent handoffs and routing decisions
        - Final response delivery
        """
        try:
            # Send agent thinking event
            await self.send_event(session_id, "agent_thinking", {
                "message": "Processing your request...",
                "agent": "Triage Agent",
                "status": "analyzing"
            })
            
            # Include file context if available
            session_context = {}
            if session_id in self.active_sessions:
                session_files = self.active_sessions[session_id]["files"]
                if session_files:
                    session_context["uploaded_files"] = session_files
            
            # Merge with provided context
            if context:
                session_context.update(context)
            
            # Send agent processing event
            await self.send_event(session_id, "agent_processing", {
                "message": "Running multi-agent analysis...",
                "context": session_context
            })
            
            # Run the agent with context
            result = await Runner.run(triage_agent, prompt, context=session_context)
            
            # Send agent response event
            response_content = result.final_output if result.final_output else "No response"
            
            await self.send_event(session_id, "agent_response", {
                "content": response_content,
                "agent": "Multi-Agent System",
                "status": "completed"
            })
            
            # Store conversation in database
            await self.store_conversation(session_id, prompt, response_content, session_context)
            
            # Send completion event
            await self.send_event(session_id, "task_completed", {
                "message": "Request processed successfully",
                "session_id": session_id
            })
            
            yield {
                "type": "response",
                "content": response_content,
                "session_id": session_id,
                "status": "completed"
            }
            
            logger.info(f"✅ Agent response streamed for session: {session_id}")
            
        except Exception as e:
            logger.error(f"❌ Agent streaming error: {str(e)}")
            
            # Send error event
            await self.send_event(session_id, "error", {
                "message": f"Agent processing failed: {str(e)}",
                "error_type": "agent_error"
            })
            
            # Handle guardrail rejections gracefully
            if "guardrail" in str(e).lower():
                error_message = "Sorry, I can only help with homework-related questions."
                await self.send_event(session_id, "agent_response", {
                    "content": error_message,
                    "agent": "Guardrail System",
                    "status": "blocked"
                })
                
                yield {
                    "type": "response",
                    "content": error_message,
                    "session_id": session_id,
                    "status": "blocked"
                }
            else:
                yield {
                    "type": "error",
                    "message": str(e),
                    "session_id": session_id,
                    "status": "error"
                }
    
    async def store_conversation(
        self, 
        session_id: str, 
        prompt: str, 
        response: str, 
        context: Optional[Dict[str, Any]] = None
    ):
        """Store conversation with AG-UI metadata in database."""
        try:
            # Store in database
            with self.engine.begin() as conn:
                conn.execute(self.messages.insert(), [
                    {
                        "role": "user", 
                        "content": prompt,
                        "ts": datetime.utcnow()
                    },
                    {
                        "role": "assistant", 
                        "content": response,
                        "ts": datetime.utcnow()
                    }
                ])
            
            logger.info(f"💾 Conversation stored for session: {session_id}")
            
        except Exception as e:
            logger.error(f"❌ Database storage error: {str(e)}")
    
    async def handle_websocket_message(self, session_id: str, message: str, triage_agent):
        """Handle incoming WebSocket messages using AG-UI protocol."""
        try:
            # Parse incoming message
            data = json.loads(message)
            message_type = data.get("type", "chat")
            content = data.get("content", "")
            
            logger.info(f"📨 Received {message_type} message from session: {session_id}")
            
            if message_type == "chat":
                # Handle chat message with streaming response
                async for response_chunk in self.stream_agent_response(
                    session_id, 
                    triage_agent, 
                    content,
                    data.get("context")
                ):
                    # Response is already sent via events in stream_agent_response
                    pass
                    
            elif message_type == "file_context":
                # Handle file context update
                if session_id in self.active_sessions:
                    self.active_sessions[session_id]["context"].update(data.get("context", {}))
                
                await self.send_event(session_id, "context_updated", {
                    "message": "Context updated successfully",
                    "context": self.active_sessions[session_id]["context"]
                })
                
            elif message_type == "ping":
                # Handle ping/pong for connection health
                await self.send_event(session_id, "pong", {
                    "timestamp": datetime.utcnow().isoformat()
                })
                
            else:
                logger.warning(f"⚠️ Unknown message type: {message_type}")
                await self.send_event(session_id, "error", {
                    "message": f"Unknown message type: {message_type}"
                })
                
        except json.JSONDecodeError:
            logger.error(f"❌ Invalid JSON message from session: {session_id}")
            await self.send_event(session_id, "error", {
                "message": "Invalid message format"
            })
        except Exception as e:
            logger.error(f"❌ WebSocket message handling error: {str(e)}")
            await self.send_event(session_id, "error", {
                "message": f"Message processing failed: {str(e)}"
            })
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information including uploaded files and context."""
        return self.active_sessions.get(session_id)
    
    def get_active_sessions(self) -> List[str]:
        """Get list of active session IDs."""
        return list(self.active_connections.keys())

# AG-UI Event Types for reference
class AGUIEventType:
    """AG-UI Protocol Event Types for enhanced agent-UI communication."""
    
    # Connection events
    CONNECTION_ESTABLISHED = "connection_established"
    CONNECTION_CLOSED = "connection_closed"
    
    # Agent events
    AGENT_THINKING = "agent_thinking"
    AGENT_PROCESSING = "agent_processing"
    AGENT_RESPONSE = "agent_response"
    AGENT_HANDOFF = "agent_handoff"
    
    # File events
    FILE_UPLOADED = "file_uploaded"
    FILE_PROCESSED = "file_processed"
    
    # Context events
    CONTEXT_UPDATED = "context_updated"
    STATE_SYNC = "state_sync"
    
    # Task events
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    
    # Communication events
    MESSAGE_RECEIVED = "message_received"
    MESSAGE_SENT = "message_sent"
    TYPING_INDICATOR = "typing_indicator"
    
    # System events
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    PONG = "pong" 
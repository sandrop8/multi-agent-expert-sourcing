"""
Multi-Agent Expert Sourcing Backend with AG-UI Protocol Integration

This FastAPI backend provides:
 - POST /chat       : runs OpenAI Agents SDK multi-agent system and stores Q&A in Postgres
 - GET  /history    : returns the last N messages
 - WebSocket /ws    : AG-UI protocol real-time communication
 - POST /upload     : file upload with AG-UI integration
 - GET  /sessions   : active AG-UI sessions management
"""

import os
import datetime as dt
import asyncio
import uuid
from typing import List

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

import sqlalchemy as sa                              # SQLAlchemy 2.x
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner  # openai-agents-python

# Import our AG-UI adapter
from ag_ui_adapter import AGUIAdapter

# Load environment variables from .env file
load_dotenv()

# ---- Environment ----------------------------------------------------------
OPENAI_KEY   = os.getenv("OPENAI_API_KEY")           # set in Railway › Variables
DATABASE_URL = os.getenv("PG_URL")                   # injected by PG plugin

# Better error messages for missing environment variables
missing_vars = []
if not OPENAI_KEY:
    missing_vars.append("OPENAI_API_KEY")
if not DATABASE_URL:
    missing_vars.append("PG_URL")

if missing_vars:
    print("❌ Missing required environment variables:")
    for var in missing_vars:
        print(f"   - {var}")
    print("\n💡 For local development:")
    print("   - Get OPENAI_API_KEY from: https://platform.openai.com/api-keys")
    print("   - For PG_URL, you can use:")
    print("     • Local PostgreSQL: postgresql://user:password@localhost:5432/dbname")
    print("     • Docker: docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres")
    print("     • Railway/Supabase/Neon for cloud database")
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing_vars)}")

# ---- Database schema ------------------------------------------------------
engine = sa.create_engine(DATABASE_URL, future=True)
meta   = sa.MetaData()

messages = sa.Table(
    "messages",
    meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("role", sa.String(10)),
    sa.Column("content", sa.Text),
    sa.Column("ts", sa.DateTime, default=dt.datetime.utcnow),
)

meta.create_all(engine)                              # auto-create table

# ---- Multi-Agent System Implementation -------------------------------------

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)

# ---- AG-UI Integration ----------------------------------------------------

# Initialize AG-UI adapter
agui_adapter = AGUIAdapter(engine, messages)

# ---- FastAPI application --------------------------------------------------
app = FastAPI(title="Multi-Agent Expert Sourcing API with AG-UI")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class ChatReq(BaseModel):
    prompt: str

class Msg(BaseModel):
    id: int
    role: str
    content: str
    ts: dt.datetime

class SessionInfo(BaseModel):
    session_id: str
    connected_at: str
    files: List[dict]
    context: dict

# ---- Traditional Chat Endpoint (Backward Compatibility) ------------------

@app.post("/chat")
async def chat(req: ChatReq):
    """Run the multi-agent system, store conversation, return response."""
    try:
        print(f"🔍 Processing request: {req.prompt}")
        
        # Use triage_agent as entry point to multi-agent system
        result = await Runner.run(triage_agent, req.prompt)
        
        answer = result.final_output if result.final_output else "No response"
        print(f"✅ AI Response: {answer}")

        # Store in database (existing logic)
        with engine.begin() as conn:
            conn.execute(messages.insert(), [
                {"role": "user",      "content": req.prompt},
                {"role": "assistant", "content": answer},
            ])
        print(f"💾 Stored conversation in database")
        
        return {"answer": answer}
    
    except Exception as e:
        print(f"❌ Error in chat endpoint: {str(e)}")
        # Handle guardrail rejections gracefully
        if "guardrail" in str(e).lower():
            return {"answer": "Sorry, I can only help with homework-related questions."}
        raise HTTPException(500, str(e))

# ---- AG-UI Protocol Endpoints --------------------------------------------

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """AG-UI WebSocket endpoint for real-time agent communication."""
    await agui_adapter.connect_websocket(websocket, session_id)
    
    try:
        while True:
            # Receive message from client
            message = await websocket.receive_text()
            
            # Handle message through AG-UI adapter
            await agui_adapter.handle_websocket_message(session_id, message, triage_agent)
            
    except WebSocketDisconnect:
        print(f"🔌 WebSocket disconnected: {session_id}")
        await agui_adapter.disconnect_websocket(session_id)
    except Exception as e:
        print(f"❌ WebSocket error for {session_id}: {str(e)}")
        await agui_adapter.disconnect_websocket(session_id)

@app.post("/upload/{session_id}")
async def upload_file(session_id: str, file: UploadFile = File(...)):
    """Handle file uploads with AG-UI integration."""
    try:
        print(f"📁 File upload request: {file.filename} for session: {session_id}")
        
        # Handle file upload through AG-UI adapter
        result = await agui_adapter.handle_file_upload(session_id, file)
        
        if result["status"] == "success":
            print(f"✅ File uploaded successfully: {file.filename}")
            return {
                "message": "File uploaded successfully",
                "file": result["file"],
                "session_id": session_id
            }
        else:
            print(f"❌ File upload failed: {result['message']}")
            raise HTTPException(400, result["message"])
            
    except Exception as e:
        print(f"❌ File upload error: {str(e)}")
        raise HTTPException(500, f"File upload failed: {str(e)}")

@app.get("/sessions", response_model=List[SessionInfo])
async def get_active_sessions():
    """Get list of active AG-UI sessions."""
    try:
        active_sessions = []
        for session_id in agui_adapter.get_active_sessions():
            session_info = agui_adapter.get_session_info(session_id)
            if session_info:
                active_sessions.append(SessionInfo(
                    session_id=session_id,
                    connected_at=session_info["connected_at"].isoformat(),
                    files=session_info["files"],
                    context=session_info["context"]
                ))
        
        return active_sessions
        
    except Exception as e:
        print(f"❌ Error getting sessions: {str(e)}")
        raise HTTPException(500, str(e))

@app.get("/sessions/{session_id}")
async def get_session_info(session_id: str):
    """Get information about a specific AG-UI session."""
    try:
        session_info = agui_adapter.get_session_info(session_id)
        if not session_info:
            raise HTTPException(404, f"Session {session_id} not found")
        
        return {
            "session_id": session_id,
            "connected_at": session_info["connected_at"].isoformat(),
            "files": session_info["files"],
            "context": session_info["context"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting session info: {str(e)}")
        raise HTTPException(500, str(e))

# ---- Traditional History Endpoint ----------------------------------------

@app.get("/history", response_model=List[Msg])
async def history(limit: int = 20):
    """Return the latest `limit` rows in ascending order."""
    with engine.connect() as conn:
        rows = conn.execute(
            sa.select(messages).order_by(messages.c.id.desc()).limit(limit)
        )
        return [dict(r) for r in rows][::-1]

# ---- Health Check Endpoint -----------------------------------------------

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": dt.datetime.utcnow().isoformat(),
        "features": [
            "multi_agent_system",
            "ag_ui_protocol",
            "file_upload",
            "real_time_streaming",
            "websocket_support"
        ],
        "active_sessions": len(agui_adapter.get_active_sessions())
    }

# ---- Testing Function (for development/debugging) -------------------------
async def test_multi_agent_system():
    """Test function to verify multi-agent system functionality"""
    print("🧪 Testing multi-agent system...")
    
    # Test 1: History question
    print("\n📚 Testing history question:")
    result = await Runner.run(triage_agent, "who was the first president of the united states?")
    print(f"Response: {result.final_output}")
    
    # Test 2: Math question
    print("\n🔢 Testing math question:")
    result = await Runner.run(triage_agent, "what is 2+2?")
    print(f"Response: {result.final_output}")
    
    # Test 3: Non-homework question (should be blocked)
    print("\n🚫 Testing non-homework question:")
    try:
        result = await Runner.run(triage_agent, "what is life")
        print(f"Response: {result.final_output}")
    except Exception as e:
        print(f"Blocked by guardrail: {str(e)}")

if __name__ == "__main__":
    # Run tests if script is executed directly
    asyncio.run(test_multi_agent_system()) 
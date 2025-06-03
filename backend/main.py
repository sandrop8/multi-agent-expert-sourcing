"""
Minimal FastAPI backend exposing endpoints:
 - POST /chat      : runs OpenAI Agents SDK multi-agent system and stores Q&A in Postgres
 - GET  /history   : returns the last N messages
 - POST /upload-cv : handles CV file uploads and stores them in Postgres
"""

import os
import datetime as dt
import asyncio
from typing import List

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

import sqlalchemy as sa                              # SQLAlchemy 2.x
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner  # openai-agents-python

# Load environment variables from .env file
load_dotenv()

# ---- Environment ----------------------------------------------------------
OPENAI_KEY   = os.getenv("OPENAI_API_KEY")           # set in Railway › Variables
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("PG_URL")  # Railway uses DATABASE_URL

# Better error messages for missing environment variables
missing_vars = []
if not OPENAI_KEY:
    missing_vars.append("OPENAI_API_KEY")
if not DATABASE_URL:
    missing_vars.append("DATABASE_URL or PG_URL")

if missing_vars:
    print("❌ Missing required environment variables:")
    for var in missing_vars:
        print(f"   - {var}")
    print("\n💡 For local development:")
    print("   - Get OPENAI_API_KEY from: https://platform.openai.com/api-keys")
    print("   - For DATABASE_URL/PG_URL, you can use:")
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

# CV storage table
cvs = sa.Table(
    "cvs",
    meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("filename", sa.String(255)),
    sa.Column("original_filename", sa.String(255)),
    sa.Column("file_size", sa.Integer),
    sa.Column("content_type", sa.String(100)),
    sa.Column("file_data", sa.LargeBinary),  # Store file content as binary
    sa.Column("uploaded_at", sa.DateTime, default=dt.datetime.utcnow),
    sa.Column("processed", sa.Boolean, default=False),
)

meta.create_all(engine)                              # auto-create tables

# ---- Multi-Agent System Implementation -------------------------------------

class ExpertSourcingOutput(BaseModel):
    is_expert_sourcing: bool
    reasoning: str

guardrail_agent = Agent(
    name="Expert Sourcing Validator",
    instructions="Check if the user is requesting expert sourcing, matchmaking, or talent acquisition services.",
    output_type=ExpertSourcingOutput,
)

project_requirements_agent = Agent(
    name="Project Requirements Assistant",
    handoff_description="Specialist agent for helping project owners create comprehensive project descriptions",
    instructions="You help project owners articulate and develop their project requirements. Guide them through defining scope, timeline, budget, required skills, and deliverables to create a complete project description.",
)

project_refinement_agent = Agent(
    name="Project Refinement Specialist",
    handoff_description="Specialist agent for finalizing and polishing project descriptions",
    instructions="You help project owners refine and finalize their project descriptions. Identify missing information, suggest improvements, and ensure the project description is clear, complete, and attractive to potential freelancers.",
)

async def expert_sourcing_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(ExpertSourcingOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_expert_sourcing,
    )

supervisor_agent = Agent(
    name="Expert Sourcing Supervisor",
    instructions="You coordinate the project submission workflow by determining which specialist agent to use based on the client's needs - helping create project requirements or refining and finalizing project descriptions.",
    handoffs=[project_refinement_agent, project_requirements_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=expert_sourcing_guardrail),
    ],
)

# ---- FastAPI application --------------------------------------------------
app = FastAPI(title="Multi-Agent Expert Sourcing API")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3002",  # Add port 3002 for your current frontend
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3002",  # Add 127.0.0.1 version too
        "https://poetic-optimism-production.up.railway.app"  # Railway frontend URL
    ],
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

@app.post("/chat")
async def chat(req: ChatReq):
    """Run the multi-agent system, store conversation, return response."""
    try:
        print(f"🔍 Processing request: {req.prompt}")
        
        # Use supervisor_agent as entry point to multi-agent system
        result = await Runner.run(supervisor_agent, req.prompt)
        
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
            return {"answer": "Sorry, I can only help with expert sourcing and talent acquisition requests."}
        raise HTTPException(500, str(e))

@app.get("/history", response_model=List[Msg])
async def history(limit: int = 20):
    """Return the latest `limit` rows in ascending order."""
    with engine.connect() as conn:
        rows = conn.execute(
            sa.select(messages).order_by(messages.c.id.desc()).limit(limit)
        )
        return [dict(r) for r in rows][::-1]

@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    """Handle CV file uploads and store them in Postgres."""
    try:
        # Validate file type
        allowed_types = ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        if file.content_type not in allowed_types:
            raise HTTPException(400, "Only PDF and Word documents are allowed")
        
        # Validate file size (10MB limit)
        file_content = await file.read()
        if len(file_content) > 10 * 1024 * 1024:
            raise HTTPException(400, "File size exceeds 10MB limit")
        
        print(f"📁 Processing CV upload: {file.filename} ({len(file_content)} bytes)")

        # Store file in database
        with engine.begin() as conn:
            result = conn.execute(cvs.insert(), [{
                "filename": file.filename,
                "original_filename": file.filename,
                "file_size": len(file_content),
                "content_type": file.content_type,
                "file_data": file_content,
                "processed": False
            }])
            
        print(f"💾 CV stored successfully in database")
        
        return {
            "message": "CV uploaded successfully",
            "filename": file.filename,
            "size": len(file_content)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in upload endpoint: {str(e)}")
        raise HTTPException(500, f"Upload failed: {str(e)}")

@app.get("/cvs")
async def list_cvs():
    """Get list of uploaded CVs (for testing/debugging)."""
    try:
        with engine.connect() as conn:
            rows = conn.execute(
                sa.select(cvs.c.id, cvs.c.filename, cvs.c.file_size, cvs.c.content_type, cvs.c.uploaded_at, cvs.c.processed)
                .order_by(cvs.c.uploaded_at.desc())
            )
            return [dict(r._mapping) for r in rows]
    except Exception as e:
        print(f"❌ Error listing CVs: {str(e)}")
        raise HTTPException(500, str(e))

# ---- Testing Function (for development/debugging) -------------------------
async def test_multi_agent_system():
    """Test function to verify multi-agent system functionality"""
    print("🧪 Testing multi-agent system...")
    
    # Test 1: Expert search question
    print("\n🔍 Testing expert search question:")
    result = await Runner.run(supervisor_agent, "I need to find a Python developer for my fintech project")
    print(f"Response: {result.final_output}")
    
    # Test 2: CV parsing question
    print("\n📄 Testing CV parsing question:")
    result = await Runner.run(supervisor_agent, "Can you analyze this developer's CV and extract their key skills?")
    print(f"Response: {result.final_output}")
    
    # Test 3: Non-expert-sourcing question (should be blocked)
    print("\n🚫 Testing non-expert-sourcing question:")
    try:
        result = await Runner.run(supervisor_agent, "what is the weather today?")
        print(f"Response: {result.final_output}")
    except Exception as e:
        print(f"Blocked by guardrail: {str(e)}")

if __name__ == "__main__":
    # Run tests if script is executed directly
    asyncio.run(test_multi_agent_system()) 
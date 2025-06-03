"""
Minimal FastAPI backend exposing two endpoints:
 - POST /chat    : runs OpenAI Agents SDK multi-agent system and stores Q&A in Postgres
 - GET  /history : returns the last N messages
"""

import os
import datetime as dt
import asyncio
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

import sqlalchemy as sa                              # SQLAlchemy 2.x
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner  # openai-agents-python

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

# ---- FastAPI application --------------------------------------------------
app = FastAPI(title="Multi-Agent Expert Sourcing API")

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

@app.get("/history", response_model=List[Msg])
async def history(limit: int = 20):
    """Return the latest `limit` rows in ascending order."""
    with engine.connect() as conn:
        rows = conn.execute(
            sa.select(messages).order_by(messages.c.id.desc()).limit(limit)
        )
        return [dict(r) for r in rows][::-1]

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
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

class ExpertSourcingOutput(BaseModel):
    is_expert_sourcing: bool
    reasoning: str

guardrail_agent = Agent(
    name="Expert Sourcing Validator",
    instructions="Check if the user is requesting expert sourcing, matchmaking, or talent acquisition services.",
    output_type=ExpertSourcingOutput,
)

expert_search_agent = Agent(
    name="Expert Search & Matchmaking Specialist",
    handoff_description="Specialist agent for finding and matching experts to project requirements",
    instructions="You help find and match experts to specific project needs. Analyze requirements, search criteria, and provide recommendations for expert selection and matchmaking.",
)

profile_enrichment_agent = Agent(
    name="CV Parsing & Profile Enrichment Specialist",
    handoff_description="Specialist agent for CV analysis and expert profile enhancement",
    instructions="You analyze CVs, parse professional profiles, and enrich expert data. Extract key skills, experience, and qualifications to create comprehensive expert profiles.",
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
    instructions="You coordinate the expert sourcing workflow by determining which specialist agent to use based on the client's needs - expert search/matchmaking or CV parsing/profile enrichment.",
    handoffs=[profile_enrichment_agent, expert_search_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=expert_sourcing_guardrail),
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
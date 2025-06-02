"""
Minimal FastAPI backend exposing two endpoints:
 - POST /chat    : runs OpenAI Agents SDK and stores Q&A in Postgres
 - GET  /history : returns the last N messages
"""

import os
import datetime as dt
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

import sqlalchemy as sa                              # SQLAlchemy 2.x
from agents import Agent, Runner                     # openai-agents-python

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

# ---- OpenAI Agent ---------------------------------------------------------
assistant = Agent(
    name="HelperBot",
    instructions="Be helpful and concise.",
    model="gpt-4o-mini",                            # Updated to use gpt-4o-mini
)

# ---- FastAPI application --------------------------------------------------
app = FastAPI(title="Agents API")

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
    """Run the agent, store both prompt and answer, return the answer."""
    try:
        print(f"🔍 Processing request: {req.prompt}")
        
        # Use the new Runner.run() API instead of create_run/run_async
        result = await Runner.run(assistant, req.prompt)
        
        # Get the assistant's response from final_output
        answer = result.final_output if result.final_output else "No response"
        print(f"✅ AI Response: {answer}")

        # Store in database
        with engine.begin() as conn:
            conn.execute(messages.insert(), [
                {"role": "user",      "content": req.prompt},
                {"role": "assistant", "content": answer},
            ])
        print(f"💾 Stored conversation in database")
        
        return {"answer": answer}
    except Exception as e:
        print(f"❌ Error in chat endpoint: {str(e)}")
        raise HTTPException(500, str(e))

@app.get("/history", response_model=List[Msg])
async def history(limit: int = 20):
    """Return the latest `limit` rows in ascending order."""
    with engine.connect() as conn:
        rows = conn.execute(
            sa.select(messages).order_by(messages.c.id.desc()).limit(limit)
        )
        return [dict(r) for r in rows][::-1] 
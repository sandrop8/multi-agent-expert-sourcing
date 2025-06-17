"""
FastAPI application setup and route registration
Phase 1 refactored version of main.py
"""

from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

# Import configuration
from core.config import CORS_ORIGINS

# Import database setup
from models.base import create_all_tables

# Import API routes
from api.v1.chat import router as chat_router
from api.v1.cv import router as cv_router, processing_router as cv_processing_router
from api.v1.company import router as company_router
from api.v1.nats import router as nats_router
from schemas.cv_schemas import CVUploadResponse
from schemas.chat_schemas import ChatReq
from services.cv_service import CVService

# Import CrewAI company profiling function
from pydantic import BaseModel
from typing import Optional


class CompanyRegistrationRequest(BaseModel):
    website_url: str
    linkedin_url: Optional[str] = None


# ---- FastAPI application setup --------------------------------------------
app = FastAPI(title="Multi-Agent Expert Sourcing API")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Register RESTful API routes
app.include_router(chat_router)
app.include_router(cv_router)
app.include_router(cv_processing_router)
app.include_router(company_router)
app.include_router(nats_router)

# Legacy endpoints for backward compatibility


@app.post("/chat")
async def legacy_chat(req: ChatReq):
    """Legacy chat endpoint - redirects to /conversations/"""
    from api.v1.chat import create_conversation_message

    return await create_conversation_message(req)


@app.get("/history")
async def legacy_history(limit: int = 20):
    """Legacy history endpoint - redirects to /conversations/"""
    from api.v1.chat import list_conversation_history

    return await list_conversation_history(limit)


@app.post("/upload-cv", response_model=CVUploadResponse)
async def legacy_upload_cv(
    background_tasks: BackgroundTasks, file: UploadFile = File(...)
):
    """
    Legacy CV upload endpoint - redirects to /cvs/
    Processes the CV in the background and returns a session ID for polling.
    """
    cv_service = CVService()
    return await cv_service.upload_cv(file, background_tasks)


@app.get("/cv-status/{session_id}")
async def legacy_cv_status(session_id: str):
    """Legacy CV status endpoint - redirects to /cv-processing-sessions/{session_id}"""
    from api.v1.cv import get_processing_session

    return await get_processing_session(session_id)


# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables and NATS connection"""
    print("🚀 Starting Multi-Agent Expert Sourcing API...")

    # Initialize database
    create_all_tables()
    print("✅ Database tables created/verified")

    # Initialize NATS connection
    try:
        from core.nats import init_nats
        from api.v1.nats import setup_event_subscribers

        await init_nats()
        print("✅ NATS connection established")

        # Setup event subscribers in background
        import asyncio
        from core.nats import get_nats

        nats_client = await get_nats()
        asyncio.create_task(setup_event_subscribers(nats_client))
        print("✅ NATS event subscribers configured")

    except Exception as e:
        print(f"⚠️  NATS initialization failed: {e}")
        print("   The app will continue without NATS functionality")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown of NATS connection"""
    try:
        from core.nats import close_nats

        await close_nats()
        print("✅ NATS connection closed")
    except Exception as e:
        print(f"⚠️  NATS shutdown error: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

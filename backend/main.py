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
from api.v1.cv import router as cv_router
from api.v1.company import router as company_router
from schemas.cv_schemas import CVUploadResponse
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

# Register API routes
app.include_router(chat_router)
app.include_router(cv_router)
app.include_router(company_router)

# Legacy endpoints for backward compatibility
from schemas.chat_schemas import ChatReq


@app.post("/chat")
async def legacy_chat(req: ChatReq):
    """Legacy chat endpoint - redirects to /chat/"""
    from api.v1.chat import chat

    return await chat(req)


@app.get("/history")
async def legacy_history(limit: int = 20):
    """Legacy history endpoint - redirects to /chat/history"""
    from api.v1.chat import history

    return await history(limit)


@app.post("/upload-cv", response_model=CVUploadResponse)
async def legacy_upload_cv(
    background_tasks: BackgroundTasks, file: UploadFile = File(...)
):
    """
    Legacy CV upload endpoint.
    Processes the CV in the background and returns a session ID for polling.
    """
    cv_service = CVService()
    return await cv_service.upload_cv(file, background_tasks)


@app.get("/cv-status/{session_id}")
async def legacy_cv_status(session_id: str):
    """Legacy CV status endpoint - redirects to /cv/status/{session_id}"""
    from api.v1.cv import get_cv_status

    return await get_cv_status(session_id)


@app.get("/cvs")
async def legacy_list_cvs():
    """Legacy CV list endpoint - redirects to /cv/list"""
    from api.v1.cv import list_cvs

    return await list_cvs()


# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables"""
    print("🚀 Starting Multi-Agent Expert Sourcing API...")
    create_all_tables()
    print("✅ Database tables created/verified")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

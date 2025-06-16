"""
Company API endpoints
"""
from fastapi import APIRouter, BackgroundTasks
from schemas.company_schemas import CompanyRegistrationRequest
from services.company_service import CompanyService

router = APIRouter(prefix="/company", tags=["company"])

@router.post("/register")
async def register_company(req: CompanyRegistrationRequest, background_tasks: BackgroundTasks):
    """
    Endpoint to register a company and trigger the CrewAI profiling workflow.
    """
    company_service = CompanyService()
    result = company_service.start_company_profiling_crew(req.website_url, background_tasks)
    return result 
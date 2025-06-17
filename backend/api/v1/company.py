"""
Company API endpoints following RESTful principles
"""

from fastapi import APIRouter, BackgroundTasks, status, HTTPException
from schemas.company_schemas import CompanyRegistrationRequest
from services.company_service import CompanyService

# RESTful resource-based router for companies
router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_company(
    req: CompanyRegistrationRequest, background_tasks: BackgroundTasks
):
    """Create a new company resource and trigger profiling workflow.

    Follows RESTful principle: POST /companies creates a new company resource.
    Returns 201 Created on successful resource creation.
    """
    try:
        company_service = CompanyService()
        result = company_service.start_company_profiling_crew(
            req.website_url, background_tasks
        )
        return result
    except Exception as e:
        print(f"❌ Error in company creation endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating company resource: {str(e)}",
        )

"""
Company Service - business logic for company registration and profiling
"""
from fastapi import BackgroundTasks
from app_agents.company_crew import run_test_crew

class CompanyService:
    """Service class for company-related business logic"""
    
    def __init__(self):
        # In the future, this could initialize a database session, etc.
        pass
    
    def start_company_profiling_crew(self, website_url: str, background_tasks: BackgroundTasks):
        """
        Schedules the CrewAI company profiling workflow to run in the background.
        """
        print(f"🏢 [CompanyService] Scheduling CrewAI workflow for URL: {website_url}")
        background_tasks.add_task(run_test_crew, website_url)
        # In a real application, we might return a session_id here for status polling
        return {"message": "Company profiling process has been started in the background."} 
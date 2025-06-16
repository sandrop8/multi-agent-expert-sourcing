"""
CrewAI agent definitions for company profiling
"""
import os
from crewai import Agent, Crew, Process, Task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

# To handle cases where SERPER_API_KEY is not set
serper_api_key = os.getenv("SERPER_API_KEY")
search_tool = SerperDevTool() if serper_api_key else None
scrape_tool = ScrapeWebsiteTool()

# Agent 1: Website Content Scraper
WebsiteContentScraper = Agent(
    role="Website Content Scraper",
    goal="Scrape the provided company URL to extract key information about the company, such as services, mission, and contact details.",
    backstory="An expert in navigating website structures to find and pull relevant text-based content efficiently.",
    verbose=True,
    allow_delegation=False,
    tools=[scrape_tool]
)

# Agent 2: Data Enrichment Researcher
DataEnrichmentResearcher = Agent(
    role="Data Enrichment Researcher",
    goal="Analyze scraped data, identify missing critical information, and use web search to find missing pieces like address, founding year, executives.",
    backstory="A resourceful detective who excels at finding publicly available information to fill in the gaps and verify facts.",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool] if search_tool else []
)

# Agent 3: Company Profile Synthesizer
CompanyProfileSynthesizer = Agent(
    role="Company Profile Synthesizer",
    goal="Take raw and enriched data to create a clean, structured JSON object with company information.",
    backstory="A meticulous editor and data analyst who transforms scattered information into a polished, coherent, and actionable company profile.",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# Task 1: Initial Website Scraping
scrape_task = Task(
    description="Scrape the content of the provided URL: {url}. Focus on extracting text related to services, company mission, about section, and contact information.",
    expected_output="A raw text document containing all relevant information found on the website.",
    agent=WebsiteContentScraper
)

# Task 2: Enrich and Verify Data
enrich_task = Task(
    description="Review the scraped content. Identify and search for the following missing key information: official company address, main phone number, and a definitive list of services. If the scraped content is unclear, use your search tool to find clarity.",
    expected_output="A report containing any missing information found through web searches, along with the source URLs for verification.",
    agent=DataEnrichmentResearcher,
    context=[scrape_task]
)

# Task 3: Synthesize Final Company Profile
synthesize_task = Task(
    description="Consolidate all the information gathered from the website scraping and the data enrichment tasks. Create a final, structured JSON object with keys for 'company_name', 'services', 'location', 'contact_info', and a 'summary'.",
    expected_output="A complete and validated JSON object representing the company's profile, ready for system use.",
    agent=CompanyProfileSynthesizer,
    context=[scrape_task, enrich_task]
)

# Define the crew for company profiling
company_profiling_crew = Crew(
    agents=[WebsiteContentScraper, DataEnrichmentResearcher, CompanyProfileSynthesizer],
    tasks=[scrape_task, enrich_task, synthesize_task],
    verbose=True,
    process=Process.sequential
)

def run_company_profiling_crew(url: str):
    """
    Initializes and runs the company profiling crew.
    """
    print(f"🚀 Initializing and running the company profiling crew for URL: {url}...")
    try:
        result = company_profiling_crew.kickoff(inputs={'url': url})
        print("✅ Company profiling crew finished running.")
        print("📝 Result:")
        print(result)
        return result
    except Exception as e:
        print(f"❌ Error running company profiling crew: {str(e)}")
        return {"error": str(e)} 
# Project Outline: Company Service Registration & Web Scraping Workflow

This document outlines the step-by-step plan to implement a new feature allowing companies/agencies to register their services. This workflow will utilize the CrewAI framework for backend processing.

## Phase 1: Frontend UI Implementation (Static)

1.  **Update Homepage (`/`)**:
    *   Add a third container to `frontend/app/page.tsx` alongside "Submit a Project" and "I'm a Freelancer".
    *   **Title**: "Register as a Service Provider"
    *   **Design**: The container will have a consistent design with the existing two cards.
    *   **Link**: It will link to a new page, `/company-registration`.

2.  **Create Company Registration Page (`/company-registration`)**:
    *   Create a new page `frontend/app/company-registration/page.tsx`.
    *   **Design**: The page layout and styling should be consistent with `frontend/app/project/page.tsx`.
    *   **Inputs**:
        *   A required input field for the company's website URL.
        *   An optional input field for the company's LinkedIn profile URL.
    *   **Action**: A "Register" or "Submit for Analysis" button.
    *   **Functionality**: Initially, the button will have no action. The focus is on UI and page flow first.

## Phase 2: Backend - CrewAI Agentic Workflow for Company Profiling

This phase will implement an entirely new agentic workflow using the **CrewAI framework** to demonstrate a different approach to multi-agent systems compared to the existing OpenAI Agents SDK implementation. The goal is to create a sophisticated, yet easy-to-understand crew of AI agents that collaborate to build a detailed profile of a company by scraping its website and enriching the data with web research.

This approach will highlight CrewAI's strengths in defining specialized agents with specific tools and orchestrating them through a sequence of tasks.

1.  **Setup CrewAI Environment**:
    *   Add `crewai` and `crewai-tools` to the backend dependencies in `pyproject.toml`.
    *   Already in .env file Configured necessary API keys (e.g., `OPENAI_API_KEY`) and a search tool API key (e.g., `SERPER_API_KEY`).

2.  **The Company Profiling Crew: Agents & Roles**:
    *   A new file, `backend/app_agents/company_crew.py`, will be created to house the CrewAI definitions. The crew will consist of a team of specialist agents with distinct roles, goals, and toolsets, orchestrated by the Crew's sequential process manager.

    *   **Specialist Agent 1**: `WebsiteContentScraper`
        *   **Role**: A specialist focused on initial data extraction from a company's website.
        *   **Goal**: To scrape the provided company URL and extract as much key information as possible, such as services offered, company mission/vision, "About Us" text, and contact details from a contact page.
        *   **Tools**: `ScrapeWebsiteTool` from `crewai-tools`.
        *   **Backstory**: An expert in navigating website structures to find and pull relevant text-based content efficiently.

    *   **Specialist Agent 2**: `DataEnrichmentResearcher`
        *   **Role**: A research analyst that verifies and supplements the initial data.
        *   **Goal**: To analyze the data from the `WebsiteContentScraper`, identify critical missing information (e.g., physical address, founding year, key executives), and use web search to find these missing pieces.
        *   **Tools**: `SerperDevTool` or `DuckDuckGoSearchRun`. This allows the agent to perform targeted web searches.
        *   **Backstory**: A resourceful detective who excels at finding publicly available information to fill in the gaps and verify facts.

    *   **Specialist Agent 3**: `CompanyProfileSynthesizer`
        *   **Role**: The final analyst responsible for creating the end product.
        *   **Goal**: To take the raw data from the scraper and the enriched data from the researcher, and synthesize it all into a clean, structured, and easy-to-read JSON object. It will perform final data cleaning and formatting.
        *   **Tools**: No external tools required. This agent focuses on reasoning and structuring information.
        *   **Backstory**: A meticulous editor and data analyst who transforms scattered information into a polished, coherent, and actionable company profile.

3.  **The Task Pipeline**:
    *   **Task 1: Initial Website Scraping**:
        *   **Description**: "Scrape the content of the provided URL: `{url}`. Focus on extracting text related to services, company mission, about section, and contact information."
        *   **Agent**: `WebsiteContentScraper`
        *   **Expected Output**: A raw text document containing all relevant information found on the website.

    *   **Task 2: Enrich and Verify Data**:
        *   **Description**: "Review the scraped content. Identify and search for the following missing key information: official company address, main phone number, and a definitive list of services. If the scraped content is unclear, use your search tool to find clarity."
        *   **Agent**: `DataEnrichmentResearcher`
        *   **Context**: This task will use the output of Task 1.
        *   **Expected Output**: A report containing any missing information found through web searches, along with the source URLs for verification.

    *   **Task 3: Synthesize Final Company Profile**:
        *   **Description**: "Consolidate all the information gathered from the website scraping and the data enrichment tasks. Create a final, structured JSON object with keys for `company_name`, `services`, `location`, `contact_info`, and a `summary`."
        *   **Agent**: `CompanyProfileSynthesizer`
        *   **Context**: This task will use the outputs of Task 1 and Task 2.
        *   **Expected Output**: A complete and validated JSON object representing the company's profile, ready for system use.

4.  **Create API Endpoint**:
    *   Add a new endpoint, `POST /register-company`, in `backend/main.py`. This endpoint will receive the company URL, initialize the CrewAI crew with its tasks, and kick off the workflow. It will return the final JSON profile generated by the `CompanyProfileSynthesizer` agent.

## Phase 3: Frontend-Backend Integration

1.  **Connect Registration Page to Backend**:
    *   In `frontend/app/company-registration/page.tsx`, implement the `onClick` handler for the "Register" button.
    *   It will make a `POST` request to the `/register-company` endpoint with the URL(s).
    *   Implement loading, success, and error states on the UI.
    *   Display a confirmation message or the analysis results upon successful submission.

## Phase 4: Testing

1.  **Backend Testing**:
    *   Create `backend/tests/test_company_agents.py`.
    *   **Unit Tests**: Test the creation of individual CrewAI agents and tasks, mocking scraping tools.
    *   **Integration Tests**: Test the `POST /register-company` endpoint using a mock website to validate the end-to-end flow.

2.  **Frontend Testing**:
    *   Create `frontend/app/company-registration/__tests__/page.test.tsx`.
    *   **Unit/Integration Tests**: Test the rendering of the registration page, user input, and mock `fetch` calls to test UI states (loading, success, error).

3.  **E2E Testing**:
    *   Add `frontend/e2e/company-registration.spec.ts`.
    *   The test will cover the user journey from the homepage to the registration page, form submission, and UI updates based on a mocked API response.

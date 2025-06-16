"""
CrewAI agent definitions for company profiling
"""
import os
from crewai import Agent, Crew, Process, Task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

# To handle cases where SERPER_API_KEY is not set
serper_api_key = os.getenv("SERPER_API_KEY")
search_tool = SerperDevTool() if serper_api_key else None

# Define a simple test agent
test_agent = Agent(
    role="Test Agent",
    goal="Verify that the CrewAI setup is working by printing a message.",
    backstory="I am a simple agent created to confirm that the basic CrewAI components can be initialized and executed.",
    verbose=True,
    allow_delegation=False,
    tools=[] # No tools needed for this simple test
)

# Define a simple test task
test_task = Task(
    description="Print a confirmation message to the console to show that the task is running. The message should include the URL: {url}",
    expected_output="A confirmation message printed to the console.",
    agent=test_agent
)

# Define the crew
test_crew = Crew(
    agents=[test_agent],
    tasks=[test_task],
    verbose=True,
    process=Process.sequential
)

def run_test_crew(url: str):
    """
    Initializes and runs the test crew.
    """
    print("🚀 Initializing and running the test crew...")
    result = test_crew.kickoff(inputs={'url': url})
    print("✅ Test crew finished running.")
    print("📝 Result:")
    print(result)
    return result 
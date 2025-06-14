"""
CV processing agent definitions
"""

from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from schemas.cv_schemas import CVValidationOutput

# ---- Agent Definitions ----------------------------------------------------
cv_guardrail_agent = Agent(
    name="CV Content Validator",
    instructions="Check if the uploaded content appears to be a valid CV/resume with professional information.",
    output_type=CVValidationOutput,
)

cv_parser_agent = Agent(
    name="CV Parser Agent",
    handoff_description="Document extraction specialist for parsing CV content",
    instructions="You extract structured information from CVs including work experience, education, skills, and contact information. Parse the document systematically and organize the data clearly.",
)

profile_enrichment_agent = Agent(
    name="Profile Enrichment Agent", 
    handoff_description="Enhancement specialist for optimizing freelancer profiles",
    instructions="You enhance basic CV data with professional summaries and achievement highlights. Create compelling professional narratives that showcase the candidate's strengths and experience effectively.",
)

skills_extraction_agent = Agent(
    name="Skills Extraction Agent",
    handoff_description="Technical specialist for identifying and categorizing skills",
    instructions="You identify technical skills, tools, programming languages, and proficiency levels from CVs. Categorize skills by type (technical, soft, domain-specific) and assess proficiency levels where possible.",
)

gap_analysis_agent = Agent(
    name="Gap Analysis Agent",
    handoff_description="Assessment specialist for profile completeness",
    instructions="You identify missing information crucial for project matching. Analyze the profile for gaps in skills, experience details, or other important information that would help with freelancer-project matching.",
)

# ---- Guardrail Functions --------------------------------------------------
async def cv_validation_guardrail(ctx, agent, input_data):
    """Guardrail to ensure only valid CV content is processed"""
    result = await Runner.run(cv_guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(CVValidationOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_valid_cv,
    )

freelancer_profile_manager = Agent(
    name="Freelancer Profile Manager",
    instructions="You coordinate the CV processing workflow by determining which specialist agents to use for parsing, enriching, and analyzing freelancer profiles. Route the CV data through appropriate specialists to create complete, high-quality freelancer profiles.",
    handoffs=[cv_parser_agent, profile_enrichment_agent, skills_extraction_agent, gap_analysis_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=cv_validation_guardrail),
    ],
) 
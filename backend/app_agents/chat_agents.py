"""
Chat and expert sourcing agent definitions
"""

from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from schemas.chat_schemas import ExpertSourcingOutput

# ---- Agent Definitions ----------------------------------------------------
guardrail_agent = Agent(
    name="Expert Sourcing Validator",
    instructions="Check if the user is requesting expert sourcing, matchmaking, or talent acquisition services.",
    output_type=ExpertSourcingOutput,
)

project_requirements_agent = Agent(
    name="Project Requirements Assistant",
    handoff_description="Specialist agent for helping project owners create comprehensive project descriptions",
    instructions="You help project owners articulate and develop their project requirements. Guide them through defining scope, timeline, budget, required skills, and deliverables to create a complete project description.",
)

project_refinement_agent = Agent(
    name="Project Refinement Specialist",
    handoff_description="Specialist agent for finalizing and polishing project descriptions",
    instructions="You help project owners refine and finalize their project descriptions. Identify missing information, suggest improvements, and ensure the project description is clear, complete, and attractive to potential freelancers.",
)

# ---- Guardrail Functions --------------------------------------------------
async def expert_sourcing_guardrail(ctx, agent, input_data):
    """Guardrail to ensure only expert sourcing requests are processed"""
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(ExpertSourcingOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_expert_sourcing,
    )

supervisor_agent = Agent(
    name="Expert Sourcing Supervisor",
    instructions="You coordinate the project submission workflow by determining which specialist agent to use based on the client's needs - helping create project requirements or refining and finalizing project descriptions.",
    handoffs=[project_refinement_agent, project_requirements_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=expert_sourcing_guardrail),
    ],
) 
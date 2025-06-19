# Agent Prompting Principles: State-of-the-Art Techniques (2025)

> A comprehensive reference of advanced prompting techniques for multi-agent systems, including the latest 2025 research and battle-tested patterns from OpenAI Agents SDK, CrewAI, and Anthropic Claude.
> Use this file when designing or reviewing prompts for any agent in this repository.

---

## ⚠️ **IMPORTANT: Our Standard Architecture Pattern**

**Before applying any prompting techniques below, understand our standardized agent development approach:**

We consistently implement a **dual-format architecture pattern** across all our agent implementations:

- **Input Processing**: **Jinja2 templates** generate **XML-formatted prompts** for consistent, structured input to agents. This approach provides clear prompt engineering capabilities with template inheritance, conditional logic, and variable interpolation while maintaining human-readable prompt structures.

- **Output Processing**: **Pydantic models** enforce **structured JSON outputs** from all agents, ensuring type safety, automatic validation, and predictable data contracts between agents and consuming systems.

This pattern allows us to maintain consistency across different frameworks while leveraging the strengths of both approaches - flexible, maintainable prompt templates on input and robust, validated data structures on output.

**Implementation Note**: All prompting techniques in this guide should be implemented within Jinja2 templates that output XML-structured prompts, with agent responses validated against Pydantic schemas for consistent data contracts.

---

## Table of Contents

### Anthropic Prompt Engineering Principles
1. [Anthropic Claude Best Practices](#1-anthropic-claude-best-practices)
2. [Prompt Templates & Variables](#2-prompt-templates--variables)
3. [Claude-Specific Techniques](#3-claude-specific-techniques)

### Foundation Techniques
4. [Prompt Engineering Overview](#4-prompt-engineering-overview)
5. [Chain of Thought (CoT)](#5-chain-of-thought-cot)
6. [ReAct: Reasoning + Acting](#6-react-reasoning--acting)
7. [Tree of Thoughts (ToT)](#7-tree-of-thoughts-tot)

### Advanced Techniques (2025)
8. [Self-Consistency & Multi-Path Reasoning](#8-self-consistency--multi-path-reasoning)
9. [Constitutional AI Prompting](#9-constitutional-ai-prompting)
10. [Meta-Prompting & Self-Reflection](#10-meta-prompting--self-reflection)
11. [Tool-Calling Optimization](#11-tool-calling-optimization)

### Multi-Agent Patterns
12. [Hierarchical Agent Prompting](#12-hierarchical-agent-prompting)
13. [Agent Handoff Patterns](#13-agent-handoff-patterns)
14. [Collaborative Agent Prompting](#14-collaborative-agent-prompting)

### Framework-Specific Optimizations
15. [OpenAI Agents SDK Best Practices](#15-openai-agents-sdk-best-practices)
16. [CrewAI Sequential Prompting](#16-crewai-sequential-prompting)
17. [Anthropic Claude Optimization](#17-anthropic-claude-optimization)

---

## 1. Anthropic Claude Best Practices

### Core Claude 4 Principles (Opus/Sonnet)
1. **Be explicit** – spell out formatting requirements, output length, etc.
2. **Add context & motivation** – tell Claude *why* a constraint matters.
3. **Use examples & detail** – the model follows provided patterns precisely.
4. **Format control** – prefer "do X" over "don't do Y", or wrap the desired area in XML tags.
5. **Think & reflect** – leverage `<thinking>` blocks or extended‑thinking to let Claude plan before acting.
6. **Parallel tool calls** – explicitly ask Claude to invoke multiple tools at once when tasks are independent.

### Be Clear, Direct & Detailed
Treat Claude like a brilliant but *brand‑new employee*: provide **context**, **precise goals**, and **step‑by‑step instructions**.
Golden rule: *If a colleague with no background would be confused, so will Claude*.

### Give Claude a Role (System Prompts)
Set the `system` message to something like "You are a **senior data‑scientist**…". Role prompting increases domain accuracy, enforces tone, and keeps the assistant focused.

### Prefill Claude's First Tokens
For non‑extended‑thinking modes you can start the assistant message with a stub (`{`, `[Sherlock Holmes]`, etc.) to:

* Force a specific output format
* Skip boiler‑plate preambles
* Remind the model to stay in character

---

## 2. Prompt Templates & Variables

Separate **fixed instructions** from **variable inputs** (user text, retrieved docs, etc.) using a template language (`{{variable}}` in the console). Benefits:

* Consistency across calls
* Easy A/B testing
* Version control on the stable part of the prompt

### Prompt Generator
A console tool that creates a *first draft* template: it identifies variables, proposes XML structure and injects best‑practice wording. Use it to defeat the "blank page" problem; then refine manually or with the Prompt Improver.

### Prompt Improver
Feeds an existing template (plus feedback & gold examples) through four stages: example identification → structured rewrite with XML → chain‑of‑thought enrichment → upgraded examples. The result is a more robust prompt ready for evaluation.

---

## 3. Claude-Specific Techniques

### Use XML Tags
Structure prompts (and sometimes responses) with semantic XML (`<instructions>`, `<example>`, `<data>` …). Advantages:

* Disambiguates sections
* Eases post‑processing
* Combines smoothly with other techniques (e.g. CoT inside `<thinking>`)

### Chain Complex Prompts
Break multi‑stage workflows into smaller prompts whose outputs feed the next step. Benefits: higher accuracy, easier debugging, possibility to parallelise independent subtasks, and self‑correction loops.

### Long‑Context Tips (200K tokens)
* Place **bulk documents first**, queries last.
* Tag every document and its metadata (`<documents><document index="1">…`).
* Ask Claude to **quote** relevant passages before analysing them.

### Extended‑Thinking Tips
Extended thinking grants Claude an internal scratch‑pad (≥ 1 024 tokens). Guidance:

* Start with the minimum thinking budget; scale up only if results need deeper reasoning.
* Prefer *high‑level* "think deeply" instructions first, then add step‑by‑step guidance if necessary.
* Few‑shot demonstrations still work—wrap them in `<thinking>` tags.
* Don't prefill inside extended‑thinking blocks; instead, steer via natural‑language instructions and chain prompts for verification steps.

---

## 4. Prompt Engineering Overview

Prompt engineering is *faster, cheaper* and easier to maintain than fine‑tuning. It should be your first line of attack whenever an evaluation fails for reasons that can be controlled with prompting (accuracy, style, compliance, etc.).

### Core Principles (2025)
* **Define success upfront** – know the metric you're trying to improve
* **Iterate from broadly effective → specialized** techniques
* **Maintain empirical tests** around every prompt to measure improvements
* **Layer techniques** – combine multiple patterns for complex reasoning
* **Optimize for specific frameworks** – different agent frameworks have different strengths

---

## 5. Chain of Thought (CoT)

For complex reasoning, instruct the agent to think **step-by-step**, breaking down problems into logical sequences.

### Basic CoT Pattern
```
Think through this step by step:
1. First, identify the key components
2. Then, analyze their relationships
3. Finally, synthesize a solution

Let me work through this systematically:
[Step-by-step reasoning here]
```

### Advanced CoT with XML Tags
```xml
<thinking>
Let me break this down:
1. Understanding the problem
2. Identifying constraints
3. Exploring solutions
4. Evaluating trade-offs
</thinking>

<answer>
Based on my analysis above...
</answer>
```

### When to Use CoT
- Complex logical reasoning tasks
- Multi-step calculations
- Decision-making with multiple factors
- Debugging agent behavior

---

## 6. ReAct: Reasoning + Acting

The ReAct pattern interleaves **reasoning** (thinking) with **acting** (tool usage), creating a loop that mimics human problem-solving.

### ReAct Framework Structure
```
Thought: [What I need to think about]
Action: [What tool/action to take]
Observation: [Result of the action]
Thought: [Analysis of the observation]
Action: [Next action based on new information]
...
Final Answer: [Conclusion]
```

### ReAct Implementation Example
```python
def react_agent_prompt():
    return """
You are an expert research agent. For each task, follow the ReAct pattern:

1. **Thought**: Analyze what you need to do
2. **Action**: Choose and execute a tool
3. **Observation**: Process the results
4. Repeat until you have enough information
5. **Final Answer**: Provide your conclusion

Available tools: web_search, document_analyzer, calculator

Example:
Thought: I need to find recent information about AI agent frameworks.
Action: web_search("AI agent frameworks 2025")
Observation: Found several articles about OpenAI Agents SDK and CrewAI...
Thought: I should analyze the technical details of these frameworks.
Action: document_analyzer("framework_comparison.pdf")
Observation: The document shows performance benchmarks...
Final Answer: Based on my research, the best frameworks are...
"""
```

### ReAct Best Practices
- **Clear thought boundaries**: Use explicit "Thought:" markers
- **Specific actions**: Choose precise tools for each step
- **Process observations**: Always analyze results before next action
- **Iterative refinement**: Build knowledge progressively

---

## 7. Tree of Thoughts (ToT)

Tree of Thoughts explores multiple reasoning paths simultaneously, evaluating and pruning paths based on their promise.

### ToT Pattern Structure
```
Problem: [Define the problem]

Path 1: [First approach]
├── Evaluation: [Assess this path]
├── Next steps: [If promising, continue]
└── Result: [Outcome]

Path 2: [Alternative approach]
├── Evaluation: [Assess this path]
├── Next steps: [If promising, continue]
└── Result: [Outcome]

Path 3: [Third approach]
├── Evaluation: [Assess this path]
├── Next steps: [If promising, continue]
└── Result: [Outcome]

Best Path: [Select most promising]
Final Solution: [Implement chosen approach]
```

### ToT Implementation
```python
def tree_of_thoughts_prompt():
    return """
Explore multiple solution paths for this problem:

1. **Generate 3-5 different approaches**
2. **Evaluate each path's viability (score 1-10)**
3. **Develop the top 2 paths further**
4. **Compare final solutions**
5. **Select the best approach**

For each path, consider:
- Feasibility
- Resource requirements
- Risk factors
- Expected outcomes

Structure your response as a decision tree.
"""
```

---

## 8. Self-Consistency & Multi-Path Reasoning

Generate multiple independent reasoning paths and select the most consistent answer.

### Self-Consistency Pattern
```python
def self_consistency_prompt():
    return """
Solve this problem using 3 different approaches:

**Approach 1**: [Method 1]
- Reasoning: [Step-by-step logic]
- Answer: [Result]

**Approach 2**: [Method 2]
- Reasoning: [Alternative logic]
- Answer: [Result]

**Approach 3**: [Method 3]
- Reasoning: [Third approach]
- Answer: [Result]

**Consistency Check**: Compare all answers
**Final Answer**: [Most consistent result with confidence level]
"""
```

### Benefits
- Reduces hallucinations
- Increases confidence in complex reasoning
- Identifies edge cases and errors
- Provides multiple validation paths

---

## 9. Constitutional AI Prompting

Build ethical guidelines and self-correction mechanisms into agent behavior.

### Constitutional Principles Template
```python
def constitutional_prompt():
    return """
You are an AI agent guided by these principles:

**Core Values**:
1. Accuracy: Provide truthful, well-sourced information
2. Helpfulness: Focus on user needs and goals
3. Harmlessness: Avoid harmful, biased, or inappropriate content
4. Transparency: Explain your reasoning and limitations

**Self-Correction Process**:
1. Initial response
2. Constitutional review: Does this align with my principles?
3. Revision if needed
4. Final response

**Red Lines** (Never cross):
- Providing false information as fact
- Generating harmful or illegal content
- Violating user privacy
- Making decisions beyond my authority
"""
```

### Constitutional Layers
- **Pre-response**: Check alignment before generating
- **Post-response**: Review and revise output
- **Meta-level**: Reflect on overall behavior patterns

---

## 10. Meta-Prompting & Self-Reflection

Enable agents to reason about their own reasoning processes and improve their prompts dynamically.

### Meta-Prompting Structure
```python
def meta_prompting_template():
    return """
**Task**: [Original task]

**Meta-Analysis**:
1. What type of problem is this?
2. What approaches would work best?
3. What are my constraints and capabilities?
4. How should I structure my response?

**Strategy Selection**:
Based on my analysis, I'll use: [chosen approach]
Because: [reasoning for choice]

**Execution**:
[Apply selected strategy]

**Self-Evaluation**:
- Did my approach work well?
- What could I improve?
- Should I try a different method?
"""
```

### Self-Reflection Patterns
```python
def self_reflection_prompt():
    return """
After completing the task, reflect on:

**Process Quality**:
- Was my reasoning sound?
- Did I consider all relevant factors?
- Were there any logical gaps?

**Output Quality**:
- Is my answer complete and accurate?
- Does it fully address the user's needs?
- Is it clearly communicated?

**Improvement Opportunities**:
- What could I have done better?
- What additional information would help?
- How can I optimize for similar future tasks?
"""
```

---

## 11. Tool-Calling Optimization

Maximize effectiveness of tool usage in agent workflows.

### Tool Selection Strategy
```python
def tool_calling_prompt():
    return """
**Tool Selection Framework**:

1. **Analyze Requirements**:
   - What information do I need?
   - What actions must I take?
   - What constraints exist?

2. **Map Tools to Tasks**:
   - Available tools: {tool_list}
   - Best tool for each subtask
   - Parallel vs sequential execution

3. **Execution Plan**:
   - Order of operations
   - Error handling strategy
   - Validation checkpoints

4. **Parallel Optimization**:
   - Which tools can run simultaneously?
   - How to aggregate results?
   - Dependency management
"""
```

### Tool Chaining Patterns
```python
def tool_chaining_example():
    return """
**Sequential Chain**: Tool A → Tool B → Tool C
- Use when output of one tool feeds into next
- Example: search → analyze → summarize

**Parallel Execution**: Tool A + Tool B + Tool C
- Use when tools are independent
- Example: multiple data sources, concurrent analysis

**Conditional Branching**: If/Then tool selection
- Use when tool choice depends on intermediate results
- Example: If search fails, try alternative sources

**Iterative Loops**: Repeat tool usage until condition met
- Use for refinement or convergence tasks
- Example: Iterative improvement cycles
"""
```

---

## 12. Hierarchical Agent Prompting

Structure complex multi-agent systems with clear roles and communication patterns.

### Supervisor-Worker Pattern
```python
def supervisor_agent_prompt():
    return """
You are a **Supervisor Agent** managing a team of specialist agents.

**Your Role**:
1. Break down complex tasks into subtasks
2. Assign subtasks to appropriate specialist agents
3. Coordinate agent interactions
4. Synthesize results into final output

**Available Specialists**:
- Research Agent: Information gathering and analysis
- Writing Agent: Content creation and editing
- Technical Agent: Code and system analysis
- Quality Agent: Review and validation

**Workflow**:
1. Analyze incoming request
2. Create execution plan
3. Delegate to specialists
4. Monitor progress
5. Integrate results
6. Quality check final output
"""
```

### Specialist Agent Template
```python
def specialist_agent_prompt(specialty):
    return f"""
You are a **{specialty} Specialist Agent** in a multi-agent team.

**Your Expertise**: {specialty}
**Your Role**: Handle all tasks related to your specialty domain

**Communication Protocol**:
- Accept tasks from Supervisor Agent
- Request clarification when needed
- Provide detailed results with confidence levels
- Escalate complex issues to Supervisor
- Collaborate with peer agents when beneficial

**Quality Standards**:
- Domain accuracy is paramount
- Provide evidence and reasoning
- Flag uncertainties and limitations
- Suggest improvements to process
"""
```

---

## 13. Agent Handoff Patterns

Seamless transfer of context and control between agents.

### Handoff Protocol Template
```python
def handoff_prompt():
    return """
**Agent Handoff Protocol**:

**Current Agent**: [Your identity and role]
**Handoff Trigger**: [Why transferring control]
**Target Agent**: [Who should handle next]

**Context Transfer**:
- **Task Summary**: [What we're trying to accomplish]
- **Progress Made**: [What's been completed]
- **Current State**: [Where we are now]
- **Next Steps**: [What needs to happen next]
- **Constraints**: [Important limitations or requirements]
- **Resources**: [Available tools and information]

**Handoff Decision**:
Based on [reasoning], I'm transferring control to [target agent] because [justification].

**Success Criteria**:
The handoff is successful when [specific conditions are met].
"""
```

### Context Preservation
```python
def context_preservation_prompt():
    return """
**Context Handoff Package**:

1. **Conversation History**: Key exchanges and decisions
2. **Task Evolution**: How requirements have changed
3. **Attempted Solutions**: What's been tried and results
4. **Current Hypotheses**: Working theories and assumptions
5. **Pending Questions**: Unresolved issues needing attention
6. **Resource Inventory**: Available tools, data, and capabilities
7. **Timeline**: Important deadlines and milestones
8. **Stakeholders**: Who needs to be informed of progress
"""
```

---

## 14. Collaborative Agent Prompting

Patterns for multiple agents working together on shared tasks.

### Consensus Building
```python
def consensus_agent_prompt():
    return """
**Collaborative Decision Making**:

**Your Role**: Participate in multi-agent consensus building

**Process**:
1. **Individual Analysis**: Form your initial position
2. **Position Sharing**: Present your viewpoint with reasoning
3. **Active Listening**: Consider other agents' perspectives
4. **Dialogue**: Engage constructively with differing views
5. **Synthesis**: Look for common ground and creative solutions
6. **Consensus Check**: Verify agreement on final decision

**Communication Guidelines**:
- Be clear and specific about your reasoning
- Acknowledge valid points from other agents
- Flag areas of uncertainty or disagreement
- Propose compromises when appropriate
- Signal when you've changed your position and why
"""
```

### Peer Review Pattern
```python
def peer_review_prompt():
    return """
**Peer Review Protocol**:

**Your Role**: Provide constructive feedback on peer agent work

**Review Dimensions**:
1. **Accuracy**: Are facts and logic sound?
2. **Completeness**: Are all requirements addressed?
3. **Clarity**: Is the output well-structured and understandable?
4. **Efficiency**: Could the approach be optimized?
5. **Risk Assessment**: What could go wrong?

**Feedback Structure**:
- **Strengths**: What works well?
- **Concerns**: What needs attention?
- **Suggestions**: Specific improvement recommendations
- **Overall Assessment**: Summary and recommendation

**Tone**: Professional, constructive, focused on improvement
"""
```

---

## 15. OpenAI Agents SDK Best Practices

Optimization patterns specific to the OpenAI Agents SDK framework.

### Function Tool Definition
```python
def openai_function_tool_prompt():
    return """
**Function Tool Best Practices**:

1. **Clear Descriptions**: Explain what the tool does and when to use it
2. **Precise Parameters**: Use specific types and detailed descriptions
3. **Error Handling**: Include error cases in tool description
4. **Examples**: Provide usage examples in docstrings

```python
@function_tool
def analyze_document(
    document_path: str,
    analysis_type: Literal["summary", "sentiment", "keywords"],
    max_length: int = 500
) -> str:
    '''
    Analyze a document using specified analysis type.

    Args:
        document_path: Path to document file
        analysis_type: Type of analysis to perform
        max_length: Maximum length of output

    Returns:
        Analysis results as formatted string

    Raises:
        FileNotFoundError: If document doesn't exist
        ValueError: If analysis_type is invalid
    '''
```
"""
```

### Agent Handoff Pattern
```python
def openai_handoff_prompt():
    return """
**OpenAI Agents SDK Handoff Pattern**:

```python
def create_handoff_agent():
    return Agent(
        name="coordinator",
        instructions='''
        You coordinate between specialist agents.
        Use handoffs to transfer complex tasks to specialists.
        Always provide complete context in handoff messages.
        ''',
        functions=[handoff_to_researcher, handoff_to_writer]
    )

def handoff_to_researcher(query: str, context: str) -> Handoff:
    '''Transfer research tasks to research specialist'''
    return Handoff(
        target="researcher",
        context=f"Research request: {query}\nContext: {context}"
    )
```

**Handoff Best Practices**:
- Include complete context
- Specify success criteria
- Set clear boundaries
- Plan return path
"""
```

---

## 16. CrewAI Sequential Prompting

Optimization for CrewAI's task-based sequential execution model.

### Task Definition Pattern
```python
def crewai_task_prompt():
    return """
**CrewAI Task Optimization**:

```python
research_task = Task(
    description='''
    Research the latest developments in AI agent frameworks.

    **Specific Requirements**:
    1. Focus on 2025 developments
    2. Include performance benchmarks
    3. Identify key differentiators
    4. Assess enterprise readiness

    **Output Format**:
    - Executive summary
    - Detailed findings
    - Recommendations

    **Success Criteria**:
    - At least 5 recent sources
    - Quantitative data where available
    - Clear actionable insights
    ''',
    agent=research_agent,
    expected_output="Comprehensive research report with actionable insights"
)
```

**Task Chaining Best Practices**:
- Clear input/output specifications
- Explicit success criteria
- Context preservation between tasks
- Error handling and fallback plans
"""
```

### Agent Role Definition
```python
def crewai_agent_roles():
    return """
**CrewAI Agent Role Optimization**:

```python
researcher = Agent(
    role='Senior Research Analyst',
    goal='Conduct thorough research and provide data-driven insights',
    backstory='''
    You are an experienced research analyst with expertise in technology
    trends and market analysis. You excel at finding reliable sources,
    synthesizing complex information, and identifying key insights that
    drive strategic decisions.
    ''',
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, analysis_tool]
)
```

**Role Definition Best Practices**:
- Specific, actionable roles
- Clear goal statements
- Rich backstory for context
- Appropriate tool assignments
- Delegation rules
"""
```

---

## 17. Anthropic Claude Optimization

Leverage Claude's unique capabilities for optimal agent performance.

### Extended Thinking Pattern
```python
def claude_extended_thinking():
    return """
**Claude Extended Thinking Optimization**:

For complex reasoning tasks, use extended thinking mode:

```python
prompt = '''
<thinking>
Let me work through this complex problem systematically:

1. Problem decomposition
2. Constraint analysis
3. Solution space exploration
4. Trade-off evaluation
5. Implementation planning
</thinking>

Based on my analysis above, here's my recommendation...
'''
```

**Extended Thinking Best Practices**:
- Start with minimum thinking budget
- Use high-level guidance first
- Add step-by-step instructions if needed
- Don't prefill thinking blocks
- Chain prompts for verification
"""
```

### XML Structure Optimization
```python
def claude_xml_patterns():
    return """
**Claude XML Structure Best Practices**:

```xml
<instructions>
You are a specialist agent focused on [domain].
Your task is to [specific goal].
</instructions>

<context>
<current_situation>
[Relevant background information]
</current_situation>

<constraints>
- [Important limitation 1]
- [Important limitation 2]
</constraints>
</context>

<task>
<primary_objective>[Main goal]</primary_objective>
<success_criteria>
- [Measurable outcome 1]
- [Measurable outcome 2]
</success_criteria>
</task>

<output_format>
<analysis>
[Your reasoning process]
</analysis>

<recommendation>
[Your final recommendation]
</recommendation>
</output_format>
```

**XML Benefits**:
- Clear section boundaries
- Improved parsing reliability
- Better context understanding
- Easier post-processing
"""
```

---

## Advanced Debugging Techniques

### Prompt Debugging Checklist
1. **Clarity Test**: Would a human understand this prompt?
2. **Specificity Check**: Are requirements precise and measurable?
3. **Context Validation**: Is all necessary information provided?
4. **Format Verification**: Is the desired output format clear?
5. **Edge Case Coverage**: What could go wrong?
6. **Tool Integration**: Are tool calls optimized?
7. **Multi-Agent Coordination**: Are handoffs smooth?

### Performance Optimization
```python
def optimization_checklist():
    return """
**Agent Performance Optimization**:

1. **Prompt Length**: Minimize while maintaining clarity
2. **Tool Efficiency**: Choose optimal tools for each task
3. **Parallel Execution**: Maximize concurrent operations
4. **Context Management**: Preserve only essential information
5. **Error Recovery**: Build robust fallback mechanisms
6. **Validation**: Implement quality checks at key points
7. **Monitoring**: Track performance metrics and improve iteratively
"""
```

---

## Quick Reference Guide

### When to Use Each Technique

| Technique | Best For | Complexity | Latency Impact |
|-----------|----------|------------|----------------|
| Chain of Thought | Complex reasoning | Medium | Medium |
| ReAct | Tool-heavy tasks | High | High |
| Tree of Thoughts | Multiple solutions | High | High |
| Self-Consistency | High-stakes decisions | Medium | High |
| Constitutional AI | Safety-critical tasks | Low | Low |
| Meta-Prompting | Dynamic adaptation | High | Medium |
| Tool Optimization | Performance critical | Medium | Low |

### Technique Combinations

**High-Accuracy Reasoning**: CoT + Self-Consistency + Validation
**Complex Problem Solving**: ReAct + Tree of Thoughts + Meta-Prompting
**Multi-Agent Coordination**: Hierarchical + Handoff + Consensus
**Production Safety**: Constitutional AI + Error Handling + Monitoring

Keep this reference handy when designing agent prompts for optimal performance and reliability.

---

## Anthropic Reference Order for Debugging

1. Prompt Generator
2. Be Clear, Direct & Detailed
3. Multishot Examples (not covered above but available)
4. Chain‑of‑Thought
5. XML Tags
6. System Role
7. Prefill
8. Chaining
9. Long‑Context / Extended‑Thinking

Keep this checklist handy whenever you craft or review a new prompt.

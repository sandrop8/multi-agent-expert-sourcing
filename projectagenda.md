# Multi-Agent Expert Sourcing - Project Agenda

## Overview
This document outlines the two major next steps for developing our multi-agent expert sourcing application, focusing on backend agent implementation and frontend protocol integration.

---

## 🎯 **Step 1: Multi-Agent Backend Implementation with OpenAI Agents SDK**

### **Objective**
Replace the single agent with a complete multi-agent system using the OpenAI Agents SDK example code. The SDK handles all complexity internally - we just need to integrate the provided code into our FastAPI backend.

### **Current Status**
- ✅ Basic single-agent chat functionality working
- ✅ FastAPI backend with CORS configuration
- ✅ Database integration for conversation storage
- ✅ Next.js frontend with real-time chat interface

### **Implementation: Direct Code Integration**

**What the SDK provides out-of-the-box:**
- ✅ Agent handoffs and routing
- ✅ Guardrail system with tripwire logic
- ✅ Structured output handling
- ✅ Automatic conversation management
- ✅ Built-in tracing and logging

**Target Architecture:**
```
User Input → Triage Agent → [Math Tutor | History Tutor] → Response
                ↓
         Guardrail Check (Homework Filter)
```

### **Complete Implementation Code**

**File: `backend/main.py` - Agent System Section:**

```python
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import asyncio

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)
```

### **Backend Changes Required**

**File: `backend/main.py`**

**Simple Changes:**
1. **Replace** single `assistant = Agent(...)` with the multi-agent system above
2. **Update** chat endpoint to use `triage_agent` instead of `assistant`
3. **Add** proper imports for `InputGuardrail` and `GuardrailFunctionOutput`
4. **Handle** guardrail exceptions in the chat endpoint

**Updated Chat Endpoint:**
```python
@app.post("/chat")
async def chat(req: ChatReq):
    """Run the multi-agent system, store conversation, return response."""
    try:
        print(f"🔍 Processing request: {req.prompt}")
        
        # Use triage_agent as entry point to multi-agent system
        result = await Runner.run(triage_agent, req.prompt)
        
        answer = result.final_output if result.final_output else "No response"
        print(f"✅ AI Response: {answer}")

        # Store in database (existing logic)
        with engine.begin() as conn:
            conn.execute(messages.insert(), [
                {"role": "user",      "content": req.prompt},
                {"role": "assistant", "content": answer},
            ])
        
        return {"answer": answer}
    
    except Exception as e:
        print(f"❌ Error in chat endpoint: {str(e)}")
        # Handle guardrail rejections gracefully
        if "guardrail" in str(e).lower():
            return {"answer": "Sorry, I can only help with homework-related questions."}
        raise HTTPException(500, str(e))
```

### **Testing Strategy**

**Test Cases:**
1. **Math Questions**: "What is 2+2?", "Solve for x: 2x + 5 = 15"
2. **History Questions**: "Who was the first president?", "When did WWII end?"
3. **Non-Homework Questions**: "What is life?", "Tell me a joke"

**Expected Behaviors:**
- Math questions → Routed to Math Tutor Agent
- History questions → Routed to History Tutor Agent  
- Non-homework → Blocked by guardrail with friendly message
- All handoffs and routing handled automatically by SDK

### **Success Criteria**
- [ ] Multi-agent system replaces single agent
- [ ] Math questions get routed to Math Tutor
- [ ] History questions get routed to History Tutor
- [ ] Non-homework questions are blocked by guardrail
- [ ] Frontend continues to work without changes
- [ ] OpenAI tracing shows agent handoffs and guardrail decisions

**Note:** No database schema changes needed initially - the existing `messages` table will continue to work. The SDK handles all agent coordination internally.

---

## 🚀 **Step 2: AG-UI Protocol Integration**

### **Objective** 
Evaluate and integrate the AG-UI protocol to enhance our React/Next.js frontend with standardized agent-UI communication, file upload capabilities, and improved user experience.

### **Current Assessment**

#### **What is AG-UI Protocol?**
- Open, lightweight, event-based protocol
- Standardizes AI agent ↔ frontend communication
- Provides real-time interactivity and state synchronization
- Supports human-in-the-loop collaboration
- Framework-agnostic but has specific integrations

#### **Key Benefits for Our Project:**
1. **Enhanced UX**: Better real-time agent interaction
2. **File Handling**: Built-in file upload/processing
3. **State Management**: Live state synchronization
4. **Standardization**: Protocol-based communication
5. **Extensibility**: Future-proof agent integration

### **Technical Feasibility Analysis**

#### **Compatibility with Current Stack**
- ✅ **React/Next.js**: AG-UI supports React integration
- ✅ **FastAPI Backend**: Protocol is backend-agnostic
- ✅ **OpenAI Agents**: Can work alongside our agent system
- ⚠️ **Learning Curve**: New protocol to implement

#### **Implementation Approach**

**Option A: Parallel Implementation**
- Keep current chat interface as fallback
- Implement AG-UI as enhanced mode
- Gradual migration and testing

**Option B: Full Migration**
- Replace current frontend communication
- Implement AG-UI as primary protocol
- More significant refactoring required

### **Implementation Plan**

#### **Phase 2.1: Research & Prototyping**

**Tasks:**
1. **Deep Dive Research**: Study AG-UI documentation and examples
2. **Compatibility Testing**: Test with our current OpenAI Agents setup
3. **Architecture Design**: Plan integration with existing backend
4. **Proof of Concept**: Simple AG-UI + React + FastAPI demo

**Questions to Answer:**
- How does AG-UI handle WebSocket connections?
- What's the learning curve for our current team?
- Are there any conflicts with our current architecture?
- What additional dependencies are required?

#### **Phase 2.2: Backend Protocol Adapter**

**New Component: `backend/ag_ui_adapter.py`**

**Responsibilities:**
- Translate between OpenAI Agents and AG-UI protocol
- Handle AG-UI event streams
- Manage WebSocket connections
- File upload/processing integration

**Architecture:**
```
Frontend (AG-UI) ↔ WebSocket ↔ AG-UI Adapter ↔ OpenAI Agents ↔ Database
```

#### **Phase 2.3: Frontend Enhancement**

**New Components:**
- AG-UI React integration components
- Enhanced chat interface with protocol features
- File upload/preview components
- Real-time state synchronization

**Files to Create/Modify:**
- `frontend/components/AgentChat.tsx` (AG-UI enabled)
- `frontend/lib/ag-ui-client.ts` (Protocol client)
- `frontend/hooks/useAgentCommunication.ts`

#### **Phase 2.4: Feature Implementation**

**Priority Features:**
1. **File Upload**: Document/image processing capabilities
2. **Real-time Streaming**: Enhanced message streaming
3. **Multi-modal Input**: Text, voice, file inputs
4. **Agent State Visualization**: Show agent thinking/processing
5. **Collaborative Features**: Multi-user support foundation

#### **Phase 2.5: Testing & Validation**

**Test Scenarios:**
- File upload → Agent processing → Response
- Real-time multi-agent conversations
- WebSocket connection stability
- Cross-browser compatibility
- Mobile responsiveness

### **Risk Assessment**

#### **Technical Risks**
- **Complexity**: AG-UI adds significant architecture complexity
- **Dependencies**: New protocol dependencies and maintenance
- **Performance**: Additional abstraction layers
- **Documentation**: Protocol is relatively new, limited examples

#### **Mitigation Strategies**
- **Phased Implementation**: Start with simple features
- **Fallback Options**: Keep current system as backup
- **Community Engagement**: Active participation in AG-UI community
- **Performance Monitoring**: Benchmark before/after implementation

### **Decision Framework**

#### **Proceed with AG-UI if:**
- [ ] Proof of concept shows clear benefits
- [ ] Integration complexity is manageable
- [ ] Performance impact is acceptable
- [ ] Community support is strong
- [ ] File handling features work seamlessly

#### **Alternative Approaches:**
- **Custom WebSocket Implementation**: Build our own real-time features
- **Existing Libraries**: Use established React libraries for enhanced UX
- **Hybrid Approach**: AG-UI for specific features, custom for others

---

## 📋 **Implementation Timeline**

### **Week 1-2: Step 1 Implementation**
- [ ] Multi-agent backend implementation
- [ ] Testing and debugging
- [ ] Basic frontend updates
- [ ] Documentation updates

### **Week 3: Step 2 Research**
- [ ] AG-UI protocol deep dive
- [ ] Compatibility assessment
- [ ] Architecture planning
- [ ] Proof of concept development

### **Week 4-5: Step 2 Implementation**
- [ ] Backend AG-UI adapter (if proceeding)
- [ ] Frontend protocol integration
- [ ] File upload feature implementation
- [ ] Comprehensive testing

### **Week 6: Integration & Polish**
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Documentation completion
- [ ] Deployment preparation

---

## 🎯 **Success Metrics**

### **Step 1 Success Indicators**
- Multiple agents handle different question types
- Guardrails effectively filter content
- Agent handoffs work seamlessly
- Database captures agent metadata
- OpenAI tracing shows complete flows

### **Step 2 Success Indicators**
- Real-time agent communication works
- File upload/processing functional
- Enhanced UI provides better UX
- Protocol integration is stable
- Performance meets requirements

---

## 📚 **Resources & References**

### **OpenAI Agents SDK**
- [Official Documentation](https://openai.github.io/openai-agents-python/)
- [GitHub Repository](https://github.com/openai/openai-agents-python)
- [Quickstart Guide](https://openai.github.io/openai-agents-python/quickstart/)

### **AG-UI Protocol**
- [GitHub Repository](https://github.com/ag-ui-protocol/ag-ui)
- [Documentation](https://github.com/ag-ui-protocol/docs)
- [Community Discussions](https://github.com/orgs/ag-ui-protocol/discussions)

### **Technical Stack**
- FastAPI, SQLAlchemy, OpenAI Agents SDK
- Next.js, React, TypeScript, Tailwind CSS
- PostgreSQL, WebSockets (for AG-UI)

---

*This agenda will be updated as we progress through implementation and learn more about the technologies involved.* 
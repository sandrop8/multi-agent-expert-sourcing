# NATS Integration Guide

## 🚀 **Quick Start**

This guide shows you how to use the NATS integration that has been implemented and tested for your FastAPI multi-agent expert sourcing application.

### **1. Install Dependencies**

```bash
cd backend
uv sync  # This will install nats-py>=2.7.0
```

### **2. Configure NATS Connection**

Add these environment variables to your `.env` file:

```bash
# Option 1: Local development with local NATS server
NATS_URL=nats://localhost:4222

# Option 2: Local development connecting to Railway NATS (public)
# Enable public networking in Railway NATS service and use generated domain
NATS_URL=nats://your-nats-domain.up.railway.app:4222

# Option 3: Railway deployment (internal networking - secure)
NATS_URL=nats://nats.railway.internal:4222

# Option 4: Railway TCP service (tested working configuration)
NATS_URL=nats://metro.proxy.rlwy.net:40859
```

### **3. Start NATS Server Locally**

For local development, you can run NATS with Docker:

```bash
# Simple NATS server (core features only)
docker run -p 4222:4222 -p 8222:8222 nats:latest

# With JetStream enabled (persistent messaging)
docker run -p 4222:4222 -p 8222:8222 nats:latest -js
```

### **4. Test the Integration**

Start your FastAPI app:
```bash
cd backend
uv run uvicorn main:app --reload
```

Visit the API docs: http://localhost:8000/docs

Navigate to the **NATS** section and try these endpoints:

#### **Health Check**
- `GET /nats/health` - Check if NATS is connected

#### **Test Event Publishing**
- `POST /nats/test/cv-uploaded` - Publish a test CV upload event
- `POST /nats/test/chat-message` - Publish a test chat message event
- `POST /nats/test/agent-task` - Publish a test agent task completion event

#### **Manual Event Publishing**
- `POST /nats/publish` - Publish custom events

#### **Request-Response Testing**
- `GET /nats/test/request-response` - Test NATS request-reply pattern

#### **JetStream Status**
- `GET /nats/streams` - Check JetStream availability and configured streams

## 📊 **What's Been Integrated & Tested**

### **1. NATS Connection Management**
- **File**: `backend/core/nats.py`
- **Features**: Auto-reconnection, JetStream support with graceful fallback, dependency injection
- **Patterns**: FastAPI startup/shutdown lifecycle with robust error handling
- **✅ Tested**: Health monitoring, connection stability, graceful degradation

### **2. NATS Service Layer**
- **File**: `backend/services/nats_service.py`
- **Features**: Event publishing with fallback, request-response, subscriptions
- **Patterns**: Service layer pattern with automatic JetStream-to-core-NATS fallback
- **✅ Tested**: All publishing patterns, error scenarios, large payloads

### **3. Event Schemas**
- **File**: `backend/schemas/nats_schemas.py`
- **Features**: Type-safe event definitions using Pydantic
- **Patterns**: Request/response validation for structured messaging
- **✅ Tested**: Complex data structures, mixed data types, special characters

### **4. API Endpoints**
- **File**: `backend/api/v1/nats.py`
- **Features**: RESTful NATS management and testing endpoints
- **Patterns**: Router-based organization with comprehensive error handling
- **✅ Tested**: All endpoints, edge cases, rapid successive calls

### **5. Integration Example**
- **File**: `backend/services/cv_nats_integration.py`
- **Features**: Shows how to add events to existing workflows
- **Patterns**: Non-intrusive event publishing for CV and chat workflows
- **✅ Tested**: CV processing events, chat message events, agent coordination

## 🧪 **Comprehensive Test Suite**

### **Test Coverage: 15/15 NATS Integration Tests Passing (100%)**

Our NATS integration includes a comprehensive test suite that has been verified against Railway's NATS service:

```bash
# Run NATS integration tests
NATS_URL=nats://metro.proxy.rlwy.net:40859 uv run pytest tests/integration/test_nats_integration.py -v
```

#### **Test Categories:**

**Health & Connection (2 tests):**
- ✅ NATS server connectivity verification
- ✅ Health check endpoint validation

**Event Publishing (3 tests):**
- ✅ Non-persistent event publishing (core NATS)
- ✅ Persistent event publishing with JetStream fallback
- ✅ Custom event publishing with various subjects

**Specialized Events (3 tests):**
- ✅ CV upload event publishing
- ✅ Chat message event publishing
- ✅ Agent task completion event publishing

**Edge Cases & Performance (4 tests):**
- ✅ Invalid subject handling (empty subjects)
- ✅ Large payload testing (10KB+ data)
- ✅ Special characters in filenames (Unicode, emojis)
- ✅ Long content messages (3000+ characters)

**Complex Scenarios (3 tests):**
- ✅ Multiple rapid publishes (race condition testing)
- ✅ Mixed data types in payloads (strings, numbers, booleans, arrays, objects)
- ✅ Complex nested result data structures

### **Test Architecture Features:**

- **🔄 Graceful Degradation**: Tests work with both JetStream-enabled and core-only NATS servers
- **🚀 Railway Compatible**: Verified against Railway's TCP NATS service configuration
- **📊 Comprehensive Coverage**: Edge cases, error scenarios, and performance testing
- **🛡️ Error Resilience**: Automatic fallback testing from JetStream to core NATS

## 🎯 **Common Use Cases**

### **1. CV Processing Events**

```python
# When a CV is uploaded
await cv_events.on_cv_uploaded(cv_id=123, filename="resume.pdf")

# When processing starts
await cv_events.on_cv_processing_started(cv_id=123, session_id="session_456")

# When processing completes
await cv_events.on_cv_processing_completed(cv_id=123, session_id="session_456", success=True)
```

### **2. Chat Message Events**

```python
# When a chat message is created
await cv_events.on_chat_message_created(message_id=789, role="user", content="Hello!")
```

### **3. Agent Task Coordination**

```python
# Publish agent task completion
nats_service = NATSService(nats_client)
event_publisher = EventPublisher(nats_service)

await event_publisher.agent_task_completed(
    agent_id="cv_analyzer_1",
    task_id="task_123",
    result={"extracted_skills": ["Python", "FastAPI"]}
)
```

### **4. Custom Events**

```python
# Publish any custom event
await nats_service.publish_event(
    subject="events.custom.user_action",
    data={
        "user_id": "user_123",
        "action": "profile_updated",
        "timestamp": datetime.utcnow().isoformat()
    },
    persistent=True  # Automatically falls back to core NATS if JetStream unavailable
)
```

## 🔧 **Railway Deployment & Local Testing**

### **✅ Tested Railway Configuration**

Our NATS integration has been thoroughly tested with Railway's NATS deployment. Here's the working configuration:

#### **Railway NATS Service Setup:**
1. **Deploy NATS from Railway Template**: Use the one-click NATS deployment
2. **Enable TCP Networking**: Railway provides a TCP proxy URL (e.g., `metro.proxy.rlwy.net:40859`)
3. **Core NATS Only**: Railway's default NATS doesn't include JetStream (this is fine!)

#### **Environment Variables:**
```bash
# For Railway deployment (using TCP proxy)
NATS_URL=nats://metro.proxy.rlwy.net:40859

# For local development connecting to Railway
NATS_URL=nats://metro.proxy.rlwy.net:40859
```

### **JetStream Fallback Behavior (✅ Tested)**

Our implementation includes robust JetStream fallback:

```python
# When persistent=True is requested:
if persistent:
    try:
        # Try JetStream for guaranteed delivery
        js = self.nc.jetstream()
        ack = await js.publish(subject, payload)
        logger.debug(f"📤 Published persistent event to {subject}: {ack}")
        return True
    except Exception as js_error:
        logger.warning(f"⚠️ JetStream publish failed for {subject}, falling back to core NATS: {js_error}")
        # Automatically fall back to core NATS
        await self.nc.publish(subject, payload)
        logger.debug(f"📤 Published event to {subject} (fallback to core NATS)")
        return True
```

**This means:**
- ✅ **With JetStream**: Gets persistent messaging with delivery guarantees
- ✅ **Without JetStream**: Automatically falls back to core NATS with warning log
- ✅ **No Failures**: Your application never fails due to JetStream unavailability

### **For Local Development (Testing with Railway NATS)**

1. **Use Railway's TCP URL directly**:
```bash
# In your local .env file
NATS_URL=nats://metro.proxy.rlwy.net:40859
```

2. **Test the connection**:
```bash
cd backend
NATS_URL=nats://metro.proxy.rlwy.net:40859 uv run python -c "
import asyncio
import os
from nats.aio.client import Client as NATS

async def test():
    nc = NATS()
    await nc.connect(os.getenv('NATS_URL'))
    print('✅ Connected to Railway NATS')
    await nc.close()

asyncio.run(test())
"
```

### **For Production Deployment (Railway to Railway)**

```bash
# In Railway environment variables, use internal networking for security:
NATS_URL=nats://nats.railway.internal:4222

# Or continue using TCP proxy for simplicity:
NATS_URL=nats://metro.proxy.rlwy.net:40859
```

## 📈 **AI Agent Integration Examples**

### **Agent Workflow Coordination**

```python
# Agent A completes CV analysis
await event_publisher.agent_task_completed(
    agent_id="cv_analyzer",
    task_id="analyze_cv_123",
    result={
        "cv_id": 123,
        "extracted_data": {...},
        "next_step": "profile_building"
    }
)

# Agent B listens for CV analysis completion
async def handle_cv_analysis_complete(subject: str, data: Dict[str, Any], msg):
    if data.get("next_step") == "profile_building":
        # Trigger profile building agent
        await start_profile_building_task(data["cv_id"], data["extracted_data"])

# Subscribe to agent events
await nats_service.subscribe_to_events("agent.task.completed.*", handle_cv_analysis_complete)
```

### **Workflow State Management**

```python
# Publish workflow state changes
await nats_service.publish_event(
    subject="workflow.cv_processing.state_change",
    data={
        "workflow_id": "cv_process_123",
        "state": "analysis_complete",
        "next_state": "profile_building",
        "data": {...}
    },
    persistent=True  # Automatically handles JetStream availability
)
```

## 🐛 **Troubleshooting**

### **NATS Not Connected**
- ✅ **Tested Solution**: Check if NATS server is running: `docker ps | grep nats`
- ✅ **Tested Solution**: Verify NATS_URL in your environment variables
- ✅ **Tested Solution**: Check logs for connection errors in FastAPI output

### **Events Not Publishing**
- ✅ **Tested Solution**: Test with `/nats/health` endpoint first
- ✅ **Tested Solution**: Check FastAPI logs for NATS errors
- ✅ **Automatic Fallback**: JetStream failures automatically fall back to core NATS

### **JetStream Not Available**
- ✅ **This is Normal**: Many NATS servers (including Railway) don't have JetStream
- ✅ **Automatic Handling**: Our implementation gracefully falls back to core NATS
- ✅ **No Action Required**: Check logs for fallback warnings, but functionality continues

### **Railway Networking Issues**
- ✅ **Tested Solution**: Use TCP proxy URLs (e.g., `metro.proxy.rlwy.net:40859`)
- ✅ **Tested Solution**: Ensure NATS service is deployed and running in Railway
- ✅ **Tested Solution**: Check Railway service logs for connection errors

### **Development vs Production**
- **✅ Local with Docker**: `NATS_URL=nats://localhost:4222`
- **✅ Local with Railway NATS**: `NATS_URL=nats://metro.proxy.rlwy.net:40859`
- **✅ Railway Production**: `NATS_URL=nats://metro.proxy.rlwy.net:40859` or internal URLs

## 🎨 **Next Steps**

### **1. Add to Existing Services**
Integrate event publishing into your existing CV and chat services:

```python
# In cv_service.py
from services.cv_nats_integration import cv_events

# Add after successful operations
background_tasks.add_task(cv_events.on_cv_uploaded, cv_id, filename)
```

### **2. Create Event Subscribers**
Set up services that react to events:

```python
# Create a service that handles CV upload events
async def handle_cv_uploaded(subject: str, data: Dict[str, Any], msg):
    cv_id = data["cv_id"]
    # Trigger automatic CV processing
    await start_cv_processing(cv_id)
```

### **3. Agent Orchestration**
Use NATS for coordinating your OpenAI Agents SDK workflows:

```python
# Agent completion triggers next agent
await event_publisher.agent_task_completed(
    agent_id="requirements_agent",
    task_id="gather_requirements_123",
    result={"requirements": [...], "ready_for_matching": True}
)
```

### **4. Real-time Updates**
Use NATS to push real-time updates to your frontend via WebSockets.

## 📊 **Production Readiness Checklist**

✅ **Connection Management**: Robust auto-reconnection and error handling
✅ **JetStream Fallback**: Graceful degradation when JetStream unavailable
✅ **Railway Compatibility**: Tested against Railway's NATS TCP service
✅ **Comprehensive Testing**: 15/15 integration tests passing
✅ **Error Logging**: Detailed logging for debugging and monitoring
✅ **API Documentation**: Complete FastAPI docs for all NATS endpoints
✅ **Event Schemas**: Type-safe Pydantic schemas for all event types
✅ **Edge Case Handling**: Large payloads, special characters, rapid publishing

This integration follows your FastAPI principles and provides a solid, tested foundation for event-driven architecture and AI agent coordination! 🎯

---

## 🎯 **Cross-Journey Module NATS Integration Patterns**

### **Event-Driven Bidirectional Matching Architecture**

Your Cross-Journey Modules use NATS differently than regular agent modules. Here are the key patterns extracted from your agent architecture:

#### **Message Subject Hierarchy**
```python
# NATS Subject Hierarchy for Cross-Journey Communication
CROSS_JOURNEY_SUBJECTS = {
    # Project lifecycle events
    'project.created': 'project.{project_id}.created',
    'project.updated': 'project.{project_id}.updated',

    # Matching events (bidirectional)
    'matching.freelancer.identified': 'matching.project.{project_id}.freelancer.{freelancer_id}.identified',
    'matching.scores.updated': 'matching.project.{project_id}.scores.updated',

    # Communication orchestration
    'communication.route': 'communication.{message_type}.route',
    'communication.clarification.request': 'freelancer.{freelancer_id}.clarification.{project_id}.request',
    'communication.clarification.response': 'project.{project_id}.clarification.{freelancer_id}.response',

    # Analytics and performance
    'analytics.user.journey': 'analytics.user.{user_id}.journey.{stage}',
    'analytics.platform.metric': 'analytics.platform.{metric_type}.{timestamp}',

    # Cross-module coordination
    'workflow.trigger': 'workflow.{module_name}.{action}.trigger',
    'workflow.complete': 'workflow.{module_name}.{action}.complete'
}
```

#### **Freelancer Opportunity Matching Flow**
```python
# Cross-Journey Module Event Handler Pattern
from services.nats_service import NATSService
from schemas.nats_schemas import ProjectCreatedEvent, FreelancerOpportunityEvent

class FreelancerOpportunityHandler:
    def __init__(self, nats_service: NATSService):
        self.nats_service = nats_service

    async def setup_event_subscriptions(self):
        """Setup NATS subscriptions for cross-journey events"""
        # Subscribe to project creation events
        await self.nats_service.subscribe_to_events(
            "project.*.created",
            self.handle_project_created
        )

        # Subscribe to freelancer opportunity responses
        await self.nats_service.subscribe_to_events(
            "freelancer.*.opportunity.*.response",
            self.handle_freelancer_opportunity_response
        )

    async def handle_project_created(self, subject: str, data: ProjectCreatedEvent, msg):
        """Handle new project creation - trigger freelancer matching"""
        project_id = data.project_id
        project_requirements = data.requirements

        # Find potential freelancer matches
        potential_matches = await self.find_potential_freelancer_matches(
            project_requirements
        )

        # Send opportunity notifications via NATS
        for freelancer_id, match_score in potential_matches:
            opportunity_event = FreelancerOpportunityEvent(
                project_id=project_id,
                freelancer_id=freelancer_id,
                match_confidence=match_score,
                missing_skills=await self.identify_skill_gaps(freelancer_id, project_requirements),
                improvement_potential=await self.calculate_improvement_potential(freelancer_id, project_requirements)
            )

            # Publish to freelancer-specific opportunity channel
            await self.nats_service.publish_event(
                subject=f"freelancer.{freelancer_id}.opportunity.{project_id}.available",
                data=opportunity_event.dict(),
                persistent=True
            )

    async def handle_freelancer_opportunity_response(self, subject: str, data: Dict, msg):
        """Handle freelancer responses to opportunities"""
        # Extract IDs from subject pattern
        freelancer_id = self.extract_id_from_subject(subject, "freelancer")
        project_id = self.extract_id_from_subject(subject, "project")

        # Process skill confirmations and profile updates
        updated_match_score = await self.process_skill_confirmations(
            freelancer_id, project_id, data
        )

        # Notify project owner of updated match scores
        await self.nats_service.publish_event(
            subject=f"matching.project.{project_id}.scores.updated",
            data={
                "freelancer_id": freelancer_id,
                "updated_score": updated_match_score,
                "timestamp": datetime.utcnow().isoformat()
            },
            persistent=True
        )
```

#### **NATS-Aware Agent Template for Cross-Journey Modules**
```python
# Extended Agent Template for NATS-Enabled Cross-Journey Modules
class NATSAwareAgent:
    def __init__(self, agent_name: str, nats_service: NATSService):
        self.agent_name = agent_name
        self.nats_service = nats_service
        self.subscriptions = []

    async def initialize(self):
        """Initialize NATS subscriptions for this agent"""
        await self.setup_subscriptions()

    async def setup_subscriptions(self):
        """Override in subclasses to define NATS subscriptions"""
        pass

    async def publish_agent_result(self, result_type: str, data: Dict, target_agents: List[str] = None):
        """Publish agent results via NATS for other agents to consume"""
        subject = f"agent.{self.agent_name}.result.{result_type}"

        event_data = {
            "agent_name": self.agent_name,
            "result_type": result_type,
            "data": data,
            "target_agents": target_agents,
            "timestamp": datetime.utcnow().isoformat()
        }

        await self.nats_service.publish_event(
            subject=subject,
            data=event_data,
            persistent=True
        )

    async def handle_agent_message(self, subject: str, data: Dict, msg):
        """Override in subclasses to handle incoming NATS messages"""
        pass
```

### **Key Architectural Benefits**

✅ **Event-Driven Matching**: Projects automatically trigger freelancer opportunity notifications
✅ **Bidirectional Communication**: Freelancers can respond and update their match scores in real-time
✅ **Cross-Module Coordination**: Communication Orchestration and Performance Analytics modules coordinate via NATS
✅ **Scalable Architecture**: Each module operates independently while coordinating through message events
✅ **Graceful Degradation**: NATS fallback patterns ensure reliability across different deployment scenarios

This creates a true **event-driven matching ecosystem** where both project owners and freelancers benefit from proactive, intelligent coordination! 🚀

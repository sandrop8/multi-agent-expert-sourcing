# Multi-Agent Expert Sourcing Demo

Find the live demo here: https://poetic-optimism-production.up.railway.app
A comprehensive multi-agent AI system showcasing **two different agent frameworks**: **OpenAI Agents SDK** for expert sourcing workflows and **CrewAI Framework** for company profiling, built with FastAPI backend and Next.js frontend.

## 📑 Table of Contents

- [🤖 Dual Agent Framework Architecture](#dual-agent-framework-architecture)
- [🎯 Multi-Agent Architecture](#-multi-agent-architecture)
  - [🏢 CrewAI Company Service Workflow](#-crewai-company-service-workflow-newly-implemented)
  - [🎯 OpenAI Agents SDK: Project Submission Track](#-openai-agents-sdk-project-submission-track-currently-implemented)
  - [👨‍💻 OpenAI Agents SDK: Freelancer Profile Track](#-openai-agents-sdk-freelancer-profile-track-planned-implementation)
- [💬 Example Chat Interface](#-example-chat-interface)
- [🔍 Agent Workflow Debugging](#-agent-workflow-debugging)
- [🛠️ Tech Stack](#️-tech-stack)
- [🧪 Testing Framework](#-testing-framework)
- [⚙️ Installation & Setup](#installation--setup)
- [🔧 Development Workflow](#development-workflow)
- [🚀 Production Deployment](#production-deployment)
- [📁 Project Structure](#project-structure)
- [💡 Development Tips](#-development-tips)
- [🤝 Contributing](#contributing)
- [📄 License](#license)

---

## Dual Agent Framework Architecture

This project demonstrates **two distinct agent frameworks** working in parallel to showcase different approaches to multi-agent AI systems:

### 🎯 **CrewAI Framework** - Company Profiling & Web Scraping
- **Purpose**: Automated company analysis through website scraping and data enrichment
- **Architecture**: Sequential crew of specialized agents with task handoffs
- **Tools**: Web scraping, search engines, and data synthesis capabilities
- **Use Case**: Company registration and service provider profiling

### 🤖 **OpenAI Agents SDK** - Expert Sourcing & CV Processing
- **Purpose**: Intelligent project management and freelancer profile generation
- **Architecture**: Hierarchical agent handoffs with supervisor coordination
- **Tools**: Guardrails, file processing, and structured data extraction
- **Use Cases**: Project requirement gathering and CV analysis workflows

---

### 🎯 **Multi-Agent Architecture**

This system demonstrates a **triple-track agent architecture** showcasing two different frameworks:
1. **CrewAI Framework** - Company service provider registration and profiling
2. **OpenAI Agents SDK** - Project owners seeking experts
3. **OpenAI Agents SDK** - Freelancers building their profiles

## 🏢 **CrewAI Company Service Workflow** *(Newly Implemented)*

### **Framework: CrewAI Sequential Crew Architecture**

### **Visual Architecture**

```mermaid
graph TD
    A[🏢 Company Registration] --> B[🔗 Website URL Input]
    B --> C[🚀 CrewAI Company Crew]

    C --> D[🕸️ Website Content Scraper]
    C --> E[🔍 Data Enrichment Researcher]
    C --> F[📊 Company Profile Synthesizer]

    D -->|Task 1: Scrape Content| G[📄 Raw Website Data]
    E -->|Task 2: Enrich Data| H[🔍 Missing Info Research]
    F -->|Task 3: Synthesize Profile| I[📋 Structured Company JSON]

    G --> J[🔄 Sequential Task Flow]
    H --> J
    I --> K[✅ Complete Company Profile]

    L[🛠️ ScrapeWebsiteTool] --> D
    M[🔍 SerperDevTool] --> E
    N[💡 AI Synthesis] --> F

    style A fill:#e1f5fe,color:#000000
    style C fill:#4fc3f7,color:#000000,stroke:#01579b,stroke-width:3px
    style D fill:#e8f5e8,color:#000000
    style E fill:#fff3e0,color:#000000
    style F fill:#f3e5f5,color:#000000
    style K fill:#c8e6c9,color:#000000
```

### **CrewAI Agent Roles & Responsibilities**

#### 🕸️ **Website Content Scraper** (Content Extraction Specialist)
- **Role**: Website content extraction using CrewAI's `ScrapeWebsiteTool`
- **Goal**: Extract key information about company services, mission, and contact details
- **Backstory**: Expert in navigating website structures to find relevant text-based content
- **Tools**: `ScrapeWebsiteTool` for comprehensive website content extraction
- **Output**: Raw text document containing all relevant website information

#### 🔍 **Data Enrichment Researcher** (Information Detective)
- **Role**: Research analyst that supplements scraped data with web searches
- **Goal**: Identify missing critical information (address, executives, services) and verify facts
- **Backstory**: Resourceful detective using search tools to fill information gaps
- **Tools**: `SerperDevTool` for targeted web searches (when API key available)
- **Output**: Report with missing information and verification sources

#### 📊 **Company Profile Synthesizer** (Data Integration Specialist)
- **Role**: Final analyst responsible for creating structured company profiles
- **Goal**: Transform raw and enriched data into clean, structured JSON objects
- **Backstory**: Meticulous data analyst creating polished, actionable company profiles
- **Tools**: AI-powered analysis and structuring (no external tools required)
- **Output**: Complete JSON profile with `company_name`, `services`, `location`, `contact_info`, `summary`

### **CrewAI Sequential Task Pipeline**

#### **Task 1: Initial Website Scraping**
- **Agent**: Website Content Scraper
- **Process**: Scrape provided URL focusing on services, mission, about section, contact info
- **CrewAI Features**: Tool integration with `ScrapeWebsiteTool`

#### **Task 2: Data Enrichment & Verification**
- **Agent**: Data Enrichment Researcher
- **Process**: Analyze scraped content, identify gaps, search for missing information
- **CrewAI Features**: Context from Task 1, web search tool integration

#### **Task 3: Profile Synthesis**
- **Agent**: Company Profile Synthesizer
- **Process**: Consolidate all information into structured JSON company profile
- **CrewAI Features**: Context from Tasks 1 & 2, structured output generation

---

## 🎯 **OpenAI Agents SDK: Project Submission Track** *(Currently Implemented)*

### **Framework: OpenAI Agents SDK Hierarchical Architecture**

### **Visual Architecture**

```mermaid
graph TD
    A[👤 Project Owner] --> B[🛡️ Expert Sourcing Validator]
    B -->|✅ Valid Request| C[🎯 Expert Sourcing Supervisor]
    B -->|❌ Invalid Request| D[🚫 Rejection Response]

    C -->|Initial Requirements| E[📝 Project Requirements Assistant]
    C -->|Refinement Needed| F[✨ Project Refinement Specialist]

    E --> G[📋 Detailed Project Description]
    F --> H[🎯 Polished Project Requirements]

    G --> I[📤 Coordinated Response]
    H --> I
    C --> I

    style A fill:#e1f5fe,color:#000000
    style C fill:#f3e5f5,color:#000000
    style B fill:#fff3e0,color:#000000
    style E fill:#e8f5e8,color:#000000
    style F fill:#e8f5e8,color:#000000
```

### **Agent Roles & Responsibilities**

#### 🎯 **Expert Sourcing Supervisor** (Main Coordinator)
- **Role**: Central orchestrator using OpenAI Agents SDK `handoffs` mechanism
- **Function**: Routes requests between project description specialists based on client needs
- **SDK Features**: Implements intelligent triage with `handoff_descriptions`
- **Workflow**: Coordinates project description creation process and ensures high-quality outputs

#### 🛡️ **Expert Sourcing Validator** (Input Guardrail)
- **Role**: Input validation using OpenAI Agents SDK `InputGuardrail`
- **Function**: Ensures requests relate to expert sourcing, matchmaking, or talent acquisition
- **SDK Features**: Uses `guardrail_function` with `tripwire_triggered` logic
- **Protection**: First line of defense, filtering irrelevant queries

#### 📝 **Project Requirements Assistant**
- **Role**: Requirements gathering specialist with domain-specific `instructions`
- **Function**: Helps project owners articulate and develop comprehensive project descriptions
- **SDK Features**: Uses conversational flows to guide requirement gathering
- **Expertise**: Project scope definition, timeline planning, skill requirement identification

#### ✨ **Project Refinement Specialist**
- **Role**: Project description optimization specialist with custom `instructions`
- **Function**: Finalizes and polishes project descriptions for maximum clarity and appeal
- **SDK Features**: Implements structured analysis and improvement suggestions
- **Output**: Complete, refined project descriptions ready for freelancer matching

---

## 👨‍💻 **OpenAI Agents SDK: Freelancer Profile Track** *(Planned Implementation)*

### **Framework: OpenAI Agents SDK Hierarchical Architecture**

### **Current Implementation Status**
✅ **Complete CV Processing System** - Fully implemented end-to-end CV processing with AI agents
- File upload interface with drag & drop support
- File validation (PDF, DOC, DOCX only, max 10MB)
- Secure binary storage in PostgreSQL database
- **NEW**: Complete AI agent workflow for CV processing
- **NEW**: Structured data extraction using OpenAI Files API
- **NEW**: Hierarchical agent handoffs with specialist processing
- Upload status feedback and comprehensive agent analysis
- CVs list endpoint for debugging and management

### **Visual Architecture**

```mermaid
graph TD
    A[👤 Freelancer] --> B[📎 CV Upload Interface]
    B --> C[🛡️ CV File Validator]
    C -->|✅ Valid CV| D[💾 PostgreSQL Storage]
    C -->|❌ Invalid File| E[🚫 Upload Error]

    D -->|stored_cv_id:123| F[🎯 Freelancer Profile Manager]
    F -->|Input Validation| G[🛡️ CV Content Validator]
    G -->|✅ Valid CV| H[📋 File Preparation Tool]

    H -->|Retrieve from DB| I[💾 Stored CV Data]
    I -->|Create temp file| J[📄 OpenAI Files API]

    F -->|Document Processing| K[📄 CV Parser Agent]
    F -->|Profile Building| L[👤 Profile Enrichment Agent]
    F -->|Skill Analysis| M[🧠 Skills Extraction Agent]
    F -->|Gap Assessment| N[🔍 Gap Analysis Agent]

    K -->|Extract with OpenAI| J
    K --> O[📊 Structured CV Data]
    L --> P[💼 Enhanced Profile]
    M --> Q[🏷️ Skill Tags & Levels]
    N --> R[📋 Missing Information Requests]

    O --> S[🎯 Profile Manager]
    P --> S
    Q --> S
    R --> S
    S --> T[📤 Complete Profile Response]

    J -->|Cleanup| U[🗑️ Temp File Removal]

    style A fill:#e1f5fe,color:#000000
    style B fill:#e8f5e8,color:#000000
    style C fill:#fff3e0,color:#000000
    style D fill:#e8f5e8,color:#000000
    style F fill:#f3e5f5,color:#000000
    style G fill:#fff3e0,color:#000000
    style H fill:#e3f2fd,color:#000000
    style I fill:#e8f5e8,color:#000000
    style J fill:#f0f4c3,color:#000000
    style K fill:#f0f0f0,color:#000000
    style L fill:#f0f0f0,color:#000000
    style M fill:#f0f0f0,color:#000000
    style N fill:#f0f0f0,color:#000000
```

### **Implemented Features**

#### 📎 **CV Upload & Storage System**
- **Role**: File upload and validation system for freelancer CVs
- **Features**: Secure file handling with comprehensive validation
- **Validation**: File type (PDF/Word), size limits (10MB), content validation
- **Storage**: Binary file storage in PostgreSQL with metadata tracking
- **UI**: Modern drag & drop interface with real-time feedback

#### 🔧 **CV Processing Tools**
- **prepare_cv_file_for_processing**: Validates stored CVs and prepares them for OpenAI processing
- **extract_cv_text_with_responses_api**: Comprehensive CV text extraction using OpenAI Files API
- **Stored CV Workflow**: Retrieves file data from Postgres, creates temporary files only for OpenAI processing
- **Automatic Cleanup**: Removes temporary files after OpenAI processing to minimize storage footprint

### **Implemented Agent Roles & Responsibilities**

#### 🎯 **Freelancer Profile Manager** (Main Coordinator) ✅ *Implemented*
- **Role**: Central orchestrator for freelancer profile creation workflow using hierarchical handoffs
- **SDK Features**: Uses OpenAI Agents SDK `handoffs` to route between 4 specialist CV processing agents
- **Function**: Coordinates complete CV processing from stored Postgres data to final profile
- **Workflow**: Processes `stored_cv_id:123` format, validates files, orchestrates specialist agents
- **Tools**: `prepare_cv_file_for_processing` for file validation and preparation

#### 🛡️ **CV Content Validator** (Input Guardrail) ✅ *Implemented*
- **Role**: Content validation using OpenAI Agents SDK `InputGuardrail` pattern
- **Function**: Validates stored CV identifiers and content relevance with enhanced permissive logic
- **SDK Features**: Implements `guardrail_function` with confidence scoring (0.6+ threshold)
- **Protection**: Ensures only valid CV processing requests enter the agent pipeline
- **Features**: Fallback validation, detailed logging, and error handling

#### 📄 **CV Parser Agent** (Document Specialist) ✅ *Implemented*
- **Role**: Document extraction specialist using OpenAI Files API for structured data extraction
- **Function**: Extracts personal info, work experience, education, skills, and certifications
- **SDK Features**: Uses `extract_cv_text_with_responses_api` tool with comprehensive JSON extraction
- **Tools**: Handles stored CV workflow, uploads to OpenAI Files API, returns structured JSON
- **Output**: Clean, structured professional data with confidence scoring

### 🧪 **CV Extraction Testing Results**

We have thoroughly tested our CV extraction system with real CV data and achieved impressive accuracy results. Our testing framework compares extracted data against manually curated ground truth data to ensure precision.

#### **Test Results Summary**
- **Overall Accuracy**: **90.6%** (14.5/16 personal info fields correctly extracted)
- **Test CV**: Janine Nel CV (nel.pdf)
- **Testing Framework**: Automated comparison against ground truth data matching PostgreSQL schema

#### **✅ Perfect Extractions (Exact Matches)**
The following fields were extracted with 100% accuracy:
- **First Name**: Janine
- **Last Name**: Nel
- **Phone**: Contact number extracted perfectly
- **Email**: Email address extracted perfectly
- **Professional Title**: "Sales Engineer" - exact match
- **Website URL**: Personal website extracted correctly
- **LinkedIn URL**: LinkedIn profile extracted correctly
- **Xing URL**: Xing profile extracted correctly
- **GitHub URL**: GitHub profile extracted correctly
- **Street Number**: Address number extracted correctly
- **PLZ/ZIP Code**: Postal code extracted correctly
- **City**: City name extracted correctly
- **Country**: Country extracted correctly

#### **🟡 Partial Matches (Areas for Improvement)**
- **Street Address**: Extracted "Pacific Ave" vs ground truth "1515 Pacific Ave" - missing house number integration
- **Languages**: Detected 2 out of multiple languages correctly - language proficiency detection needs refinement

#### **❌ Current Challenges**
- **Professional Summary**: Minor formatting differences in extracted text vs ground truth (spacing and capitalization)

#### **📊 Additional Metrics**
- **Employment History**: 2/2 positions extracted correctly
- **Education**: 1/1 education entry extracted correctly

#### **📄 Test CV Sample**
**Source Document**: [nel.pdf](backend/data/fictional_cvs/nel.pdf) - Janine Nel's CV used for extraction testing


#### **🎯 Development Status**
This demo showcases our multi-agent CV processing system in active development. While we achieved excellent results with **90.6% accuracy** on personal information extraction, we're continuously improving the system to handle edge cases like:
- **Language proficiency detection** - Working on better multilingual skill assessment
- **Address parsing precision** - Refining street address component extraction
- **Text formatting consistency** - Standardizing summary and description formatting

The high accuracy rate demonstrates the effectiveness of our OpenAI Files API integration and structured extraction approach, providing a solid foundation for freelancer profile generation.

#### 👤 **Profile Enrichment Agent** (Enhancement Specialist) 🚧 *WIP*
- **Role**: Profile optimization specialist that enhances extracted CV data
- **Function**: Creates professional summaries, highlights achievements, and optimizes presentations
- **SDK Features**: Uses advanced handoff descriptions and specialized instructions
- **Value-add**: Transforms raw CV data into compelling professional narratives
- **Process**: Receives structured data from CV Parser and enhances for freelancer profiles

#### 🧠 **Skills Extraction Agent** (Technical Specialist) 🚧 *WIP*
- **Role**: Skills analysis specialist with technical and soft skill identification
- **Function**: Categorizes technical skills, assesses proficiency levels, maps to industry standards
- **SDK Features**: Implements skill taxonomy matching with structured analysis
- **Output**: Standardized skill categories (technical, soft, languages) with confidence levels
- **Process**: Analyzes parsed CV data to extract comprehensive skill profiles

#### 🔍 **Gap Analysis Agent** (Assessment Specialist) 🚧 *WIP*
- **Role**: Profile completeness specialist that identifies missing crucial information
- **Function**: Analyzes processed profile data to find gaps in experience, skills, and qualifications
- **SDK Features**: Uses analytical instructions to provide actionable recommendations
- **Interactive**: Generates targeted suggestions for profile improvement and completeness
- **Output**: Detailed recommendations for enhancing freelancer profile quality

### 🔄 **Triple-Track Workflow Logic**

#### **CrewAI Company Service Flow** ✅ *(Implemented)*
1. **Company Registration** → Service provider submits website URL for analysis
2. **CrewAI Crew Initialization** → Sequential crew of 3 specialized agents activated
3. **Website Scraping** → Website Content Scraper extracts company information using `ScrapeWebsiteTool`
4. **Data Enrichment** → Data Enrichment Researcher fills gaps using `SerperDevTool` web searches
5. **Profile Synthesis** → Company Profile Synthesizer creates structured JSON company profile
6. **Sequential Task Flow** → Each task builds on previous results in CrewAI's sequential process
7. **Structured Output** → Final JSON with company details ready for service provider database

#### **OpenAI Agents SDK: Project Submission Flow** ✅ *(Implemented)*
1. **Input Validation** → Expert Sourcing Validator ensures project-related queries
2. **Intelligent Routing** → Expert Sourcing Supervisor routes to appropriate specialist
3. **Specialized Processing** → Requirements Assistant or Refinement Specialist guides project description creation
4. **Response Coordination** → Supervisor provides unified, high-quality project descriptions ready for freelancer matching

#### **OpenAI Agents SDK: Freelancer Profile Flow** 🚧 *(WIP)*
1. **File Upload & Storage** → CVs stored securely in PostgreSQL database with binary data
2. **Stored CV Processing** → Freelancer Profile Manager receives `stored_cv_id:123` identifier
3. **Input Validation** → CV Content Validator guardrail ensures valid CV processing requests
4. **File Preparation** → `prepare_cv_file_for_processing` tool validates and prepares stored CV
5. **Hierarchical Processing** → Manager hands off to 4 specialist agents in sequence:
   - CV Parser Agent extracts structured data using OpenAI Files API
   - Profile Enrichment Agent enhances with professional summaries
   - Skills Extraction Agent categorizes technical and soft skills
   - Gap Analysis Agent identifies missing information
6. **Data Integration** → Manager combines all specialist outputs into comprehensive profile
7. **Automatic Cleanup** → Temporary files removed after OpenAI processing

### 🏗️ **Multi-Framework Implementation Patterns**

This project demonstrates two distinct agent framework architectures:

#### **🎯 CrewAI Framework Patterns** (Company Service Track)
- **🔄 Sequential Crew Processing** - Agents work in sequence with task context sharing
- **🛠️ Specialized Tool Integration** - Each agent has specific tools (`ScrapeWebsiteTool`, `SerperDevTool`)
- **📋 Task-Driven Architecture** - Explicit task definitions with expected outputs
- **🤝 Context Sharing** - Later tasks receive context from previous task results
- **🎯 Role-Based Specialization** - Clear agent roles with specific backstories and goals

#### **🤖 OpenAI Agents SDK Patterns** (Project & Freelancer Tracks)
- **🎯 Hierarchical Structure** - Clear supervisor/specialist relationships using `handoffs`
- **🛡️ Guardrail Implementation** - Input validation with `InputGuardrail` and custom functions
- **🔄 Intelligent Triage** - Smart routing based on request analysis with `handoff_descriptions`
- **🎨 Modular Specialization** - Dedicated agents with specific `instructions` and `output_type`
- **📈 Extensible Architecture** - Easy addition of new specialist agents to either track

### 💬 **Example Chat Interface**

The system provides an intuitive chat interface where users can request expert sourcing services:

![Example Chat](example_project_chat.png)

*The Expert Sourcing Supervisor intelligently requests more details about project requirements when users ask for experts.*

### 🔍 **Agent Workflow Debugging**

Built-in tracing capabilities allow you to debug and monitor the complete agent workflow:

![Agent Traces](traces.png)

*Real-time traces show the complete agent execution flow: from Expert Sourcing Supervisor through guardrail validation to specialist agent handoffs.*

## 🛠️ **Tech Stack**

### **Backend**
#### **Core Framework & Runtime**
- **Python 3.9+** - Programming language with modern async support
- **FastAPI** - High-performance Python web framework with automatic API docs
- **Uvicorn** - Lightning-fast ASGI server with standard extras

#### **API Design & Architecture Standards**
- **RESTful API Design** - Following REST principles for resource-oriented architecture ([REST API Principles](backend/docs/REST_API_PRINCIPLES.md))
- **[FastAPI Best Practices](backend/docs/FASTAPI_PRINCIPLES.md)** - Comprehensive guide for SQLAlchemy ORM, Pydantic schemas, and project structure

#### **AI & Agent Systems**
- **OpenAI Agents SDK** (`openai-agents>=0.0.16`) - Hierarchical multi-agent orchestration for expert sourcing
- **CrewAI Framework** (`crewai>=0.130.0`) - Sequential crew-based agents for company profiling
- **CrewAI Tools** (`crewai-tools>=0.47.1`) - Specialized tools for web scraping and search
- **OpenAI API** (`openai>=1.30`) - GPT models and AI capabilities for both frameworks

#### **Database & Data**
- **PostgreSQL** - Robust relational database for conversation and CV storage
- **SQLAlchemy 2.x** (`sqlalchemy>=2.0`) - Database ORM and abstraction layer (migrating from Core to ORM pattern)
- **psycopg2-binary** - PostgreSQL database adapter

#### **Development & Utilities**
- **uv** - Ultra-fast Python package manager and resolver
- **python-dotenv** - Environment variable management
- **WebSockets** (`websockets>=11.0`) - Real-time communication support
- **python-multipart** - File upload and form data handling

### **Frontend**
#### **Core Framework & Runtime**
- **Next.js 15.0.0** - React framework with App Router and SSR
- **React 19.0.0** - Latest React with concurrent features
- **TypeScript 5.0+** - Type safety with strict mode configuration
- **Bun 1.0.0** - Ultra-fast JavaScript runtime and package manager

#### **Styling & UI Components**
- **Tailwind CSS 4.0.0** - Utility-first CSS framework (latest v4)
- **PostCSS 8.5.4+** - CSS post-processing with `@tailwindcss/postcss`
- **Autoprefixer 10.4.21+** - Automatic vendor prefixing
- **shadcn/ui** - Modern component library (Button, Card, Input, ScrollArea)
- **Radix UI** - Headless UI primitives for accessibility
- **Lucide React 0.377.0** - Beautiful icon system

#### **State & Communication**
- **Socket.io Client 4.8.1** - Real-time bidirectional communication
- **UUID 11.1.0** - Unique identifier generation

#### **Developer Experience**
- **ESLint 8.0+** - Code linting with Next.js configuration
- **Class Variance Authority** - Type-safe component variants
- **Tailwind Merge** - Intelligent class merging
- **CLSX** - Conditional CSS class composition

### **Package Management**
- **Backend**: `uv` with `uv.lock` for deterministic installs
- **Frontend**: `bun` with `bun.lockb` for ultra-fast dependency resolution

## 🧪 **Testing Framework**

**Comprehensive test suite with 220 total tests:**

### **Testing Stack**
- **Frontend Testing** - Jest + React Testing Library for UI components, interactions, accessibility (38/38 tests passing)
- **E2E Testing** - Playwright cross-browser testing across 5 browsers for full user journeys (75/75 tests passing)*
- **API Testing** - pytest + FastAPI TestClient for endpoints, database, agent systems (100/107 tests passing)**
  - **OpenAI Agents SDK Tests** - Expert sourcing and CV processing workflows (67 tests)
  - **CrewAI Framework Tests** - Company profiling and web scraping workflows (18 tests)
  - **Core API & Database Tests** - FastAPI endpoints and PostgreSQL integration (7 tests)
  - **NATS Integration Tests** - Event-driven messaging and communication system (15 tests)
- **Quality Assurance** - ESLint + TypeScript for code quality and type safety (0 errors)
- **Performance** - Coverage reports and build validation for production readiness

### **NATS Messaging Tests**
✅ **15/15 NATS Integration Tests Passing** (100% success rate)
- **Health & Connection** - NATS server connectivity and health monitoring (2 tests)
- **Event Publishing** - Core and persistent messaging with JetStream fallback (3 tests)
- **Specialized Events** - CV upload, chat message, and agent task events (3 tests)
- **Edge Cases & Performance** - Invalid subjects, large payloads, special characters (4 tests)
- **Complex Scenarios** - Rapid publishing, mixed data types, nested structures (3 tests)

**NATS Test Architecture:**
- 🔄 **Graceful Degradation** - Tests work with both JetStream-enabled and core NATS servers
- 🚀 **Railway Compatible** - Verified against Railway's TCP NATS service
- 📊 **Comprehensive Coverage** - Edge cases, error handling, and performance scenarios
- 🛡️ **Error Resilience** - Automatic fallback from JetStream to core NATS messaging

### **Testing Summary**
✅ **138/145 Core Tests Passing** (95% success rate) - *Backend + Frontend*
✅ **213/220 Total Tests Passing** (97% success rate) - *When backend running for E2E*
⚡ **Fast feedback loop** - Local testing before GitHub commits
🔄 **Pre-commit Ready** - Comprehensive validation across dual agent frameworks

*E2E tests require backend server running*
**7 backend tests skipped (long-running integration tests)*

### **Quick Start Testing**
```bash
# Run all tests
./test-all.sh

# Frontend only
cd frontend && bun run test

# Backend only
cd backend && uv run pytest tests/ -v
```

### **🪝 Pre-commit Hooks (Quality Assurance)**
**Automated quality checks before every commit:**
```bash
# Install pre-commit hooks (one-time setup)
cd backend && uv run pre-commit install

# Test hooks manually
cd backend && uv run pre-commit run --all-files

# Run full test suite manually
./test-all.sh
```

**Pre-commit automatically runs:**
- ✅ **Backend**: Ruff linting/formatting + quick tests
- ✅ **Frontend**: ESLint + TypeScript checking + quick tests
- ✅ **General**: File validation (YAML, JSON, trailing whitespace)

## 📚 **Documentation Structure**

### **📖 For Developers & LLMs**
- **[Project Testing Guide](ai_project_docs/TESTING.md)** - Current test status, project-specific setup, debugging for this application
- **[Generic CI/CD Setup Guide](ai_generic_docs/CI_CD_Setup.md)** - Reusable CI/CD pipeline patterns for Python + JavaScript projects

### **🎯 Quick Reference**
- **Current Project Testing**: See [TESTING.md](ai_project_docs/TESTING.md) for 205 tests status and project debugging
- **CI/CD Implementation**: See [CI_CD_Setup.md](ai_generic_docs/CI_CD_Setup.md) for pre-commit hooks, GitHub Actions, and deployment automation
- **LLM Guidance**: The CI/CD setup guide contains reusable patterns and best practices for implementing CI/CD in similar projects

---

## Installation & Setup

### Prerequisites
- **Python 3.9+** (verified minimum version from pyproject.toml)
- **Node.js 18+** (required for Bun compatibility)
- **PostgreSQL** database (local or cloud instance)
- **OpenAI API Key** (from OpenAI Platform)
- **uv** (Python package manager): `pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Bun** (JavaScript runtime): `npm install -g bun` or `curl -fsSL https://bun.sh/install | bash`

### Backend Setup

> **📋 Using Local Postgres.app?** See the detailed [Local Postgres Setup Guide](backend/LOCAL_POSTGRES_SETUP.md) for your specific configuration.

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies with uv:**
   ```bash
   uv sync
   ```

3. **Configure environment variables:**

   **Option A: Standard PostgreSQL setup**
   ```bash
   # Create .env file in backend directory
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   echo "PG_URL=postgresql://username:password@localhost:5432/database_name" >> .env
   ```

   **Option B: Using local Postgres.app (port 54323)**
   ```bash
   # For Postgres.app users, see LOCAL_POSTGRES_SETUP.md for detailed setup
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   echo "PG_URL=postgresql://$(whoami)@localhost:54323/expert" >> .env
   ```

4. **Run the development server:**
   ```bash
   uv run uvicorn main:app --reload
   ```

   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies with Bun:**
   ```bash
   bun install
   ```

3. **Run the development server:**
   ```bash
   bun dev
   ```

   Frontend will be available at `http://localhost:3000`

## Development Workflow

### 🛠️ Build System
This project uses **Makefiles** for standardized development workflows:
- **Root Makefile**: Cross-service orchestration (`make dev-all`, `make install-all`)
- **Backend Makefile**: Python/uv specific commands (`make dev`, `make test-db`)
- **Frontend Makefile**: Bun/Next.js specific commands (`make dev`, `make build`)

### Starting Both Services

**Option 1: Using Makefiles (Recommended)**
```bash
# From project root
make dev-all          # Start both services
make dev-backend      # Backend only
make dev-frontend     # Frontend only

# Service-specific commands
cd backend && make help
cd frontend && make help
```

**Option 2: Manual commands**
```bash
# Terminal 1 - Backend
cd backend && uv run uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend && bun dev
```

### API Endpoints

#### **CrewAI Framework Endpoints**
- **POST** `/company/register` - Register company service provider (triggers CrewAI crew workflow)

#### **OpenAI Agents SDK Endpoints**
- **POST** `/chat` - Send message to AI agent (expert sourcing workflow)
- **GET** `/history?limit=20` - Retrieve conversation history
- **POST** `/upload-cv` - Upload CV files (PDF/Word, max 10MB)
- **GET** `/cvs` - List uploaded CVs (debugging/management)

#### **General**
- **GET** `/docs` - FastAPI automatic documentation

### Environment Variables

**Backend (`backend/.env`):**
- `OPENAI_API_KEY` - Your OpenAI API key (required for both frameworks)
- `SERPER_API_KEY` - Serper API key for web search (optional, for CrewAI enhanced search)
- `PG_URL` - PostgreSQL connection string

**Frontend (environment variables):**
- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)

## Production Deployment

### Backend (Railway/Render/Heroku)
1. Set environment variables in platform
2. Connect PostgreSQL addon
3. Deploy with `uv run uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel/Netlify)
1. Set `NEXT_PUBLIC_API_URL` to production backend URL
2. Deploy with `bun build`

## Project Structure

```
multi-agent-expert-sourcing/
├── backend/                      # FastAPI backend
│   ├── main.py                  # Main application with multi-agent system
│   ├── pyproject.toml           # Python dependencies (uv)
│   ├── uv.lock                  # Dependency lock file
│   ├── test_db.py               # Database connection test
│   ├── LOCAL_POSTGRES_SETUP.md  # Local Postgres.app setup guide
│   └── .env                     # Environment variables
├── frontend/                    # Next.js frontend
│   ├── app/
│   │   ├── page.tsx            # Main chat interface
│   │   ├── test-styles/         # Tailwind test page
│   │   └── globals.css         # Global styles (Tailwind v4)
│   ├── components/
│   │   └── ui/                 # shadcn/ui components
│   │       ├── button.tsx      # Button component
│   │       ├── card.tsx        # Card component
│   │       ├── input.tsx       # Input component
│   │       └── scroll-area.tsx # ScrollArea component
│   ├── lib/utils.ts            # Utility functions
│   ├── package.json            # Node dependencies (Bun)
│   ├── bun.lockb               # Bun lock file
│   ├── postcss.config.js       # PostCSS configuration (Tailwind v4)
│   ├── components.json         # shadcn/ui configuration
│   ├── next.config.js          # Next.js configuration
│   ├── tsconfig.json           # TypeScript configuration
│   ├── tailwind-test.js        # Tailwind configuration test
│   └── TAILWIND_DEBUG_GUIDE.md # Tailwind v4 debugging guide
├── example_chat.png            # Example chat interface
├── traces.png                  # Agent workflow traces
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

## 🔧 Development Tips

- **Quick Start**: `make help` (root) | `cd backend && make help` | `cd frontend && make help`
- **Dependencies**: `make install-all` | `cd backend && make install` | `cd frontend && make install`
- **Development**: `make dev-all` for both services | `make dev-backend` | `make dev-frontend`
- **Testing**: `make test-all` | `cd backend && make test` | `cd frontend && make test`
- **Cleanup**: `make clean-all` | `cd backend && make clean` | `cd frontend && make clean`
- **Debugging**: Browser DevTools (frontend) | Terminal output (backend)

### 🆘 Need Help?
- **Testing Issues**: See [Testing Documentation](TESTING.md) troubleshooting section
- **Styling Issues**: See [Tailwind Debug Guide](frontend/TAILWIND_DEBUG_GUIDE.md)
- **Database Issues**: Check [Local Postgres Setup](backend/LOCAL_POSTGRES_SETUP.md)
- **General Setup**: Verify environment variables and dependency installation

## Contributing

This is just an exmaple repo to demonstrate the implementation of Agent Frameworks like Open AI's Agent SDK.
It is not under active development.

## License

This project is licensed under the MIT License.
# Test commit

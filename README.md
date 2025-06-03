# Multi-Agent Expert Sourcing

A modular, hierarchical multi-agent AI system that demonstrates intelligent expert sourcing workflows using OpenAI Agents SDK with FastAPI backend and Next.js frontend.

## OpenAI Agents SDK Framework

This project showcases a sophisticated multi-agent system built with the OpenAI Agents SDK, featuring:

### 🎯 **Multi-Agent Architecture**

This system demonstrates a sophisticated dual-track agent architecture supporting both **Project Owners** seeking experts and **Freelancers** building their profiles.

## 🏢 **Project Submission Track** *(Currently Implemented)*

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
    
    style A fill:#e1f5fe
    style C fill:#f3e5f5
    style B fill:#fff3e0
    style E fill:#e8f5e8
    style F fill:#e8f5e8
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

## 👨‍💻 **Freelancer Profile Track** *(Planned Implementation)*

### **Visual Architecture**

```mermaid
graph TD
    A[👤 Freelancer] --> B[📎 CV Upload]
    B --> C[🛡️ CV Content Validator]
    C -->|✅ Valid CV| D[🎯 Freelancer Profile Manager]
    C -->|❌ Invalid File| E[🚫 Upload Error]
    
    D -->|Document Processing| F[📄 CV Parser Agent]
    D -->|Profile Building| G[👤 Profile Enrichment Agent]
    D -->|Skill Analysis| H[🧠 Skills Extraction Agent]
    D -->|Gap Assessment| I[🔍 Gap Analysis Agent]
    
    F --> J[📊 Structured CV Data]
    G --> K[💼 Enhanced Profile]
    H --> L[🏷️ Skill Tags & Levels]
    I --> M[📋 Missing Information Requests]
    
    J --> N[🎯 Profile Manager]
    K --> N
    L --> N
    M --> N
    N --> O[📤 Complete Profile Response]
    
    style A fill:#e1f5fe
    style D fill:#f3e5f5
    style C fill:#fff3e0
    style F fill:#e8f5e8
    style G fill:#e8f5e8
    style H fill:#e8f5e8
    style I fill:#e8f5e8
```

### **Planned Agent Roles & Responsibilities**

#### 🎯 **Freelancer Profile Manager** (Main Coordinator)
- **Role**: Central orchestrator for freelancer profile creation workflow
- **SDK Features**: Uses OpenAI Agents SDK `handoffs` to route between CV processing agents
- **Function**: Coordinates CV parsing, profile enrichment, and gap analysis
- **Workflow**: Ensures complete, high-quality freelancer profiles

#### 🛡️ **CV Content Validator** (Input Guardrail)
- **Role**: File and content validation using `InputGuardrail`
- **Function**: Validates CV file format, content relevance, and completeness
- **SDK Features**: Implements `guardrail_function` with file type and content checks
- **Protection**: Ensures only valid CVs enter the processing pipeline

#### 📄 **CV Parser Agent** (Document Specialist)
- **Role**: Document extraction specialist with structured `output_type`
- **Function**: Extracts work experience, education, certifications, and contact info
- **SDK Features**: Uses Pydantic models for structured CV data extraction
- **Output**: Clean, structured professional history data

#### 👤 **Profile Enrichment Agent** (Enhancement Specialist)
- **Role**: Profile optimization specialist with custom `instructions`
- **Function**: Enhances basic CV data with professional summaries and achievements
- **SDK Features**: Uses advanced prompt engineering for profile optimization
- **Value-add**: Creates compelling professional narratives from raw CV data

#### 🧠 **Skills Extraction Agent** (Technical Specialist)
- **Role**: Skills analysis specialist with domain knowledge
- **Function**: Identifies technical skills, tools, and proficiency levels
- **SDK Features**: Implements skill taxonomy matching with confidence scoring
- **Output**: Standardized skill tags with proficiency levels

#### 🔍 **Gap Analysis Agent** (Assessment Specialist)
- **Role**: Profile completeness specialist with interactive capabilities
- **Function**: Identifies missing information crucial for project matching
- **SDK Features**: Uses conversational flows to request additional details
- **Interactive**: Generates targeted questions for profile completion

### 🔄 **Dual-Track Workflow Logic**

#### **Project Submission Flow**
1. **Input Validation** → Expert Sourcing Validator ensures project-related queries
2. **Intelligent Routing** → Expert Sourcing Supervisor routes to appropriate specialist
3. **Specialized Processing** → Requirements Assistant or Refinement Specialist guides project description creation
4. **Response Coordination** → Supervisor provides unified, high-quality project descriptions ready for freelancer matching

#### **Freelancer Profile Flow** *(Planned)*
1. **File Validation** → CV Content Validator ensures valid CV uploads
2. **Workflow Orchestration** → Freelancer Profile Manager coordinates processing
3. **Parallel Processing** → Multiple specialists extract different data aspects
4. **Gap Analysis** → Interactive agent identifies missing profile elements
5. **Profile Assembly** → Manager combines all data into complete freelancer profile

### 🏗️ **OpenAI Agents SDK Implementation Patterns**

Both tracks demonstrate key SDK concepts:
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

#### **AI & Agent System**
- **OpenAI Agents SDK** (`openai-agents>=0.0.16`) - Multi-agent orchestration framework
- **OpenAI API** (`openai>=1.30`) - GPT models and AI capabilities

#### **Database & Data**
- **PostgreSQL** - Robust relational database for conversation storage
- **SQLAlchemy Core 2.x** (`sqlalchemy>=2.0`) - Database abstraction layer for schema and queries
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

**Comprehensive test suite with 46 tests across frontend and backend:**

### **Quick Stats**
- ✅ **46 Total Tests** - 37 Frontend + 9 Backend
- 🎯 **95% Success Rate** - Production-ready quality
- ⚡ **< 30 seconds** - Fast feedback loop
- 🔄 **Pre-commit Ready** - Local testing before GitHub

### **Testing Stack**
```
Frontend: Jest + React Testing Library + Playwright
Backend:  pytest + FastAPI TestClient + Coverage
E2E:      Cross-browser testing with Playwright
Quality:  ESLint, TypeScript, Coverage Reports
```

### **Test Coverage**
- **Component Testing** - UI components, interactions, accessibility
- **Integration Testing** - API calls, user workflows, error handling  
- **E2E Testing** - Full user journeys across browsers
- **API Testing** - Endpoints, database, agent system
- **Build Testing** - TypeScript compilation, production builds

### **Quick Start Testing**
```bash
# Run all tests
./test-all.sh

# Frontend only
cd frontend && bun run test

# Backend only  
cd backend && uv run pytest tests/test_simple.py -v
```

📚 **Detailed Documentation:**
- [🚀 Quick Start Testing Guide](QUICK_START_TESTING.md) - Ready to test immediately
- [📖 Complete Testing Documentation](TESTING.md) - Comprehensive setup and best practices

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

### Starting Both Services

**Option 1: Manual (Recommended for development)**
```bash
# Terminal 1 - Backend
cd backend
uv run uvicorn main:app --reload

# Terminal 2 - Frontend  
cd frontend
bun dev
```

**Option 2: Using scripts (future enhancement)**
```bash
# From project root
bun run dev:all
```

### API Endpoints

- **POST** `/chat` - Send message to AI agent
- **GET** `/history?limit=20` - Retrieve conversation history
- **GET** `/docs` - FastAPI automatic documentation

### Environment Variables

**Backend (`backend/.env`):**
- `OPENAI_API_KEY` - Your OpenAI API key
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

- **Dependencies**: `uv add package_name` (Python) | `bun add package_name` (Node.js)
- **Auto-reload**: Backend (`--reload` flag) | Frontend (`bun dev`)
- **Debugging**: Browser DevTools (frontend) | Terminal output (backend)
- **Testing**: Run `./test-all.sh` before commits for quality assurance

### 🆘 Need Help?
- **Testing Issues**: See [Quick Start Testing](QUICK_START_TESTING.md) troubleshooting
- **Styling Issues**: See [Tailwind Debug Guide](frontend/TAILWIND_DEBUG_GUIDE.md)
- **Database Issues**: Check [Local Postgres Setup](backend/LOCAL_POSTGRES_SETUP.md)
- **General Setup**: Verify environment variables and dependency installation

## Contributing

This is just an exmaple repo to demonstrate the implementation of Agent Frameworks like Open AI's Agent SDK.
It is not under active development.

## License

This project is licensed under the MIT License. 
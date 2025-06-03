# Multi-Agent Expert Sourcing

A modular, hierarchical multi-agent AI system that demonstrates intelligent expert sourcing workflows using OpenAI Agents SDK with FastAPI backend and Next.js frontend.

## OpenAI Agents SDK Framework

This project showcases a sophisticated multi-agent system built with the OpenAI Agents SDK, featuring:

### 🎯 **Agent Architecture**

#### **Expert Sourcing Supervisor** (Main Coordinator)
The central orchestrator that routes requests to specialized agents based on client needs. Uses intelligent triage to determine workflow paths and coordinates the entire expert sourcing process.

#### **Expert Sourcing Validator** (Guardrail Agent)
Validates incoming requests to ensure they relate to expert sourcing, matchmaking, or talent acquisition services. Acts as the first line of defense, filtering out irrelevant queries and maintaining system focus.

#### **Expert Search & Matchmaking Specialist**
Specialized agent for finding and matching experts to specific project requirements. Analyzes project needs, search criteria, and provides intelligent recommendations for expert selection and matchmaking.

#### **CV Parsing & Profile Enrichment Specialist**
Dedicated agent for CV analysis and expert profile enhancement. Extracts key skills, experience, and qualifications to create comprehensive expert profiles and enriched talent data.

### 🔄 **Agent Workflow Logic**

1. **Request Validation**: Expert Sourcing Validator checks if the request is within scope
2. **Intelligent Routing**: Expert Sourcing Supervisor determines the appropriate specialist
3. **Specialized Processing**: Either Expert Search or CV Parsing agent handles the specific task
4. **Guardrail Protection**: Non-expert-sourcing requests are gracefully rejected
5. **Response Coordination**: Supervisor ensures consistent, high-quality responses

This demonstrates key agent framework concepts:
- **Hierarchical Agent Structure** - Clear supervisor/specialist relationships
- **Guardrail Implementation** - Input validation and scope protection  
- **Intelligent Triage** - Smart routing based on request analysis
- **Modular Specialization** - Dedicated agents for specific domains
- **Extensible Architecture** - Easy to add new specialist agents

### 💬 **Example Chat Interface**

The system provides an intuitive chat interface where users can request expert sourcing services:

![Example Chat](example_chat.png)

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
- [🎨 Tailwind CSS v4 Debug Guide](frontend/TAILWIND_DEBUG_GUIDE.md) - Styling framework troubleshooting

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

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## License

This project is licensed under the MIT License. 
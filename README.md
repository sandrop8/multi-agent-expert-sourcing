# Multi-Agent Expert Sourcing

A chat application with FastAPI backend using OpenAI Agents SDK and Next.js frontend.

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **OpenAI Agents SDK** - AI agent functionality
- **PostgreSQL** - Database for conversation history
- **SQLAlchemy 2.x** - Database ORM
- **uv** - Fast Python package manager

### Frontend  
- **Next.js 15** - React framework
- **React 19** - Latest React features
- **Tailwind CSS v4** - Styling
- **shadcn/ui** - UI component library
- **TypeScript** - Type safety
- **Bun** - Fast JavaScript runtime and package manager

## Installation & Setup

### Prerequisites
- **Python 3.11+** 
- **Node.js 20+** (for Bun)
- **PostgreSQL** database
- **OpenAI API Key**
- **uv** (Python package manager): `pip install uv`
- **Bun** (JavaScript runtime): `npm install -g bun`

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

3. **Environment is already configured:**
   - `.env.local` points to `http://localhost:8000` (backend)

4. **Run the development server:**
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

**Frontend (`frontend/.env.local`):**
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
│   ├── main.py                  # Main application
│   ├── pyproject.toml           # Python dependencies (uv)
│   ├── test_db.py               # Database connection test
│   ├── LOCAL_POSTGRES_SETUP.md  # Local Postgres.app setup guide
│   └── .env                     # Environment variables
├── frontend/                    # Next.js frontend
│   ├── app/
│   │   ├── page.tsx            # Main chat page
│   │   └── globals.css         # Global styles
│   ├── components/ui/          # shadcn/ui components
│   ├── lib/utils.ts            # Utility functions
│   ├── package.json            # Node dependencies (Bun)
│   ├── tailwind.config.js      # Tailwind configuration
│   ├── next.config.js          # Next.js configuration
│   ├── tsconfig.json           # TypeScript configuration
│   └── .env.local              # Environment variables
├── .gitignore                  # Git ignore rules
└── README.md                   # Main project documentation
```

## Troubleshooting

### Common Issues

**Backend not starting:**
- Check Python version: `python --version` (needs 3.11+)
- Verify environment variables in `.env`
- Ensure PostgreSQL is running and accessible
- **Local Postgres.app users**: See [LOCAL_POSTGRES_SETUP.md](backend/LOCAL_POSTGRES_SETUP.md) for specific troubleshooting

**Frontend not building:**
- Check Node.js version: `node --version` (needs 20+)
- Clear cache: `bun install --force`
- Verify backend is running on correct port

**API connection issues:**
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`
- Verify backend is accessible from frontend
- Check CORS settings if needed

### Development Tips

- Use `uv add package_name` to add Python dependencies
- Use `bun add package_name` to add Node.js dependencies  
- Backend auto-reloads with `--reload` flag
- Frontend auto-reloads with `bun dev`
- Check browser developer tools for frontend issues
- Check terminal output for backend issues

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## License

This project is licensed under the MIT License. 
# Local Postgres Setup Guide

> **Note**: This guide is for setting up the backend with a local Postgres.app instance instead of Docker or cloud databases. For general setup instructions, see the [main README](../README.md).

## Local Database Configuration

This setup uses your local Postgres.app instance with the following configuration:

- **Host**: localhost
- **Port**: 54323 (non-standard port to avoid conflicts)
- **Database**: expert
- **User**: jensbosseparra (your macOS username)
- **Connection String**: `postgresql://jensbosseparra@localhost:54323/expert`

## Setup Steps Completed ✅

1. **Database Creation**: Created the `expert` database on your local Postgres instance
2. **Environment Configuration**: Set up `.env` file with local database connection
3. **Dependency Management**: Added `python-dotenv` for environment variable loading
4. **Application Updates**: Modified `main.py` to load `.env` automatically
5. **SDK Fixes**: Corrected OpenAI Agents SDK usage
6. **Connection Testing**: Verified database connectivity with test script

## Local Environment File

Your `backend/.env` file contains:
```bash
# OpenAI API Key - get from https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Local Postgres database URL (using Postgres.app on custom port)
PG_URL=postgresql://jensbosseparra@localhost:54323/expert
```

## Quick Test Commands

```bash
# Test database connection only
uv run python test_db.py

# Start backend with local database
uv run uvicorn main:app --reload --port 8000
```

## Database Schema

The application automatically creates a `messages` table:
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    role VARCHAR(10) NOT NULL,     -- 'user' or 'assistant'
    content TEXT NOT NULL,         -- message content
    ts TIMESTAMP DEFAULT NOW()     -- timestamp
);
```

## Troubleshooting Local Setup

### Database Connection Issues
```bash
# Check if Postgres.app is running and database exists
psql -h localhost -p 54323 -d expert -c "SELECT 1;"

# If database doesn't exist, create it
psql -h localhost -p 54323 -d postgres -c "CREATE DATABASE expert;"
```

### Environment Variable Issues
```bash
# Verify .env file exists and is readable
cat backend/.env

# Test environment loading
cd backend && uv run python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('OPENAI_API_KEY:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET')
print('PG_URL:', os.getenv('PG_URL'))
"
```

### Port Conflicts
If port 54323 is busy, you can:
1. Change the port in Postgres.app settings
2. Update the `PG_URL` in your `.env` file accordingly
3. Restart both Postgres.app and your backend

## Alternative Database Options

If you prefer different setups, see the [main README](../README.md) for:
- Docker Postgres setup
- Cloud database providers (Railway, Supabase, Neon)
- Standard PostgreSQL installation

---

**Next Step**: Add your OpenAI API key to the `.env` file and start developing! 🚀 
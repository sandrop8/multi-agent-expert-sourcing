"""
Configuration and environment variable management
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ---- Environment Variables ------------------------------------------------
OPENAI_KEY = os.getenv("OPENAI_API_KEY")  # set in Railway › Variables
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("PG_URL")  # Railway uses DATABASE_URL

# Better error messages for missing environment variables
missing_vars = []
if not OPENAI_KEY:
    missing_vars.append("OPENAI_API_KEY")
if not DATABASE_URL:
    missing_vars.append("DATABASE_URL or PG_URL")

if missing_vars:
    print("❌ Missing required environment variables:")
    for var in missing_vars:
        print(f"   - {var}")
    print("\n💡 For local development:")
    print("   - Get OPENAI_API_KEY from: https://platform.openai.com/api-keys")
    print("   - For DATABASE_URL/PG_URL, you can use:")
    print("     • Local PostgreSQL: postgresql://user:password@localhost:5432/dbname")
    print("     • Docker: docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres")
    print("     • Railway/Supabase/Neon for cloud database")
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Fix Railway URL format: postgres:// -> postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

# ---- Application Configuration --------------------------------------------
CORS_ORIGINS = [
    "http://localhost:3000", 
    "http://localhost:3002",  # Add port 3002 for your current frontend
    "http://localhost:3004",  # Add port 3004 for your current frontend
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3002",  # Add 127.0.0.1 version too
    "http://127.0.0.1:3004",  # Add 127.0.0.1 version too
    "https://poetic-optimism-production.up.railway.app"  # Railway frontend URL
]

# File upload limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_TYPES = [
    "application/pdf", 
    "application/msword", 
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
] 
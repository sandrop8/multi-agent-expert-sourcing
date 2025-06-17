#!/usr/bin/env python3
"""
Simple script to test database connectivity to the local Postgres instance.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed, loading .env manually...")
    # Manual .env loading
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value

import sqlalchemy as sa


def test_database_connection():
    """Test the database connection and create the messages table if it doesn't exist."""

    # Use same logic as main.py: DATABASE_URL first, then PG_URL as fallback
    database_url = os.getenv("DATABASE_URL") or os.getenv("PG_URL")

    if not database_url:
        print("❌ DATABASE_URL or PG_URL environment variable not found!")
        print("   Make sure your .env file is properly configured.")
        return False

    # Fix Railway URL format: postgres:// -> postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://")

    print(f"🔗 Testing connection to: {database_url}")

    try:
        # Create engine
        engine = sa.create_engine(database_url, future=True)

        # Test connection
        with engine.connect() as conn:
            result = conn.execute(sa.text("SELECT version()"))
            version = result.fetchone()[0]
            print("✅ Connected successfully!")
            print(f"   PostgreSQL version: {version}")

        # Test table creation (same as in main.py)
        meta = sa.MetaData()
        messages = sa.Table(
            "messages",
            meta,
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("role", sa.String(10)),
            sa.Column("content", sa.Text),
            sa.Column("ts", sa.DateTime, default=sa.func.now()),
        )

        print("📝 Creating/checking messages table...")
        meta.create_all(engine)
        print("✅ Messages table is ready!")

        # Test a simple query
        with engine.connect() as conn:
            result = conn.execute(sa.text("SELECT COUNT(*) FROM messages"))
            count = result.fetchone()[0]
            print(f"📊 Current messages in database: {count}")

        return True

    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Make sure Postgres app is running")
        print("   2. Verify the database 'expert' exists on port 54323")
        print("   3. Check if your username 'jensbosseparra' has access")
        print("   4. Try connecting manually: psql -h localhost -p 54323 -d expert")
        return False


if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)

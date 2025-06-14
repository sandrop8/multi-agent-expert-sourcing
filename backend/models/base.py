"""
Database engine and metadata setup
Supporting both SQLAlchemy Core (legacy) and ORM (new structured CV data)
"""

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, mapped_column
from sqlalchemy import DateTime, Integer
from core.config import DATABASE_URL
from datetime import datetime

# ---- Database Setup -------------------------------------------------------
engine = sa.create_engine(DATABASE_URL, future=True)
meta = sa.MetaData()

# ---- ORM Setup (for new structured CV models) ----------------------------
Base = declarative_base()

class BaseModel(Base):
    """Abstract base model with common audit fields for ORM models"""
    __abstract__ = True

    id = mapped_column(Integer, primary_key=True, index=True)
    created_at = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

# ---- Legacy Core Functions (backwards compatibility) ---------------------
def create_all_tables():
    """Create all tables defined in metadata (Core tables)"""
    meta.create_all(engine)

def create_all_orm_tables():
    """Create all ORM model tables"""
    Base.metadata.create_all(engine)

def get_engine():
    """Get database engine"""
    return engine

def get_metadata():
    """Get database metadata (for Core tables)"""
    return meta 
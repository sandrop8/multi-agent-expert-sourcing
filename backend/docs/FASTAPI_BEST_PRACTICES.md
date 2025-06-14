# FastAPI Best Practices & Architecture Guide

This document provides comprehensive best practices for FastAPI development, focusing on SQLAlchemy ORM, Pydantic models, database patterns, and project structure that an LLM can follow for consistent development.

## 🏗️ **Project Architecture Overview**

### **Recommended File Structure**
```
multi-agent-expert-sourcing/
├── README.md              # Project overview and quick start
├── Makefile               # Root-level commands (dev-all, test-all, etc.)
├── .gitignore             # Git ignore patterns
├── test-all.sh           # Comprehensive test suite script
├── TESTING.md            # Testing documentation
├── QUICK_START_TESTING.md # Quick testing guide
├── railway.json          # Deployment configuration
├── backend/
│   ├── main.py           # FastAPI app initialization and routes
│   ├── Makefile          # Backend-specific commands
│   ├── pyproject.toml    # Python dependencies and project config
│   ├── uv.lock           # Dependency lock file
│   ├── Dockerfile        # Container configuration
│   ├── models/           # SQLAlchemy ORM models (database schema)
│   │   ├── __init__.py
│   │   ├── base.py       # Base model class and database session
│   │   ├── cv_models.py  # CV-related database models
│   │   ├── chat_models.py # Chat/conversation models
│   │   └── user_models.py # User-related models (future)
│   ├── schemas/          # Pydantic models (API request/response)
│   │   ├── __init__.py
│   │   ├── cv_schemas.py # CV-related API schemas
│   │   ├── chat_schemas.py # Chat API schemas
│   │   └── base_schemas.py # Common base schemas
│   ├── api/              # API route handlers
│   │   ├── __init__.py
│   │   └── v1/           # API versioning
│   │       ├── __init__.py
│   │       ├── cv.py     # CV-related endpointsSo as you have recreated the wrong backend structure before, you may need to now go back to the readme with fast API best practices with the project structure. And first, rearrange 
│   │       ├── chat.py   # Chat endpoints
│   │       └── health.py # Health check endpoints
│   ├── core/             # Core application configuration
│   │   ├── __init__.py
│   │   ├── config.py     # Settings and environment variables
│   │   └── database.py   # Database connection and session management
│   ├── services/         # Business logic layer
│   │   ├── __init__.py
│   │   ├── cv_service.py # CV processing business logic
│   │   └── chat_service.py # Chat service logic
│   ├── agents/           # OpenAI Agents SDK related code
│   │   ├── __init__.py
│   │   ├── cv_agents.py  # CV processing agents
│   │   └── chat_agents.py # Chat agents
│   ├── tests/            # Test suite
│   │   ├── __init__.py
│   │   ├── test_api.py   # API endpoint tests
│   │   ├── test_simple.py # Basic functionality tests
│   │   ├── test_cv_models.py # Model-specific tests
│   │   └── test_services.py # Service layer tests
│   ├── migrations/       # Alembic database migrations
│   │   ├── versions/
│   │   └── alembic.ini
│   ├── docs/             # Backend-specific documentation
│   │   ├── FASTAPI_BEST_PRACTICES.md
│   │   ├── CV_Semantic_Search.md
│   │   └── LOCAL_POSTGRES_SETUP.md
│   ├── data/             # Test data and fixtures
│   │   ├── fictional_cvs/ # Test CV files
│   │   └── ground_truth/ # Manual analysis data
│   │       └── lisa_shaw_ground_truth.py
│   ├── scripts/          # Utility scripts
│   │   ├── test_db.py    # Database connectivity test
│   │   └── migration_helpers.py # Migration utilities
│   └── .venv/            # Virtual environment
├── frontend/             # Next.js frontend application
│   ├── app/, components/, lib/ # (existing frontend structure)
│   ├── package.json
│   ├── Makefile
│   └── ...
├── docs/                 # Project-level documentation
│   ├── architecture.md   # System architecture overview
│   ├── development-guide.md # Development setup and guidelines
│   └── deployment.md     # Deployment instructions
├── scripts/              # Project-level scripts
│   ├── setup.sh          # Project setup automation
│   └── deploy.sh         # Deployment automation
├── .github/              # GitHub Actions CI/CD
│   └── workflows/
│       ├── test.yml      # Automated testing
│       └── deploy.yml    # Automated deployment
└── .vscode/              # IDE configuration
    └── settings.json
```

## 🗄️ **SQLAlchemy ORM Best Practices**

### **1. Base Model Pattern**
```python
# models/base.py
from datetime import datetime
import os

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager

# Database configuration -------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("PG_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")

engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False,
    pool_size=20,
    pool_pre_ping=True,
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()

class BaseModel(Base):
    """Abstract base model with common audit fields"""
    __abstract__ = True

    id: int = mapped_column(primary_key=True, index=True)
    created_at: datetime = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: datetime = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

# Dependency --------------------------------------------------------------
async def get_db() -> AsyncSession:
    """FastAPI dependency that provides a scoped AsyncSession."""
    async with AsyncSessionLocal() as session:
        yield session
```

#### **Why AsyncSession is “professional default” (2023‑2025)**

* **Non‑blocking I/O** – `asyncpg`, `psycopg 3` and SQLAlchemy 2.x deliver full coroutine support; each Uvicorn worker now multiplexes hundreds of DB queries concurrently rather than one at a time.  
* **Unified API** – the same `select()`/`update()` constructs work in both sync and async code; migrating old sync paths is mostly a find‑and‑replace of `.Session` → `.AsyncSession` plus `await`.  
* **FastAPI docs & templates** – all official examples since FastAPI 0.110 yield an `AsyncSession` via dependency injection, so new hires (often coming from Django) instantly recognise the pattern.  
* **Testing & scripts** – you can still spin up a *sync* `Session` in a CLI script by binding a synchronous engine to the same declarative models. No duplication, maximum flexibility.

### **2. Model Definition Patterns**

> **Declarative mapping is first‑class.**  
> SQLAlchemy 2.x removed the old `mapper()` imperative API; declarative classes like `CVFile` *are* the canonical approach. Core `Table` objects are still available (and power the ORM behind the scenes) but you rarely need them unless writing raw SQL for analytics or pgvector similarity search.
```python
# models/cv_models.py
from sqlalchemy import Column, String, Integer, Boolean, Text, Date, DECIMAL, ForeignKey, LargeBinary, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from .base import BaseModel

class CVFile(BaseModel):
    """CV file storage and metadata"""
    __tablename__ = "cv_files"
    
    # File metadata
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_format = Column(String(10), nullable=False)  # 'pdf', 'docx', 'jpeg', 'png'
    file_size = Column(Integer, nullable=False)
    content_type = Column(String(100), nullable=False)
    file_data = Column(LargeBinary, nullable=False)  # Binary file content
    
    # Processing metadata
    processing_status = Column(String(50), default='pending', nullable=False)
    extraction_provider = Column(String(50), nullable=True)  # 'mistral', 'openai', 'simple'
    extraction_confidence = Column(DECIMAL(3,2), nullable=True)
    processed = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    personal_info = relationship("CVPersonalInfo", back_populates="cv_file", cascade="all, delete-orphan", uselist=False)
    employment = relationship("CVEmployment", back_populates="cv_file", cascade="all, delete-orphan")
    education = relationship("CVEducation", back_populates="cv_file", cascade="all, delete-orphan")
    skills = relationship("CVSkill", back_populates="cv_file", cascade="all, delete-orphan")
    certifications = relationship("CVCertification", back_populates="cv_file", cascade="all, delete-orphan")
    projects = relationship("CVProject", back_populates="cv_file", cascade="all, delete-orphan")
    languages = relationship("CVLanguage", back_populates="cv_file", cascade="all, delete-orphan")

class CVPersonalInfo(BaseModel):
    """Personal information extracted from CV"""
    __tablename__ = "cv_personal_info"
    
    cv_file_id = Column(Integer, ForeignKey("cv_files.id", ondelete="CASCADE"), nullable=False)
    
    # Personal details (all nullable as not all CVs contain all information)
    full_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    location = Column(String(255), nullable=True)
    professional_title = Column(String(255), nullable=True)
    
    # Online presence (all optional)
    linkedin_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    portfolio_url = Column(String(500), nullable=True)
    
    # Professional summary
    summary = Column(Text, nullable=True)
    
    # Relationship
    cv_file = relationship("CVFile", back_populates="personal_info")

class CVEmployment(BaseModel):
    """Employment history from CV"""
    __tablename__ = "cv_employment"
    
    cv_file_id = Column(Integer, ForeignKey("cv_files.id", ondelete="CASCADE"), nullable=False)
    
    # Job details
    company_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    
    # Dates (nullable for incomplete information)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_current = Column(Boolean, default=False, nullable=False)
    duration_months = Column(Integer, nullable=True)  # Calculated field
    
    # Ordering (0 = most recent)
    employment_order = Column(Integer, default=0, nullable=False)
    
    # Relationship
    cv_file = relationship("CVFile", back_populates="employment")

# Additional models follow similar patterns...
```

### **3. Nullable Fields Strategy**
```python
# For CV data, most fields should be nullable because:
# - Not all CVs contain complete information
# - Different CV formats include different sections
# - OCR/extraction might miss certain fields

# Required fields (NOT NULL):
- Primary keys (id)
- Foreign keys (cv_file_id)
- File metadata (filename, file_size, content_type)
- Status fields (processing_status, processed)

# Optional fields (NULL allowed):
- All personal information (email, phone, linkedin_url, github_url)
- All extracted content (skills, experience details, education)
- All dates and descriptions
- All URLs and external references
```

## 📊 **Pydantic Schema Patterns**

### **1. Request/Response Schemas**
```python
# schemas/cv_schemas.py
from pydantic import BaseModel, EmailStr, HttpUrl, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal

class CVFileBase(BaseModel):
    """Base CV file schema"""
    filename: str
    file_format: str
    file_size: int
    content_type: str

class CVFileCreate(CVFileBase):
    """Schema for creating CV file records"""
    file_data: bytes
    processing_status: str = "pending"
    processed: bool = False

class CVFileResponse(CVFileBase):
    """Schema for CV file API responses"""
    id: int
    processing_status: str
    extraction_provider: Optional[str] = None
    extraction_confidence: Optional[Decimal] = None
    processed: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)  # SQLAlchemy compatibility

class CVPersonalInfoCreate(BaseModel):
    """Schema for creating personal info"""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    professional_title: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    portfolio_url: Optional[HttpUrl] = None
    summary: Optional[str] = None

class CVPersonalInfoResponse(CVPersonalInfoCreate):
    """Schema for personal info API responses"""
    id: int
    cv_file_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Employment schema with nullable fields
class CVEmploymentCreate(BaseModel):
    """Schema for creating employment records"""
    company_name: str
    job_title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: bool = False
    duration_months: Optional[int] = None
    employment_order: int = 0

class CVEmploymentResponse(CVEmploymentCreate):
    """Schema for employment API responses"""
    id: int
    cv_file_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
```

### **2. Validation Patterns**
```python
# Custom validators for CV data
from pydantic import validator, Field
from typing import Optional

class CVPersonalInfoCreate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    
    @validator('phone')
    def validate_phone(cls, v):
        if v is not None:
            # Remove common phone formatting
            cleaned = ''.join(filter(str.isdigit, v))
            if len(cleaned) < 10:
                raise ValueError('Phone number too short')
        return v
    
    @validator('full_name')
    def validate_name(cls, v):
        if v is not None:
            v = v.strip()
            if len(v) < 2:
                raise ValueError('Name too short')
        return v
```

## 🔌 **FastAPI Integration Patterns**

### **1. Route Definition with Dependencies**
```python
# api/v1/cv.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models.base import get_db
from models.cv_models import CVFile, CVPersonalInfo
from schemas.cv_schemas import CVFileResponse, CVPersonalInfoResponse
from services.cv_service import CVService

router = APIRouter(prefix="/cv", tags=["cv"])

@router.post("/upload", response_model=CVFileResponse)
async def upload_cv(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Upload and process CV file"""
    cv_service = CVService(db)
    return await cv_service.upload_cv(file)

@router.get("/{cv_id}", response_model=CVFileResponse)
async def get_cv(
    cv_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve a CV by primary key"""
    cv = await db.get(CVFile, cv_id)
    if cv is None:
        raise HTTPException(status_code=404, detail="CV not found")
    return cv
```

### **2. Service Layer Pattern**
```python
# services/cv_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, HTTPException
from models.cv_models import CVFile, CVPersonalInfo
from schemas.cv_schemas import CVFileCreate, CVPersonalInfoCreate

class CVService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upload_cv(self, file: UploadFile) -> CVFile:
        """Process CV upload with validation (async)"""
        allowed_types = {
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }
        if file.content_type not in allowed_types:
            raise HTTPException(400, "Only PDF and Word documents allowed")

        file_content = await file.read()
        if len(file_content) > 10 * 1024 * 1024:  # 10 MB
            raise HTTPException(400, "File size exceeds 10 MB limit")

        cv_data = CVFileCreate(
            filename=file.filename,
            original_filename=file.filename,
            file_format=file.filename.split(".")[-1].lower(),
            file_size=len(file_content),
            content_type=file.content_type,
            file_data=file_content,
        )

        cv_file = CVFile(**cv_data.model_dump())
        self.db.add(cv_file)
        await self.db.commit()
        await self.db.refresh(cv_file)
        return cv_file

    async def create_personal_info(
        self, cv_id: int, personal_data: CVPersonalInfoCreate
    ) -> CVPersonalInfo:
        """Create personal info record for CV (async)"""
        personal_info = CVPersonalInfo(
            cv_file_id=cv_id, **personal_data.model_dump(exclude_unset=True)
        )
        self.db.add(personal_info)
        await self.db.commit()
        await self.db.refresh(personal_info)
        return personal_info
```

## 🚀 **Migration Strategy from Current Setup**

### **1. Current State (SQLAlchemy Core)**
```python
# Current approach in main.py (to be migrated)
messages = sa.Table(
    "messages",
    meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("role", sa.String(10)),
    sa.Column("content", sa.Text),
    sa.Column("ts", sa.DateTime, default=dt.datetime.utcnow),
)
```

### **2. Migration to ORM**
```python
# New ORM approach
class Message(BaseModel):
    __tablename__ = "messages"
    
    role = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    # id, created_at, updated_at inherited from BaseModel
```

### **3. Migration Steps**
1. **Create model files** following the structure above
2. **Set up Alembic** for database migrations
3. **Create initial migration** from existing schema
4. **Update routes** to use ORM queries instead of Core
5. **Add service layer** for business logic
6. **Test thoroughly** before deployment

## 📋 **Development Workflow**

### **1. Adding New Features**
1. **Define SQLAlchemy model** in appropriate model file
2. **Create Pydantic schemas** for API requests/responses
3. **Generate migration** with Alembic
4. **Implement service layer** logic
5. **Create API routes** with proper dependencies
6. **Write tests** for all layers
7. **Update documentation**

### **2. Database Changes**
```bash
# Generate migration after model changes
alembic revision --autogenerate -m "Add CV personal info table"

# Review and edit migration file if needed
# Apply migration
alembic upgrade head
```

### **3. Testing Pattern**
```python
# tests/test_cv_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_upload_cv():
    with TestClient(app) as client:
        # Test CV upload
        response = client.post("/cv/upload", files={"file": ("test.pdf", b"test content", "application/pdf")})
        assert response.status_code == 200
```

## 🎯 **Key Benefits of This Architecture**

1. **Type Safety**: Full type checking with Pydantic and SQLAlchemy
2. **Separation of Concerns**: Clear layers (models, schemas, services, routes)
3. **Database Migrations**: Automatic migration generation with Alembic
4. **Testability**: Easy to mock and test individual components
5. **Maintainability**: Django-like structure familiar to developers
6. **Scalability**: Easy to add new features and endpoints
7. **Documentation**: Automatic API docs with proper schemas

## 🔧 **Configuration Management**

```python
# core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str
    
    # OpenAI
    openai_api_key: str
    
    # File upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list = ["application/pdf", "application/msword"]
    
    # CV Processing
    text_extraction_provider: str = "mistral"
    embedding_model: str = "text-embedding-3-large"
    similarity_threshold: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

This architecture provides a robust, maintainable, and scalable foundation for your FastAPI application with proper database modeling, API design, and OpenAI Agents SDK integration. 
# END OF FILE

---

### 🧩 **ORM vs Core Cheat‑Sheet (2025)**

| Use case | Preferred layer | Why |
| -------- | --------------- | --- |
| CRUD endpoints, Pydantic ↔ DB round‑tripping | **ORM** | Declarative models, type hints, Alembic autogen |
| Vector similarity search, analytics queries | **Core / Text** | Fine‑tuned SQL (`pgvector` ops, `COPY`) without object overhead |
| Mixed workload | **Hybrid** | Map tables for migrations, write hot‑path queries in Core |
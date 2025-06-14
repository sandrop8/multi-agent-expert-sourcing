# CV Semantic Search Implementation Project

## Table of Contents
- [ ] [🎯 Project Overview](#project-overview)
- [ ] [🏗️ Current Architecture Analysis](#current-architecture-analysis)
  - [ ] [Existing Components](#existing-components)
  - [ ] [Integration Points](#integration-points)
- [ ] [🚀 Implementation Phases](#implementation-phases)
  - [x] [Phase 0: Data Preparation & Schema Design](#phase-0-data-preparation--schema-design)
    - [x] [0.1 Download Example CVs](#01-download-example-cvs)
    - [x] [0.2 Define PostgreSQL Schema for Structured CV Data](#02-define-postgresql-schema-for-structured-cv-data)
    - [x] [0.3 Manual CV Analysis & Schema Mapping](#03-manual-cv-analysis--schema-mapping)
  - [ ] [Phase 1: Database & Infrastructure Setup](#phase-1-database--infrastructure-setup)
    - [ ] [1.1 PgVector Database Setup](#11-pgvector-database-setup)
    - [ ] [1.2 Dependencies & Environment](#12-dependencies--environment)
    - [ ] [1.3 Environment Variables](#13-environment-variables)
    - [ ] [1.4 Embedding Models Under Evaluation](#14-embedding-models-under-evaluation)
  - [ ] [Phase 2: CV Text Extraction Pipeline](#phase-2-cv-text-extraction-pipeline)
    - [ ] [2.1 Why Mistral OCR + OpenAI Strategy](#21-why-mistral-ocr--openai-strategy)
    - [ ] [2.2 Provider‑Agnostic Text Extraction Interface](#22-provider-agnostic-text-extraction-interface)
    - [ ] [2.2 Three‑Provider Implementation Strategy](#22-three-provider-implementation-strategy)
    - [ ] [2.3 Provider Selection Strategy](#23-provider-selection-strategy)
  - [ ] [Phase 3: Agent Integration & Embedding Creation](#phase-3-agent-integration--embedding-creation)
    - [ ] [3.1 New Specialized Agents](#31-new-specialized-agents)
    - [ ] [3.2 Enhanced Freelancer Profile Manager](#32-enhanced-freelancer-profile-manager)
  - [ ] [Phase 4: Semantic Search Implementation](#phase-4-semantic-search-implementation)
    - [ ] [4.1 Expert Search Agent System](#41-expert-search-agent-system)
    - [ ] [4.2 Semantic Search Service](#42-semantic-search-service)
  - [ ] [Phase 5: API Endpoints & Integration](#phase-5-api-endpoints--integration)
    - [ ] [5.1 New FastAPI Endpoints](#51-new-fastapi-endpoints)
    - [ ] [5.2 Updated CV Upload Flow](#52-updated-cv-upload-flow)
  - [ ] [Phase 6: Evaluation & Benchmarking](#phase-6-evaluation--benchmarking)
    - [ ] [6.1 CV Extraction Evaluation Framework](#61-cv-extraction-evaluation-framework)
    - [ ] [6.2 Benchmark Test Scenarios](#62-benchmark-test-scenarios)
    - [ ] [6.3 Evaluation API Endpoints](#63-evaluation-api-endpoints)
    - [ ] [6.4 Evaluation Metrics & Reporting](#64-evaluation-metrics--reporting)
  - [ ] [Phase 7: Testing & Validation](#phase-7-testing--validation)
    - [ ] [7.1 Unit Tests for Each Component](#71-unit-tests-for-each-component)
    - [ ] [7.2 Integration Tests with Agent System](#72-integration-tests-with-agent-system)
    - [ ] [7.3 End-to-End Demo Scenarios](#73-end-to-end-demo-scenarios)
- [ ] [🔄 Testing Strategy & Incremental Implementation](#testing-strategy--incremental-implementation)
  - [ ] [Development Approach](#development-approach)
    - [ ] [1. Start Simple, Scale Up](#1-start-simple-scale-up)
    - [ ] [2. Provider Flexibility Testing](#2-provider-flexibility-testing)
    - [ ] [3. Model Provider Flexibility](#3-model-provider-flexibility)
  - [ ] [Validation Checkpoints](#validation-checkpoints)
    - [ ] [Phase 0 Validation: Test Data Ready](#phase-0-validation-test-data-ready)
    - [ ] [Phase 1 Validation: Database Works](#phase-1-validation-database-works)
    - [ ] [Phase 2 Validation: Text Extraction Works](#phase-2-validation-text-extraction-works)
    - [ ] [Phase 3 Validation: Agents Integration Works](#phase-3-validation-agents-integration-works)
    - [ ] [Phase 4 Validation: Semantic Search Works](#phase-4-validation-semantic-search-works)
    - [ ] [Phase 5 Validation: Full Pipeline Works](#phase-5-validation-full-pipeline-works)
    - [ ] [Phase 6 Validation: Evaluation System Works](#phase-6-validation-evaluation-system-works)
- [ ] [🎯 Success Metrics](#success-metrics)
  - [ ] [Technical Metrics](#technical-metrics)
  - [ ] [Functional Metrics](#functional-metrics)
  - [ ] [Demo Readiness](#demo-readiness)
- [ ] [🔄 Next Steps](#next-steps)
  - [ ] [Immediate Actions](#immediate-actions)
  - [ ] [Implementation Order](#implementation-order)
  - [ ] [Risk Mitigation](#risk-mitigation)

> **Goal**: Implement semantic search capabilities for uploaded CVs using PgVector, breaking down into manageable chunks that integrate with our existing OpenAI Agent SDK multi-agent system.

## 🎯 **Project Overview**

Transform the existing CV upload system into a semantic search engine that can find the most relevant experts based on natural language queries like "find me a Python developer with machine learning experience" using vector embeddings and similarity search.

## 🏗️ **Current Architecture Analysis**

### **Existing Components** ✅
- **CV Upload System**: File validation, storage in PostgreSQL (`cvs` table)
- **OpenAI Agent SDK**: Multi-agent system with `Runner`, `handoffs`, guardrails
- **Database**: PostgreSQL with SQLAlchemy 2.x, existing tables (`messages`, `cvs`)
- **Agents**: Freelancer Profile Manager, CV Content Validator, specialized parsing agents

### **Integration Points** 🔄
- **Agent Workflow**: Extend existing CV processing pipeline with semantic capabilities
- **Database Schema**: Add PgVector extension and embedding storage tables
- **API Endpoints**: New semantic search endpoints that leverage existing agent patterns

---

## 🚀 **Implementation Phases**

### **Phase 0: Data Preparation & Schema Design**

> **Foundation Phase**: Establish test data, define structured data schema, and create the baseline for all subsequent development phases.

#### **0.1 Download Example CVs**

**Objective**: Collect 10 diverse, fictional example CVs in different formats to serve as consistent test data throughout development.

**CV Collection Requirements:**
```bash
# Create test data directory
mkdir -p test_data/sample_cvs/

# Download 10 diverse CVs in different formats:
# - 4 PDFs (most common format)
# - 3 DOCX files (Microsoft Word format)  
# - 2 JPEG images (scanned/photo CVs)
# - 1 PNG image (screenshot CV)
```

**Required CV Diversity:**
- **Technical Roles**: Python Developer, React Frontend Developer, Data Scientist, DevOps Engineer
- **Formats**: Clean layouts, complex designs, scanned documents, image-based CVs
- **File Types**: PDFs, DOCX files, JPEG images, PNG images
- **Industries**: Different industries to provide variety in extraction testing
- **Languages**: English only at this time

**CV Sources:**
- **Template-based**: Use CV templates from the internet featuring fictional characters
- **Format Variations**: Ensure different layouts (single-column, two-column, creative designs)

#### **0.2 Define PostgreSQL Schema for Structured CV Data**

**Objective**: Design comprehensive SQLAlchemy ORM models to store extracted CV data in structured format (separate from vector embeddings), following FastAPI best practices.

```python
# models/cv_models.py
from sqlalchemy import Column, String, Integer, Boolean, Text, Date, DECIMAL, ForeignKey, LargeBinary, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from .base import BaseModel

class CVFile(BaseModel):
    """Core CV metadata and file information"""
    __tablename__ = "cv_files"
    
    # File metadata
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_format = Column(String(10), nullable=False)  # 'pdf', 'docx', 'jpeg', 'png'
    file_size = Column(Integer, nullable=False)
    content_type = Column(String(100), nullable=False)
    file_data = Column(LargeBinary, nullable=False)  # Binary file content
    
    # Processing metadata
    processing_status = Column(String(50), default='pending', nullable=False)  # 'pending', 'processed', 'failed'
    extraction_provider = Column(String(50), nullable=True)  # 'mistral', 'openai', 'simple'
    extraction_confidence = Column(DECIMAL(3,2), nullable=True)  # 0.00 to 1.00
    processed = Column(Boolean, default=False, nullable=False)
    
    # Relationships (cascade delete for data integrity)
    personal_info = relationship("CVPersonalInfo", back_populates="cv_file", cascade="all, delete-orphan", uselist=False)
    professional_services = relationship("CVProfessionalServices", back_populates="cv_file", cascade="all, delete-orphan", uselist=False)
    employment = relationship("CVEmployment", back_populates="cv_file", cascade="all, delete-orphan")
    education = relationship("CVEducation", back_populates="cv_file", cascade="all, delete-orphan")
    skills = relationship("CVSkill", back_populates="cv_file", cascade="all, delete-orphan")
    certifications = relationship("CVCertification", back_populates="cv_file", cascade="all, delete-orphan")
    projects = relationship("CVProject", back_populates="cv_file", cascade="all, delete-orphan")
    # languages relationship removed - languages now integrated into CVPersonalInfo

class CVPersonalInfo(BaseModel):
    """Comprehensive personal information extracted from CVs - Base class for all personal data"""
    __tablename__ = "cv_personal_info"
    
    cv_file_id = Column(Integer, ForeignKey("cv_files.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # REQUIRED PERSONAL DETAILS (must be collected if not in CV)
    first_name = Column(String(255), nullable=True)  # REQUIRED: Ask user if not extracted from CV
    last_name = Column(String(255), nullable=True)   # REQUIRED: Ask user if not extracted from CV
    phone = Column(String(50), nullable=True)        # REQUIRED: Ask user if not extracted from CV
    
    # OPTIONAL PERSONAL DETAILS
    email = Column(String(255), nullable=True)
    professional_title = Column(String(255), nullable=True)
    summary = Column(Text, nullable=True)
    
    # ONLINE PRESENCE URLs
    website_url = Column(String(500), nullable=True)      # General website/portfolio
    linkedin_url = Column(String(500), nullable=True)     # LinkedIn profile
    xing_url = Column(String(500), nullable=True)         # Xing profile (German professional network)
    github_url = Column(String(500), nullable=True)       # GitHub profile (kept for developers)
    
    # ADDRESS FIELDS (German address format)
    street = Column(String(255), nullable=True)           # Street name
    street_number = Column(String(20), nullable=True)     # House/building number
    plz = Column(String(10), nullable=True)               # Postal code (PLZ in Germany)
    city = Column(String(255), nullable=True)             # City name
    country = Column(String(100), nullable=True)          # MUST be from predefined country list, case-sensitive
    
    # LANGUAGES (JSON field for multiple languages with proficiency levels)
    # Format: [{"language": "German", "level": "native"}, {"language": "English", "level": "fluent"}]
    # Supported levels: "native", "fluent", "good", "basic", "conversational"
    # Can convert CV levels like "C1" -> "fluent", "B2" -> "good", etc.
    languages = Column(JSON, nullable=True)
    
    # WORK PREFERENCES (Array for multiple selections)
    # Options: ["remote", "on_premise"] - can select one or both
    # Most CVs won't have this information, so nullable
    work_preferences = Column(ARRAY(String), nullable=True)
    
    # PROFESSIONAL CAPABILITIES & INDUSTRIES
    # Industries - Multi-selection from 4 predefined options
    # Options: ["IT", "Engineering", "Marketing & Design", "Management, Sales & HR"]
    # Can select multiple industries
    industries = Column(ARRAY(String), nullable=True)
    
    # SKILLS SUMMARY (separate from detailed CVSkill records)
    # Overall skills array - all skills the person has
    skills_array = Column(ARRAY(String), nullable=True)
    # Top 5 skills - MUST be subset of skills_array
    top_skills = Column(ARRAY(String), nullable=True)  # Max 5 items, must be from skills_array
    # Total years of professional experience
    total_years_experience = Column(Integer, nullable=True)
    
    # FREELANCER PLATFORM AVAILABILITY & PRICING
    # Hours per week available (dropdown selection)
    hours_per_week_available = Column(Integer, nullable=True)  # e.g., 10, 20, 30, 40 hours/week
    
    # Available start date (when freelancer can start working)
    available_start_date = Column(Date, nullable=True)
    
    # HOURLY RATE - Support both single rate and range
    # Option 1: Single hourly rate (e.g., €80/hour)
    hourly_rate_single = Column(DECIMAL(8,2), nullable=True)  # Single rate in currency
    
    # Option 2: Hourly rate range (e.g., €70-€100/hour)  
    hourly_rate_min = Column(DECIMAL(8,2), nullable=True)     # Minimum rate for range
    hourly_rate_max = Column(DECIMAL(8,2), nullable=True)     # Maximum rate for range
    
    # NOTE: Use either single rate OR range, not both
    # - Single rate: populate hourly_rate_single, leave min/max null
    # - Range rate: populate hourly_rate_min + hourly_rate_max, leave single null
    # Currency assumed to be EUR for German market
    
    # Relationship
    cv_file = relationship("CVFile", back_populates="personal_info")

class CVProfessionalServices(BaseModel):
    """Professional services offered by freelancer - Tree-based structure based on industry selection"""
    __tablename__ = "cv_professional_services"
    
    cv_file_id = Column(Integer, ForeignKey("cv_files.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # SERVICES BASED ON INDUSTRY SELECTION (Tree-based structure)
    # Each industry has specific suggested services, but more can be added from dropdown
    
    # Services for "Management, Sales & HR" industry
    # Suggested: agile coaching, business consulting, HR services, project management, sales services, strategy consulting
    management_sales_hr_services = Column(ARRAY(String), nullable=True)
    
    # Services for "Marketing & Design" industry  
    # Suggested: advertising, branding, copywriting, corporate identity, graphic design, marketing consulting,
    #           marketing strategy, product design, SEA, SEO, UI/UX design, user research, web design
    marketing_design_services = Column(ARRAY(String), nullable=True)
    
    # Services for "Engineering" industry
    # Suggested: autonomous driving, AUTOSAR, computer vision, electrical engineering, embedded systems,
    #           functional safety, industry 4.0, mechanical engineering, MES & ERP systems, PLC programming,
    #           robotics, supply chain management and logistics, system architecture
    engineering_services = Column(ARRAY(String), nullable=True)
    
    # Services for "IT" industry
    # Suggested: artificial intelligence, application development, cloud development, cyber security,
    #           data science, devops, edge computing, low code/no code, SAP, web development
    it_services = Column(ARRAY(String), nullable=True)
    
    # NOTE: Only populate arrays for industries selected in CVPersonalInfo.industries
    # e.g., if industries = ["IT", "Engineering"], only populate it_services and engineering_services
    
    # Relationship
    cv_file = relationship("CVFile", back_populates="professional_services")

class CVEmployment(BaseModel):
    """Employment history extracted from CVs"""
    __tablename__ = "cv_employment"
    
    cv_file_id = Column(Integer, ForeignKey("cv_files.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Job details
    company_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    
    # Dates (nullable for incomplete information)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)  # NULL for current position
    is_current = Column(Boolean, default=False, nullable=False)
    duration_months = Column(Integer, nullable=True)  # Calculated field
    
    # Ordering (0 = most recent)
    employment_order = Column(Integer, default=0, nullable=False)
    
    # Relationship
    cv_file = relationship("CVFile", back_populates="employment")

class CVEducation(BaseModel):
    """Education background extracted from CVs"""
    __tablename__ = "cv_education"
    
    cv_file_id = Column(Integer, ForeignKey("cv_files.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Education details
    institution = Column(String(255), nullable=False)
    degree = Column(String(255), nullable=False)
    field_of_study = Column(String(255), nullable=True)
    graduation_year = Column(Integer, nullable=True)
    grade_gpa = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    education_order = Column(Integer, default=0, nullable=False)
    
    # Relationship
    cv_file = relationship("CVFile", back_populates="education")

class CVSkill(BaseModel):
    """Skills and technologies extracted from CVs"""
    __tablename__ = "cv_skills"
    
    cv_file_id = Column(Integer, ForeignKey("cv_files.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Skill details
    skill_name = Column(String(255), nullable=False)
    skill_category = Column(String(100), nullable=True, index=True)  # 'programming', 'framework', 'tool', 'soft_skill', 'language'
    proficiency_level = Column(String(50), nullable=True)  # 'beginner', 'intermediate', 'advanced', 'expert'
    years_experience = Column(Integer, nullable=True)
    is_primary_skill = Column(Boolean, default=False, nullable=False)
    
    # Relationship
    cv_file = relationship("CVFile", back_populates="skills")

class CVCertification(BaseModel):
    """Certifications and awards extracted from CVs"""
    __tablename__ = "cv_certifications"
    
    cv_file_id = Column(Integer, ForeignKey("cv_files.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Certification details
    certification_name = Column(String(255), nullable=False)
    issuing_organization = Column(String(255), nullable=True)
    issue_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    credential_id = Column(String(255), nullable=True)
    verification_url = Column(String(500), nullable=True)
    
    # Relationship
    cv_file = relationship("CVFile", back_populates="certifications")

class CVProject(BaseModel):
    """Projects mentioned in CVs"""
    __tablename__ = "cv_projects"
    
    cv_file_id = Column(Integer, ForeignKey("cv_files.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Project details
    project_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    technologies_used = Column(ARRAY(String), nullable=True)  # PostgreSQL array of technologies
    project_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    
    # Relationship
    cv_file = relationship("CVFile", back_populates="projects")

# CVLanguage class removed - languages are now integrated into CVPersonalInfo as JSON field

# Database indexes will be automatically created for:
# - Primary keys (id fields)
# - Foreign keys (cv_file_id fields) 
# - Explicitly indexed fields (skill_category, etc.)
# - Additional indexes can be added with Index() objects if needed
```

**Key ORM Benefits:**
- **Type Safety**: Full type hints and IDE support
- **Relationships**: Automatic foreign key management and cascading deletes
- **Migrations**: Alembic auto-generation from model changes
- **Comprehensive Personal Info**: All personal data consolidated into single CVPersonalInfo class
- **German Address Format**: Structured address fields (street, street_number, PLZ, city, country)
- **Multi-language Support**: JSON field for multiple languages with proficiency levels
- **Professional Capabilities**: Industries, skills summary, and tree-based services structure
- **Freelancer Platform Ready**: Availability, pricing, and work preference fields
- **Flexible Rate Structure**: Support for both single rate and range pricing
- **Tree-based Services**: Industry-specific service suggestions with extensibility
- **Skills Management**: Dual approach with summary (top skills) and detailed skill records
- **Required Field Strategy**: Clear marking of required fields (first_name, last_name, phone) for user follow-up
- **FastAPI Integration**: Direct Pydantic schema mapping with `from_attributes=True`

**Data Format Examples:**
```python
# Languages JSON format
languages = [
    {"language": "German", "level": "native"},
    {"language": "English", "level": "fluent"},
    {"language": "Spanish", "level": "good"}
]

# Work preferences array
work_preferences = ["remote", "on_premise"]  # Both options
work_preferences = ["remote"]                # Remote only

# Industries multi-selection
industries = ["IT", "Marketing & Design"]  # Can select multiple

# Skills summary
skills_array = ["Python", "React", "SQL", "Docker", "AWS", "JavaScript"]
top_skills = ["Python", "React", "SQL", "Docker", "AWS"]  # Max 5, subset of skills_array

# Professional services (based on selected industries)
# For IT industry
it_services = ["artificial intelligence", "web development", "cloud development"]
# For Marketing & Design industry  
marketing_design_services = ["UI/UX design", "web design", "SEO"]

# Hourly rate options
# Single rate
hourly_rate_single = 80.00  # €80/hour
hourly_rate_min = None
hourly_rate_max = None

# Range rate
hourly_rate_single = None
hourly_rate_min = 70.00     # €70/hour minimum
hourly_rate_max = 100.00    # €100/hour maximum

# Availability
hours_per_week_available = 30        # 30 hours/week
available_start_date = "2024-02-01"  # Available from February 1st

# Country validation required for case-sensitive country field
```

#### **0.3 Manual CV Analysis & Schema Mapping**

**Objective**: Manually analyze each of the 10 test CVs to extract structured data and create ground truth for benchmarking.

**Manual Analysis Process:**
```python
# Create ground truth data structure matching updated schema
@dataclass
class GroundTruthCV:
    filename: str
    file_format: str
    personal_info: Dict[str, Any]           # Comprehensive personal info including new fields
    professional_services: Dict[str, Any]  # Industry-based services offered
    employment_history: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    skills_detailed: List[Dict[str, Any]]   # Individual skill records (CVSkill)
    certifications: List[Dict[str, Any]]
    projects: List[Dict[str, Any]]
    extraction_challenges: List[str]        # Note difficult-to-extract elements

# Example ground truth for one CV (updated schema)
ground_truth_example = GroundTruthCV(
    filename="python_ml_engineer.pdf",
    file_format="pdf",
    personal_info={
        # Required fields
        "first_name": "Sarah",
        "last_name": "Martinez", 
        "phone": "+1-555-0123",
        
        # Optional personal details
        "email": "sarah.martinez@email.com",
        "professional_title": "Senior ML Engineer",
        "summary": "Experienced ML engineer with 5+ years in recommendation systems...",
        
        # Online presence
        "website_url": "sarah-martinez-ml.com",
        "linkedin_url": "linkedin.com/in/sarah-martinez-ml",
        "github_url": "github.com/sarah-martinez",
        
        # Address (German format)
        "street": "Tech Street", 
        "street_number": "123",
        "plz": "94102",
        "city": "San Francisco",
        "country": "United States",
        
        # Languages
        "languages": [
            {"language": "English", "level": "native"},
            {"language": "Spanish", "level": "fluent"}
        ],
        
        # Work preferences
        "work_preferences": ["remote", "on_premise"],
        
        # Professional capabilities
        "industries": ["IT"],
        "skills_array": ["Python", "TensorFlow", "PyTorch", "scikit-learn", "SQL", "Docker", "AWS"],
        "top_skills": ["Python", "TensorFlow", "PyTorch", "scikit-learn", "SQL"],
        "total_years_experience": 5,
        
        # Freelancer platform fields
        "hours_per_week_available": 40,
        "available_start_date": "2024-02-01",
        "hourly_rate_single": 120.00,  # €120/hour
        "hourly_rate_min": None,
        "hourly_rate_max": None
    },
    professional_services={
        "it_services": ["artificial intelligence", "application development", "data science"],
        "engineering_services": None,
        "marketing_design_services": None,
        "management_sales_hr_services": None
    },
    employment_history=[
        {
            "company_name": "TechCorp Inc",
            "job_title": "Senior ML Engineer",
            "start_date": "2022-01-01",
            "end_date": None,  # Current position
            "is_current": True,
            "duration_months": 24,
            "description": "Led development of recommendation systems using TensorFlow and PyTorch...",
            "location": "San Francisco, CA",
            "employment_order": 0
        },
        {
            "company_name": "DataViz Solutions",
            "job_title": "Data Scientist",
            "start_date": "2019-06-01", 
            "end_date": "2021-12-31",
            "is_current": False,
            "duration_months": 31,
            "description": "Built predictive models for customer churn analysis...",
            "location": "Remote",
            "employment_order": 1
        }
    ],
    skills_detailed=[
        {"skill_name": "Python", "skill_category": "programming", "proficiency_level": "expert", "years_experience": 5, "is_primary_skill": True},
        {"skill_name": "TensorFlow", "skill_category": "framework", "proficiency_level": "advanced", "years_experience": 3, "is_primary_skill": True},
        {"skill_name": "scikit-learn", "skill_category": "framework", "proficiency_level": "advanced", "years_experience": 4, "is_primary_skill": True},
        {"skill_name": "SQL", "skill_category": "programming", "proficiency_level": "intermediate", "years_experience": 4, "is_primary_skill": False}
    ],
    extraction_challenges=[
        "Complex mathematical equations in projects section",
        "Skills scattered across multiple sections",
        "Duration calculations needed for overlapping positions",
        "Freelancer availability and rates not mentioned in CV",
        "Industry selection needs to be inferred from job titles"
    ]
)
```

**Ground Truth Documentation:**
```python
# Create comprehensive ground truth file
class GroundTruthManager:
    def __init__(self):
        self.ground_truth_data = {}
        
    def add_cv_analysis(self, cv_data: GroundTruthCV):
        """Add manually analyzed CV data"""
        self.ground_truth_data[cv_data.filename] = cv_data
        
    def export_to_json(self, filepath: str):
        """Export ground truth for benchmarking"""
        with open(filepath, 'w') as f:
            json.dump(self.ground_truth_data, f, indent=2, default=str)
            
    def get_benchmark_expectations(self, filename: str) -> Dict[str, Any]:
        """Get expected extraction results for a specific CV"""
        return self.ground_truth_data.get(filename, {})

# Usage: Create test_data/ground_truth.json with all 10 CVs analyzed
```

**Deliverables for Phase 0:**
1. **10 Test CVs** in `test_data/sample_cvs/` directory
2. **PostgreSQL Schema** for structured CV data (separate from vector DB)
3. **Ground Truth JSON** with manually extracted data from all 10 CVs
4. **Documentation** of extraction challenges for each CV format
5. **Validation Script** to verify schema matches ground truth data

---

### **Phase 1: Database & Infrastructure Setup**

#### **1.1 PgVector Database Setup**
```sql
-- Enable PgVector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create embeddings storage table
CREATE TABLE cv_embeddings (
    id SERIAL PRIMARY KEY,
    cv_id INTEGER REFERENCES cvs(id) ON DELETE CASCADE,
    content_type VARCHAR(50) NOT NULL, -- 'full_text', 'skills', 'experience'
    text_content TEXT NOT NULL,
    embedding vector(1536), -- OpenAI ada-002 dimension
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for similarity search
CREATE INDEX cv_embeddings_embedding_idx ON cv_embeddings 
USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

#### **1.2 Dependencies & Environment**
```toml
# Add to pyproject.toml dependencies
dependencies = [
  # ... existing dependencies ...
  "pgvector>=0.2.0",  # PgVector Python client
  "pypdf2>=3.0.0",    # PDF text extraction (fallback)
  "python-docx>=0.8.11",  # Word document extraction
  "tiktoken>=0.5.0",  # Token counting for embeddings
  "mistralai>=1.0.0", # Mistral OCR API client
]
```

#### **1.3 Environment Variables**
```bash
# Add to .env
MISTRAL_API_KEY=your_mistral_api_key_here  # Mistral OCR API key
TEXT_EXTRACTION_PROVIDER=mistral           # mistral, openai, or simple
EMBEDDING_MODEL=text-embedding-3-large     # OpenAI (v3) large embedding model
DEEPINFRA_EMBEDDING_MODEL=qwen3-embed           # DeepInfra Qwen3 embedding model
NOMIC_EMBEDDING_MODEL=nomic-embed-vision-v1.5    # Nomic image embedding model
EMBEDDING_DIMENSION=1536
SIMILARITY_THRESHOLD=0.7
```

#### **1.4 Embedding Models Under Evaluation**

We will benchmark three different embedding approaches:

1. **OpenAI `text-embedding-3-large`** (text only) – no longer sota, and costly but easy integration.  
2. **DeepInfra `qwen3-embed`** (text only) – Qwen‑3 embedding model hosted on DeepInfra, noted for multilingual retrieval accuracy and low cost.  
3. **Nomic `nomic-embed-vision-v1.5`** (images) – multimodal vision model accessed via the Nomic Python SDK.


> **OCR vs. Multimodal Note**  
> • The OpenAI `text-embedding-3-large` and DeepInfra `qwen3-embed` models are *text‑only*. When processing PDFs or image‑heavy CVs you must first run an OCR or image‑captioning step (our pipeline uses Mistral OCR via `MISTRAL_API_KEY`).  
> • The Nomic multimodal lineup (`nomic-embed-vision-v1.5` and `colnomic-embed-multimodal`) can ingest both text and images directly, so you may skip OCR entirely. Set `TEXT_EXTRACTION_PROVIDER=none` to bypass the OCR stage when these models are selected.


<https://docs.nomic.ai/reference/python-api/generate-embeddings>

Example call for the Nomic image embedding:

```python
from nomic import embed

output = embed.image(
    images=['/path/to/image1.jpg', '/path/to/image2.jpg'],
    model='nomic-embed-vision-v1.5',
)
print(output)
# {
#     'embeddings': [
#         [0.008766174, 0.014785767, -0.13134766, ...],
#         [0.017822266, 0.018585205, -0.12683105, ...]
#     ],
#     'model': 'nomic-embed-vision-v1.5',
#     'usage': {'prompt_tokens': 10, 'total_tokens': 10}
# }
```

`embed.image(images: Sequence[Union[str, PIL.Image.Image]], model: str = "nomic-embed-vision-v1.5")` generates embeddings for each supplied image.

---

### **Phase 2: CV Text Extraction Pipeline**

#### **2.1 Why Mistral OCR + OpenAI Strategy**

Based on [Mistral's OCR announcement](https://mistral.ai/news/mistral-ocr), their model offers significant advantages for CV processing:

**Mistral OCR Advantages:**
- ✅ **94.89% Overall Accuracy** - outperforms GPT-4o (89.77%) and other OCR solutions  
- ✅ **Superior Multilingual Support** - 99.02% fuzzy match across diverse languages
- ✅ **Complex Document Understanding** - handles tables, equations, images natively
- ✅ **Cost Effective** - 1000 pages per $1 (vs higher OpenAI costs)
- ✅ **Speed** - processes up to 2000 pages/minute
- ✅ **Multimodal Output** - extracts both text and embedded images

**OpenAI GPT-4o as Fallback:**
- ✅ **Proven Reliability** - mature API with good error handling
- ✅ **Familiar Integration** - already using OpenAI for other agents
- ✅ **Structured Output** - excellent at formatting extracted data

#### **2.2 Provider-Agnostic Text Extraction Interface**
```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ExtractedContent:
    full_text: str
    skills: List[str]
    experience: List[str]
    education: List[str]
    contact_info: Dict[str, str]
    confidence_score: float

class TextExtractionProvider(ABC):
    @abstractmethod
    async def extract_from_pdf(self, content: bytes) -> ExtractedContent:
        pass
    
    @abstractmethod
    async def extract_from_docx(self, content: bytes) -> ExtractedContent:
        pass
```

#### **2.2 Three-Provider Implementation Strategy**

**Option A: Mistral OCR (State-of-the-Art)**
```python
class MistralOCRExtractor(TextExtractionProvider):
    """Uses Mistral OCR API for state-of-the-art document understanding"""
    
    async def extract_from_pdf(self, content: bytes) -> ExtractedContent:
        # 1. Send PDF directly to Mistral OCR API
        # 2. Get structured text + embedded images extraction
        # 3. Parse multimodal output (text, tables, equations)
        # 4. Return ExtractedContent with high confidence
        # Benefits: 94.89% accuracy, 2000 pages/min, multilingual
```

**Option B: OpenAI GPT-4o (LLM-Enhanced)**
```python
class OpenAITextExtractor(TextExtractionProvider):
    """Uses OpenAI GPT-4o for intelligent text extraction"""
    
    async def extract_from_pdf(self, content: bytes) -> ExtractedContent:
        # 1. Use PyPDF2 for basic text extraction
        # 2. Pass extracted text to GPT-4o for structured extraction
        # 3. Return ExtractedContent with good confidence
        # Benefits: Familiar API, good performance, proven reliability
```

**Option C: PyPDF2 Simple (Baseline)**
```python
class SimplePyPDF2Extractor(TextExtractionProvider):
    """Uses PyPDF2 + regex for basic text extraction without LLM costs"""
    
    async def extract_from_pdf(self, content: bytes) -> ExtractedContent:
        # 1. PyPDF2 for direct text extraction
        # 2. Regex patterns for skills detection (Python, React, etc.)
        # 3. Simple heuristics for experience parsing (years mentioned)
        # 4. Return ExtractedContent with lower confidence
        # Benefits: No API costs, fast, works offline, good baseline
```

#### **2.3 Provider Selection Strategy**
```python
class TextExtractionService:
    def __init__(self):
        self.providers = {
            'mistral': MistralOCRExtractor(),
            'openai': OpenAITextExtractor(),
            'simple': SimplePyPDF2Extractor()
        }
        self.default_provider = os.getenv('TEXT_EXTRACTION_PROVIDER', 'mistral')
    
    async def extract_cv_content(self, file_content: bytes, content_type: str) -> ExtractedContent:
        """Extract CV content with automatic fallback chain"""
        primary_provider = self.providers[self.default_provider]
        
        try:
            # Try primary provider first
            return await primary_provider.extract_from_pdf(file_content)
        except Exception as e:
            print(f"⚠️ Primary provider {self.default_provider} failed: {e}")
            
            # Try fallback providers
            fallback_order = ['mistral', 'openai', 'simple']
            for provider_name in fallback_order:
                if provider_name != self.default_provider:
                    try:
                        print(f"🔄 Trying fallback provider: {provider_name}")
                        return await self.providers[provider_name].extract_from_pdf(file_content)
                    except Exception as fallback_error:
                        print(f"⚠️ Fallback {provider_name} also failed: {fallback_error}")
                        continue
            
            raise Exception("All text extraction providers failed")
```

---

### **Phase 3: Agent Integration & Embedding Creation**

#### **3.1 New Specialized Agents**

**CV Text Extraction Agent**
```python
class CVExtractionOutput(BaseModel):
    extracted_text: str
    skills: List[str]
    experience_years: Optional[int]
    key_technologies: List[str]
    extraction_confidence: float

cv_extraction_agent = Agent(
    name="CV Text Extraction Agent",
    handoff_description="Specialist for extracting structured information from CV content",
    instructions="""Extract key information from CV text including:
    - Technical skills and proficiency levels
    - Years of experience in different technologies
    - Education background and certifications
    - Previous job titles and responsibilities
    Return structured data optimized for semantic search.""",
    output_type=CVExtractionOutput,
)
```

**CV Embedding Generation Agent**
```python
class CVEmbeddingOutput(BaseModel):
    embeddings_created: int
    embedding_ids: List[int]
    processing_status: str

cv_embedding_agent = Agent(
    name="CV Embedding Generation Agent", 
    handoff_description="Specialist for creating semantic embeddings from CV content",
    instructions="""Create semantic embeddings from extracted CV content:
    - Generate embeddings for full text, skills, and experience sections
    - Ensure embeddings capture semantic meaning for job matching
    - Store embeddings with appropriate metadata for retrieval""",
    output_type=CVEmbeddingOutput,
)
```

#### **3.2 Enhanced Freelancer Profile Manager**
```python
# Update existing freelancer_profile_manager with new handoffs
freelancer_profile_manager = Agent(
    name="Freelancer Profile Manager",
    instructions="""Coordinate CV processing workflow including:
    1. Content validation and extraction
    2. Structured data parsing 
    3. Semantic embedding generation
    4. Profile completeness analysis
    Ensure high-quality, searchable freelancer profiles.""",
    handoffs=[
        cv_parser_agent,           # Existing
        profile_enrichment_agent,  # Existing
        skills_extraction_agent,   # Existing
        gap_analysis_agent,        # Existing
        cv_extraction_agent,       # New
        cv_embedding_agent,        # New
    ],
    input_guardrails=[
        InputGuardrail(guardrail_function=cv_validation_guardrail),
    ],
)
```

---

### **Phase 4: Semantic Search Implementation**

#### **4.1 Expert Search Agent System**

**Expert Search Supervisor**
```python
class ExpertSearchOutput(BaseModel):
    experts_found: List[Dict[str, Any]]
    search_query: str
    similarity_scores: List[float]
    total_results: int

expert_search_supervisor = Agent(
    name="Expert Search Supervisor",
    instructions="""Coordinate semantic expert search by:
    1. Understanding natural language search queries
    2. Converting queries to optimized search vectors
    3. Finding most relevant experts using semantic similarity
    4. Ranking results by relevance and availability""",
    output_type=ExpertSearchOutput,
)
```

**Query Enhancement Agent**
```python
query_enhancement_agent = Agent(
    name="Query Enhancement Agent",
    handoff_description="Specialist for optimizing search queries for semantic search",
    instructions="""Enhance user search queries for better semantic matching:
    - Expand technical terms with related concepts
    - Add context for ambiguous terms
    - Suggest alternative phrasings for better results
    - Optimize query structure for embedding similarity""",
)
```

#### **4.2 Semantic Search Service**
```python
class SemanticSearchService:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
        
    async def search_experts(
        self, 
        query: str, 
        limit: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        1. Generate embedding for search query
        2. Perform vector similarity search in PgVector
        3. Rank results by similarity score
        4. Return expert profiles with relevance scores
        """
        
        # Generate query embedding
        query_embedding = await self.embedding_service.create_embedding(query)
        
        # Vector similarity search
        with engine.connect() as conn:
            result = conn.execute(
                sa.text("""
                SELECT 
                    c.id, c.filename, c.uploaded_at,
                    ce.text_content, ce.content_type,
                    1 - (ce.embedding <=> :query_vector) as similarity
                FROM cvs c
                JOIN cv_embeddings ce ON c.id = ce.cv_id  
                WHERE 1 - (ce.embedding <=> :query_vector) > :threshold
                ORDER BY ce.embedding <=> :query_vector
                LIMIT :limit
                """),
                {
                    "query_vector": str(query_embedding),
                    "threshold": similarity_threshold,
                    "limit": limit
                }
            )
            
            return [dict(row) for row in result]
```

---

### **Phase 5: API Endpoints & Integration**

#### **5.1 New FastAPI Endpoints**
```python
@app.post("/process-cv/{cv_id}")
async def process_cv_for_search(cv_id: int):
    """Extract text and create embeddings for existing CV"""
    # Use freelancer_profile_manager with new extraction/embedding agents
    
@app.get("/search-experts")
async def search_experts(
    query: str, 
    limit: int = 10,
    threshold: float = 0.7
):
    """Semantic search for experts using natural language queries"""
    # Use expert_search_supervisor agent system
    
@app.get("/cv/{cv_id}/embeddings")
async def get_cv_embeddings(cv_id: int):
    """Debug endpoint to view CV embeddings and extracted content"""
    
@app.post("/reprocess-all-cvs")
async def reprocess_all_cvs():
    """Batch process all existing CVs for embeddings (admin only)"""
```

#### **5.2 Updated CV Upload Flow**
```python
@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    """Enhanced CV upload with automatic embedding generation"""
    try:
        # ... existing file validation and storage ...
        
        # Process with enhanced freelancer agent system
        cv_description = f"""
        CV file uploaded: {file.filename} ({file.content_type}, {len(file_content)} bytes).
        
        Please:
        1. Validate this CV content
        2. Extract structured information  
        3. Generate semantic embeddings
        4. Create searchable profile
        """
        
        result = await Runner.run(freelancer_profile_manager, cv_description)
        
        return {
            "message": "CV uploaded and processed for semantic search!",
            "filename": file.filename,
            "processing_status": "embedded",
            "searchable": True,
            "agent_feedback": result.final_output
        }
```

---

### **Phase 6: Evaluation & Benchmarking**

#### **6.1 CV Extraction Evaluation Framework**

> **Note**: This evaluation framework uses the 10 test CVs and ground truth data established in **Phase 0**. The benchmark scenarios must be updated to match the actual CVs collected and analyzed in Phase 0.
```python
@dataclass
class ExtractionMetrics:
    provider_name: str
    cv_filename: str
    extraction_time: float
    skills_extracted: List[str]
    experience_years: Optional[int]
    confidence_score: float
    cost_per_extraction: float
    error_occurred: bool
    error_message: Optional[str]

class CVExtractionEvaluator:
    def __init__(self):
        self.test_cvs = [
            "sample_cvs/python_ml_engineer.pdf",      # Technical CV with ML skills
            "sample_cvs/frontend_react_dev.pdf",      # Frontend focused CV
            "sample_cvs/fullstack_developer.pdf"      # Full-stack experience CV
        ]
        self.providers = ['mistral', 'openai', 'simple']
        self.results = []
    
    async def run_evaluation(self) -> Dict[str, Any]:
        """Run all providers against all test CVs and collect metrics"""
        for cv_file in self.test_cvs:
            cv_content = self._load_cv_file(cv_file)
            
            for provider in self.providers:
                metrics = await self._evaluate_provider(provider, cv_file, cv_content)
                self.results.append(metrics)
        
        return self._generate_comparison_report()
    
    async def _evaluate_provider(self, provider: str, cv_file: str, content: bytes) -> ExtractionMetrics:
        """Evaluate a single provider on a single CV"""
        start_time = time.time()
        
        try:
            # Set provider environment
            os.environ['TEXT_EXTRACTION_PROVIDER'] = provider
            service = TextExtractionService()
            
            # Extract content
            result = await service.extract_cv_content(content, "application/pdf")
            extraction_time = time.time() - start_time
            
            # Calculate costs (estimated)
            cost = self._calculate_cost(provider, content)
            
            return ExtractionMetrics(
                provider_name=provider,
                cv_filename=cv_file,
                extraction_time=extraction_time,
                skills_extracted=result.skills,
                experience_years=result.experience_years,
                confidence_score=result.confidence_score,
                cost_per_extraction=cost,
                error_occurred=False,
                error_message=None
            )
            
        except Exception as e:
            return ExtractionMetrics(
                provider_name=provider,
                cv_filename=cv_file,
                extraction_time=time.time() - start_time,
                skills_extracted=[],
                experience_years=None,
                confidence_score=0.0,
                cost_per_extraction=0.0,
                error_occurred=True,
                error_message=str(e)
            )
```

#### **6.2 Benchmark Test Scenarios**

> **Important**: These test scenarios are **placeholders** and must be replaced with the actual ground truth data from **Phase 0**. Once the 10 test CVs are collected and manually analyzed, update this section to reflect the real CV content.

**Benchmark Using Phase 0 Test Data**
```python
# This will be populated from test_data/ground_truth.json after Phase 0
# Example structure based on actual CVs:
def load_benchmark_data():
    """Load ground truth data from Phase 0"""
    with open('test_data/ground_truth.json', 'r') as f:
        ground_truth = json.load(f)
    
    test_profiles = {}
    for filename, cv_data in ground_truth.items():
        test_profiles[filename] = {
            "expected_skills": [skill["skill_name"] for skill in cv_data["skills"] if skill["is_primary_skill"]],
            "expected_experience": calculate_total_experience(cv_data["employment_history"]),
            "complexity": determine_complexity(cv_data["extraction_challenges"]),
            "expected_personal_info": cv_data["personal_info"],
            "expected_employment_count": len(cv_data["employment_history"]),
            "expected_education_count": len(cv_data["education"]),
            "file_format": cv_data["file_format"]
        }
    return test_profiles

# Placeholder structure (to be replaced after Phase 0):
placeholder_test_profiles = {
    "python_ml_engineer.pdf": {
        "expected_skills": ["Python", "Machine Learning", "TensorFlow", "scikit-learn"],
        "expected_experience": 5,
        "complexity": "high"  # Math equations, technical diagrams
    },
    "frontend_react_dev.pdf": {
        "expected_skills": ["React", "JavaScript", "CSS", "HTML"],
        "expected_experience": 3,
        "complexity": "medium"  # Clean layout, some graphics
    },
    "fullstack_developer.pdf": {
        "expected_skills": ["Node.js", "React", "PostgreSQL", "Docker"],
        "expected_experience": 4,
        "complexity": "medium"  # Mixed technical content
    }
}
```

**Extended Benchmark (10 CVs)**
```python
# Additional test cases for scaling evaluation
extended_test_profiles = {
    **test_profiles,  # Include initial 3
    "data_scientist.pdf": {
        "expected_skills": ["Python", "R", "Statistics", "SQL"],
        "expected_experience": 6,
        "complexity": "high"
    },
    "mobile_developer.pdf": {
        "expected_skills": ["Swift", "Kotlin", "React Native", "iOS"],
        "expected_experience": 4,
        "complexity": "medium"
    },
    "devops_engineer.pdf": {
        "expected_skills": ["AWS", "Kubernetes", "Docker", "Terraform"],
        "expected_experience": 7,
        "complexity": "high"
    },
    # ... add 4 more diverse CVs
}
```

#### **6.3 Evaluation API Endpoints**
```python
@app.post("/evaluate-providers")
async def evaluate_all_providers():
    """Run evaluation across all providers and return comparison report"""
    evaluator = CVExtractionEvaluator()
    results = await evaluator.run_evaluation()
    return results

@app.get("/evaluation-results")
async def get_evaluation_results():
    """Get latest evaluation results and comparison metrics"""
    # Return cached evaluation results
    
@app.post("/evaluate-single-cv")
async def evaluate_single_cv(file: UploadFile = File(...)):
    """Test all three providers on a single uploaded CV"""
    cv_content = await file.read()
    results = {}
    
    for provider in ['mistral', 'openai', 'simple']:
        os.environ['TEXT_EXTRACTION_PROVIDER'] = provider
        service = TextExtractionService()
        
        try:
            start_time = time.time()
            extraction = await service.extract_cv_content(cv_content, file.content_type)
            processing_time = time.time() - start_time
            
            results[provider] = {
                "success": True,
                "processing_time": processing_time,
                "skills_count": len(extraction.skills),
                "skills": extraction.skills,
                "confidence": extraction.confidence_score,
                "experience_years": extraction.experience_years
            }
        except Exception as e:
            results[provider] = {
                "success": False,
                "error": str(e),
                "processing_time": None
            }
    
    return {
        "filename": file.filename,
        "provider_results": results,
        "timestamp": datetime.utcnow()
    }
```

#### **6.4 Evaluation Metrics & Reporting**
```python
class EvaluationReporter:
    def generate_comparison_report(self, results: List[ExtractionMetrics]) -> Dict[str, Any]:
        """Generate comprehensive comparison report"""
        
        provider_stats = {}
        
        for provider in ['mistral', 'openai', 'simple']:
            provider_results = [r for r in results if r.provider_name == provider]
            
            provider_stats[provider] = {
                "success_rate": len([r for r in provider_results if not r.error_occurred]) / len(provider_results),
                "avg_processing_time": np.mean([r.extraction_time for r in provider_results if not r.error_occurred]),
                "avg_confidence_score": np.mean([r.confidence_score for r in provider_results if not r.error_occurred]),
                "avg_skills_extracted": np.mean([len(r.skills_extracted) for r in provider_results if not r.error_occurred]),
                "total_cost": sum([r.cost_per_extraction for r in provider_results]),
                "error_count": len([r for r in provider_results if r.error_occurred])
            }
        
        # Determine recommended provider based on metrics
        recommendation = self._calculate_recommendation(provider_stats)
        
        return {
            "evaluation_summary": provider_stats,
            "recommendation": recommendation,
            "test_details": results,
            "evaluation_date": datetime.utcnow()
        }
    
    def _calculate_recommendation(self, stats: Dict) -> Dict[str, str]:
        """Calculate which provider to recommend based on performance"""
        
        # Score providers based on multiple factors
        scores = {}
        for provider, stat in stats.items():
            # Weighted scoring: accuracy(40%) + speed(20%) + cost(20%) + reliability(20%)
            score = (
                stat['avg_confidence_score'] * 0.4 +
                (1 / max(stat['avg_processing_time'], 0.1)) * 0.2 +  # Inverse time (faster = better)
                (1 / max(stat['total_cost'], 0.001)) * 0.2 +  # Inverse cost (cheaper = better)
                stat['success_rate'] * 0.2
            )
            scores[provider] = score
        
        best_provider = max(scores.keys(), key=lambda k: scores[k])
        
        return {
            "recommended_provider": best_provider,
            "reasoning": f"Best overall score: {scores[best_provider]:.2f}",
            "all_scores": scores
        }
```

---

### **Phase 7: Testing & Validation**

#### **7.1 Unit Tests for Each Component**
```python
# Test text extraction providers
async def test_mistral_ocr_extraction():
    extractor = MistralOCRExtractor()
    result = await extractor.extract_from_pdf(sample_cv_content)
    assert result.confidence_score > 0.9  # Mistral OCR has 94.89% accuracy
    assert len(result.skills) > 0

async def test_openai_text_extraction():
    extractor = OpenAITextExtractor()
    result = await extractor.extract_from_pdf(sample_cv_content)
    assert result.confidence_score > 0.8
    assert len(result.skills) > 0

async def test_simple_pypdf2_extraction():
    extractor = SimplePyPDF2Extractor()
    result = await extractor.extract_from_pdf(sample_cv_content)
    assert result.confidence_score > 0.5  # Lower baseline expectation
    assert len(result.skills) >= 0  # May not detect skills as well

# Test embedding generation
async def test_cv_embedding_creation():
    service = EmbeddingService()
    embedding = await service.create_embedding("Python developer with ML experience")
    assert len(embedding) == 1536  # OpenAI ada-002 dimension

# Test semantic search
async def test_semantic_expert_search():
    search_service = SemanticSearchService()
    results = await search_service.search_experts("React developer")
    assert len(results) >= 0
    assert all(result['similarity'] > 0.7 for result in results)
```

#### **7.2 Integration Tests with Agent System**
```python
async def test_full_cv_processing_pipeline():
    """Test complete flow from CV upload to searchable embedding"""
    
    # 1. Upload CV
    # 2. Verify agent processing
    # 3. Check embedding creation
    # 4. Test semantic search
    # 5. Validate results quality

async def test_agent_handoff_workflow():
    """Test OpenAI Agent SDK handoffs work correctly"""
    
    # Test freelancer_profile_manager coordinates all specialists
    # Verify cv_extraction_agent → cv_embedding_agent handoff
    # Check error handling and guardrail behavior
```

#### **7.3 End-to-End Demo Scenarios**
```python
# Scenario 1: Upload multiple diverse CVs
sample_cvs = [
    "python_ml_engineer.pdf",
    "react_frontend_dev.pdf", 
    "fullstack_node_developer.pdf",
    "data_scientist.pdf"
]

# Scenario 2: Test various search queries
search_queries = [
    "Python developer with machine learning",
    "Frontend React expert",
    "Full-stack JavaScript engineer", 
    "Data scientist with visualization skills"
]

# Scenario 3: Validate result relevance
# Upload CVs → Generate embeddings → Search → Verify correct matches
```

---

## 🔄 **Testing Strategy & Incremental Implementation**

### **Development Approach**

#### **1. Start Simple, Scale Up**
- **Phase 0**: Data preparation + Schema design (Foundation)
- **Phase 1-2**: Database + Three text extraction providers
- **Phase 3-4**: Agent integration + Basic search  
- **Phase 5-6**: API integration + Provider evaluation
- **Phase 7**: Comprehensive testing + Final optimization

#### **2. Provider Flexibility Testing**
```bash
# Test different extraction providers
export TEXT_EXTRACTION_PROVIDER=mistral   # Mistral OCR (state-of-the-art)
export TEXT_EXTRACTION_PROVIDER=openai    # OpenAI GPT-4o (LLM-enhanced)  
export TEXT_EXTRACTION_PROVIDER=simple    # PyPDF2 (baseline, no API costs)
```

#### **3. Model Provider Flexibility**  
```bash
# Test different embedding models
export EMBEDDING_MODEL=text-embedding-ada-002     # OpenAI (default)
export EMBEDDING_MODEL=text-embedding-3-small     # OpenAI newer/cheaper
export EMBEDDING_MODEL=sentence-transformers      # Local/open-source option
```

### **Validation Checkpoints**

#### **Phase 0 Validation**: Test Data Ready
```bash
# Verify 10 test CVs collected
ls test_data/sample_cvs/ | wc -l
# Expected: 10 files

# Verify file format diversity
ls test_data/sample_cvs/*.pdf | wc -l    # Expected: 4 PDFs
ls test_data/sample_cvs/*.docx | wc -l   # Expected: 3 DOCX
ls test_data/sample_cvs/*.{jpg,jpeg} | wc -l  # Expected: 2 JPEG
ls test_data/sample_cvs/*.png | wc -l    # Expected: 1 PNG

# Verify PostgreSQL schema created
psql -d your_db -c "\dt cv_*"
# Expected: All CV tables (cv_files, cv_personal_info, cv_employment, etc.)

# Verify ground truth data exists
python -c "
import json
with open('test_data/ground_truth.json', 'r') as f:
    gt = json.load(f)
print(f'✅ Ground truth data for {len(gt)} CVs')
assert len(gt) == 10, 'Should have 10 CVs analyzed'
"
```

#### **Phase 1 Validation**: Database Works
```bash
# Test PgVector setup
uv run python -c "
import psycopg2
from pgvector.psycopg2 import register_vector
conn = psycopg2.connect('your_db_url')
register_vector(conn)
print('✅ PgVector extension working!')
"
```

#### **Phase 2 Validation**: Text Extraction Works
```bash
# Test Mistral OCR extraction
export TEXT_EXTRACTION_PROVIDER=mistral
uv run python test_extraction.py sample_cv.pdf
# Expected: High accuracy extraction (94.89%), multilingual support

# Test OpenAI LLM-enhanced extraction  
export TEXT_EXTRACTION_PROVIDER=openai  
uv run python test_extraction.py sample_cv.pdf
# Expected: Good quality extraction, structured output

# Test PyPDF2 simple baseline
export TEXT_EXTRACTION_PROVIDER=simple
uv run python test_extraction.py sample_cv.pdf
# Expected: Basic text extraction, lower accuracy but fast and free
```

#### **Phase 3 Validation**: Agents Integration Works
```bash
# Test agent workflow
uv run python -c "
from main import freelancer_profile_manager, Runner
result = await Runner.run(freelancer_profile_manager, 'Process sample CV')
print('✅ Agent workflow operational!')
"
```

#### **Phase 4 Validation**: Semantic Search Works
```bash
# Test semantic search
curl "http://localhost:8000/search-experts?query=Python+developer&limit=5"
# Expected: Ranked results with similarity scores
```

#### **Phase 5 Validation**: Full Pipeline Works
```bash
# Test complete workflow
curl -X POST "http://localhost:8000/upload-cv" -F "file=@sample_cv.pdf"
curl "http://localhost:8000/search-experts?query=skills+from+uploaded+CV"
# Expected: Uploaded CV appears in search results
```

#### **Phase 6 Validation**: Evaluation System Works
```bash
# Test provider evaluation with single CV
curl -X POST "http://localhost:8000/evaluate-single-cv" -F "file=@sample_cv.pdf"
# Expected: Comparison results for all 3 providers (mistral, openai, simple)

# Run full evaluation on test set
curl -X POST "http://localhost:8000/evaluate-providers"
# Expected: Comprehensive report with recommendations

# View evaluation results
curl "http://localhost:8000/evaluation-results"
# Expected: Provider comparison metrics and recommended approach
```

---

## 🎯 **Success Metrics**

### **Technical Metrics**
- ✅ **Text Extraction Accuracy**: >90% for skills, >80% for experience
- ✅ **Embedding Generation**: <5 seconds per CV
- ✅ **Search Performance**: <500ms response time for queries
- ✅ **Agent Integration**: All handoffs work without errors

### **Functional Metrics**  
- ✅ **Search Relevance**: Correct CVs ranked in top 3 for test queries
- ✅ **Provider Flexibility**: Can switch text extraction methods easily
- ✅ **Agent Compatibility**: Works with existing OpenAI Agent SDK patterns
- ✅ **Database Performance**: Handles 100+ CVs with sub-second search

### **Demo Readiness**
- ✅ **Upload Multiple CVs**: Different skills, experience levels
- ✅ **Semantic Search**: "Find Python developer" returns Python CVs
- ✅ **Ranking Quality**: Most relevant results appear first
- ✅ **Error Handling**: Graceful fallbacks for unsupported files

---

## 📋 **Next Steps**

### **Immediate Actions**
1. **Complete Phase 0** (data preparation & schema design)
   - Download 10 diverse test CVs in different formats
   - Design PostgreSQL schema for structured CV data
   - Manually analyze CVs and create ground truth data
2. **Set up PgVector** in local PostgreSQL instance
3. **Choose initial text extraction provider** (recommend starting with Mistral OCR)
4. **Implement Phase 1** (database schema + basic text extraction)
5. **Test with Phase 0 CVs** to validate extraction accuracy

### **Implementation Order**
1. **Database First**: Get PgVector working with existing schema
2. **Text Extraction**: Pick one provider, get it working end-to-end  
3. **Agent Integration**: Extend existing agents with new capabilities
4. **Search API**: Add semantic search endpoints
5. **Polish & Test**: Comprehensive testing and refinement

### **Risk Mitigation**
- **Text Extraction Fallbacks**: Multiple provider options
- **Embedding Model Flexibility**: Easy to switch models/providers
- **Agent Compatibility**: Build on existing OpenAI Agent SDK patterns
- **Performance**: Start with small dataset, optimize incrementally

**Ready to start with Phase 1? Let's set up PgVector and test the foundation! 🚀**

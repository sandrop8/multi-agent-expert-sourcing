"""
CV-related database models
Updated to use existing 'cvs' table + new structured CV data tables
(following FastAPI best practices and CV Semantic Search implementation)
"""

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Text,
    Date,
    DECIMAL,
    ForeignKey,
    JSON,
)
from sqlalchemy.dialects.postgresql import ARRAY
from .base import BaseModel

# ---- CV ORM Models (SQLAlchemy 2.x ORM) ------------------------------
# Note: We use the existing 'cvs' table for file storage (defined in Core below)
# New ORM models store extracted/structured data and link to cvs.id


class CVPersonalInfo(BaseModel):
    """Comprehensive personal information extracted from CVs - Base class for all personal data"""

    __tablename__ = "cv_personal_info"

    cv_id = Column(
        Integer, ForeignKey("cvs.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # REQUIRED PERSONAL DETAILS (must be collected if not in CV)
    first_name = Column(
        String(255), nullable=True
    )  # REQUIRED: Ask user if not extracted from CV
    last_name = Column(
        String(255), nullable=True
    )  # REQUIRED: Ask user if not extracted from CV
    phone = Column(
        String(50), nullable=True
    )  # REQUIRED: Ask user if not extracted from CV

    # OPTIONAL PERSONAL DETAILS
    email = Column(String(255), nullable=True)
    professional_title = Column(String(255), nullable=True)
    summary = Column(Text, nullable=True)

    # ONLINE PRESENCE URLs
    website_url = Column(String(500), nullable=True)  # General website/portfolio
    linkedin_url = Column(String(500), nullable=True)  # LinkedIn profile
    xing_url = Column(
        String(500), nullable=True
    )  # Xing profile (German professional network)
    github_url = Column(
        String(500), nullable=True
    )  # GitHub profile (kept for developers)

    # ADDRESS FIELDS (German address format)
    street = Column(String(255), nullable=True)  # Street name
    street_number = Column(String(20), nullable=True)  # House/building number
    plz = Column(String(10), nullable=True)  # Postal code (PLZ in Germany)
    city = Column(String(255), nullable=True)  # City name
    country = Column(
        String(100), nullable=True
    )  # MUST be from predefined country list, case-sensitive

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
    top_skills = Column(
        ARRAY(String), nullable=True
    )  # Max 5 items, must be from skills_array
    # Total years of professional experience
    total_years_experience = Column(Integer, nullable=True)

    # FREELANCER PLATFORM AVAILABILITY & PRICING
    # Hours per week available (dropdown selection)
    hours_per_week_available = Column(
        Integer, nullable=True
    )  # e.g., 10, 20, 30, 40 hours/week

    # Available start date (when freelancer can start working)
    available_start_date = Column(Date, nullable=True)

    # HOURLY RATE - Support both single rate and range
    # Option 1: Single hourly rate (e.g., €80/hour)
    hourly_rate_single = Column(DECIMAL(8, 2), nullable=True)  # Single rate in currency

    # Option 2: Hourly rate range (e.g., €70-€100/hour)
    hourly_rate_min = Column(DECIMAL(8, 2), nullable=True)  # Minimum rate for range
    hourly_rate_max = Column(DECIMAL(8, 2), nullable=True)  # Maximum rate for range

    # NOTE: Use either single rate OR range, not both
    # - Single rate: populate hourly_rate_single, leave min/max null
    # - Range rate: populate hourly_rate_min + hourly_rate_max, leave single null
    # Currency assumed to be EUR for German market


class CVProfessionalServices(BaseModel):
    """Professional services offered by freelancer - Tree-based structure based on industry selection"""

    __tablename__ = "cv_professional_services"

    cv_id = Column(
        Integer, ForeignKey("cvs.id", ondelete="CASCADE"), nullable=False, index=True
    )

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


class CVEmployment(BaseModel):
    """Employment history extracted from CVs"""

    __tablename__ = "cv_employment"

    cv_id = Column(
        Integer, ForeignKey("cvs.id", ondelete="CASCADE"), nullable=False, index=True
    )

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


class CVEducation(BaseModel):
    """Education background extracted from CVs"""

    __tablename__ = "cv_education"

    cv_id = Column(
        Integer, ForeignKey("cvs.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Education details
    institution = Column(String(255), nullable=False)
    degree = Column(String(255), nullable=False)
    field_of_study = Column(String(255), nullable=True)
    graduation_year = Column(Integer, nullable=True)
    grade_gpa = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    education_order = Column(Integer, default=0, nullable=False)


class CVSkill(BaseModel):
    """Skills and technologies extracted from CVs"""

    __tablename__ = "cv_skills"

    cv_id = Column(
        Integer, ForeignKey("cvs.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Skill details
    skill_name = Column(String(255), nullable=False)
    skill_category = Column(
        String(100), nullable=True, index=True
    )  # 'programming', 'framework', 'tool', 'soft_skill', 'language'
    proficiency_level = Column(
        String(50), nullable=True
    )  # 'beginner', 'intermediate', 'advanced', 'expert'
    years_experience = Column(Integer, nullable=True)
    is_primary_skill = Column(Boolean, default=False, nullable=False)


class CVCertification(BaseModel):
    """Certifications and awards extracted from CVs"""

    __tablename__ = "cv_certifications"

    cv_id = Column(
        Integer, ForeignKey("cvs.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Certification details
    certification_name = Column(String(255), nullable=False)
    issuing_organization = Column(String(255), nullable=True)
    issue_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    credential_id = Column(String(255), nullable=True)
    verification_url = Column(String(500), nullable=True)


class CVProject(BaseModel):
    """Projects mentioned in CVs"""

    __tablename__ = "cv_projects"

    cv_id = Column(
        Integer, ForeignKey("cvs.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Project details
    project_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    technologies_used = Column(
        ARRAY(String), nullable=True
    )  # PostgreSQL array of technologies
    project_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)


# ---- Legacy Core Table (for file storage) ------------------
# This is the MAIN table for storing CV files - all new ORM models link to this

import sqlalchemy as sa
from .base import meta

cvs = sa.Table(
    "cvs",
    meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("filename", sa.String(255)),
    sa.Column("original_filename", sa.String(255)),
    sa.Column("file_size", sa.Integer),
    sa.Column("content_type", sa.String(100)),
    sa.Column("file_data", sa.LargeBinary),  # Store file content as binary
    sa.Column("uploaded_at", sa.DateTime, default=sa.func.now()),
    sa.Column("processed", sa.Boolean, default=False),
)

# NOTE: All new ORM models above link to cvs.id for file reference
# This provides separation: cvs = file storage, new tables = extracted data

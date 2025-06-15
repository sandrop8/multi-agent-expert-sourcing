"""
Ground truth data extraction for Janine Nel's CV.
Updated to match EXACT cv_models.py PostgreSQL schema structure.
This demonstrates how to map CV content to our PostgreSQL database schema.
"""
from datetime import date
from typing import Dict, List, Any, Optional

def extract_janine_nel_cv() -> Dict[str, Any]:
    """
    Extract structured data from Janine Nel's CV based on EXACT cv_models.py PostgreSQL schema.
    This serves as ground truth for benchmarking extraction algorithms.
    """
    
    # File metadata
    file_info = {
        "filename": "Shaw.pdf",  # Original filename from upload
        "original_filename": "Shaw.pdf", 
        "file_format": "pdf",
        "file_size": None,  # Size not specified
        "content_type": "application/pdf",
        "processing_status": "pending"
    }
    
    # EXACT CVPersonalInfo structure matching cv_models.py
    # FOCUS: These are the fields we actually request from OpenAI and test for accuracy
    personal_info = {
        # REQUIRED FIELDS - these are what we test for accuracy
        "first_name": "Janine",
        "last_name": "Nel", 
        "phone": "3868683442",
        "email": "email@email.com",
        "professional_title": "Sales Engineer",
        
        # OPTIONAL PERSONAL DETAILS - requested from OpenAI
        "summary": "Deadline-focused Sales Engineer with six years experience in technical sales, contributing to the 30% growth of income for a regional technology solutions provider over five states, producing and assisting long-term contracts with Fortune 500 clients, and growing territory sixfold up to $350M.",
        
        # ONLINE PRESENCE URLs - requested from OpenAI
        "website_url": None,      # Not provided in CV
        "linkedin_url": "LinkedIn",  # Listed as "LinkedIn" (not full URL)
        "xing_url": None,         # Not provided in CV  
        "github_url": None,       # Not provided in CV
        
        # ADDRESS FIELDS - requested from OpenAI
        "street": "1515 Pacific Ave",
        "street_number": "1515",
        "plz": "90291",           # US ZIP code
        "city": "Los Angeles",
        "country": "United States",
        
        # LANGUAGES (JSON format) - requested from OpenAI
        "languages": [
            {"language": "English", "level": "Native"},
            {"language": "Dutch", "level": "Native"}
        ],
        
        # WORK PREFERENCES - ARRAY(String) field
        "work_preferences": None,  # Not mentioned in CV
        
        # PROFESSIONAL CAPABILITIES & INDUSTRIES - ARRAY(String) field
        "industries": ["Engineering", "Management, Sales & HR"],  # From CV: "Engineering, Management, Sales & HR"
        
        # SKILLS SUMMARY - matches cv_models.py ARRAY(String) fields
        "skills_array": [
            "AutoCAD", "Knowledge of Technical Diagrams", "Industry Trends & Sales Forecasting", 
            "Agile Project Management", "Engineering", "Technical Sales", "Customer Relations",
            "Program Management", "Territory Management"
        ],
        "top_skills": [
            "AutoCAD", "Engineering", "Technical Sales", "Industry Trends & Sales Forecasting", "Agile Project Management"
        ],  # Top 5 skills - subset of skills_array
        
        # FREELANCER FIELDS - Integer and Date fields
        "total_years_experience": 6,  # From summary: "six years experience"
        "hours_per_week_available": None,     # Not mentioned in CV
        "available_start_date": None,         # Not mentioned in CV
        
        # HOURLY RATE FIELDS - DECIMAL(8,2) fields
        "hourly_rate_single": None,           # Not mentioned in CV
        "hourly_rate_min": None,              # Not mentioned in CV
        "hourly_rate_max": None               # Not mentioned in CV
    }
    
    # EXACT CVProfessionalServices structure matching cv_models.py
    professional_services = {
        # Janine works in "Engineering" and "Management, Sales & HR" industries
        "engineering_services": [
            "technical consulting",   # Inferred from Sales Engineer role
            "project management"      # From "Agile Project Management" skill
        ],
        "management_sales_hr_services": [
            "sales services",         # From Sales Engineer role
            "business consulting"     # Inferred from Fortune 500 client work
        ],
        
        # Not applicable for Janine's profile
        "marketing_design_services": None,
        "it_services": None
    }

    # EXACT CVEmployment structure matching cv_models.py
    employment_history = [
        {
            "company_name": "Engen Oil",
            "job_title": "Sales Engineer",
            "description": "Recognized and provided current and future customer necessities in areas of filtration and lubrication products and services.",
            "location": "Jacksonville",
            "start_date": date(2022, 5, 1),
            "end_date": date(2022, 5, 31),  # 1 month duration
            "is_current": False,
            "duration_months": 1,
            "employment_order": 0  # Most recent
        },
        {
            "company_name": "Quest Medical",
            "job_title": "Sales Engineer",
            "description": "Accountable for day-to-day program management, customer relationships, and estimating the shaping and assembly of medical programs for critical Fortune 500 Clients.",
            "location": "Los Angeles",
            "start_date": date(2019, 1, 1),
            "end_date": date(2021, 4, 30),  # January 2019 - April 2021 (28 months)
            "is_current": False,
            "duration_months": 28,
            "employment_order": 1  # Earlier position
        }
    ]
    
    # EXACT CVEducation structure matching cv_models.py
    education = [
        {
            "institution": "Harvard University",
            "degree": "Masters in Industrial Engineering",
            "field_of_study": "Industrial Engineering",
            "graduation_year": 2022,
            "grade_gpa": None,  # Not mentioned
            "description": None,
            "education_order": 0  # Most recent/highest
        }
    ]
    
    # EXACT CVSkill structure matching cv_models.py
    skills_detailed = [
        # Technical skills
        {"skill_name": "AutoCAD", "skill_category": "technical", "proficiency_level": "expert", "years_experience": None, "is_primary_skill": True},
        {"skill_name": "Knowledge of Technical Diagrams", "skill_category": "technical", "proficiency_level": "advanced", "years_experience": None, "is_primary_skill": False},
        
        # Business skills
        {"skill_name": "Industry Trends & Sales Forecasting", "skill_category": "business", "proficiency_level": "advanced", "years_experience": None, "is_primary_skill": True},
        {"skill_name": "Agile Project Management", "skill_category": "business", "proficiency_level": "advanced", "years_experience": None, "is_primary_skill": True},
        
        # Industry knowledge
        {"skill_name": "Engineering", "skill_category": "industry_knowledge", "proficiency_level": "expert", "years_experience": None, "is_primary_skill": True},
        
        # Inferred from work experience
        {"skill_name": "Technical Sales", "skill_category": "business", "proficiency_level": "expert", "years_experience": 6, "is_primary_skill": True},
        {"skill_name": "Customer Relations", "skill_category": "soft_skill", "proficiency_level": "advanced", "years_experience": None, "is_primary_skill": False},
        {"skill_name": "Program Management", "skill_category": "business", "proficiency_level": "advanced", "years_experience": None, "is_primary_skill": False},
        {"skill_name": "Territory Management", "skill_category": "business", "proficiency_level": "advanced", "years_experience": None, "is_primary_skill": False}
    ]
    
    # EXACT CVCertification structure matching cv_models.py
    certifications = [
        {
            "certification_name": "Professional Engineering (PE) Exam",
            "issuing_organization": "National Council of Examiners for Engineering and Surveying (NCEES)",
            "issue_date": date(2018, 1, 1),
            "expiry_date": date(2019, 12, 31),
            "credential_id": None,
            "credential_url": None,
            "description": None
        },
        {
            "certification_name": "Certified Associate in Project Management",
            "issuing_organization": "Project Management Institute (PMI)",
            "issue_date": date(2021, 5, 1),
            "expiry_date": date(2021, 5, 31),  # Same month expiry seems odd, but as listed
            "credential_id": None,
            "credential_url": None,
            "description": None
        }
    ]
    
    # EXACT CVProject structure matching cv_models.py (empty for Janine)
    projects = []  # No projects mentioned in Janine's CV
    
    # Extraction challenges for this CV
    extraction_challenges = [
        "CV is in PDF format requiring text extraction",
        "LinkedIn URL is incomplete - just says 'LinkedIn' without full URL",
        "Email appears generic (email@email.com) - may not be real contact",
        "Some employment dates need calculation (28 months duration)",
        "Skills are categorized but proficiency levels need inference",
        "Professional services need to be mapped from job roles and skills",
        "Address parsing required for street number extraction",
        "Certification expiry dates seem unusual (same month issue/expiry for PMI cert)",
        "Industry classification requires mapping from job titles and skills",
        "Total years experience mentioned in summary but needs validation against employment history"
    ]
    
    return {
        "file_info": file_info,
        "personal_info": personal_info,
        "professional_services": professional_services,
        "employment_history": employment_history,
        "education": education,
        "skills_detailed": skills_detailed,
        "certifications": certifications,
        "projects": projects,
        "extraction_challenges": extraction_challenges
    }

def validate_extraction(data: Dict[str, Any]) -> List[str]:
    """
    Validate the extracted data against our cv_models.py schema requirements.
    Returns list of validation errors.
    """
    errors = []
    
    # Required file info fields
    required_file_fields = ["filename", "file_format", "content_type"]
    for field in required_file_fields:
        if not data["file_info"].get(field):
            errors.append(f"Missing required file field: {field}")
    
    # Personal info validation - check required fields
    personal = data["personal_info"]
    required_personal_fields = ["first_name", "last_name", "phone", "email", "professional_title"]
    for field in required_personal_fields:
        if not personal.get(field):
            errors.append(f"Missing required personal info field: {field}")
    
    # Employment validation
    for i, emp in enumerate(data["employment_history"]):
        if not emp.get("company_name"):
            errors.append(f"Employment {i}: Missing company_name")
        if not emp.get("job_title"):
            errors.append(f"Employment {i}: Missing job_title")
    
    # Education validation
    for i, edu in enumerate(data["education"]):
        if not edu.get("institution"):
            errors.append(f"Education {i}: Missing institution")
        if not edu.get("degree"):
            errors.append(f"Education {i}: Missing degree")
    
    # Skills validation
    for i, skill in enumerate(data["skills_detailed"]):
        if not skill.get("skill_name"):
            errors.append(f"Skill {i}: Missing skill_name")
    
    return errors

if __name__ == "__main__":
    # Test the extraction
    janine_data = extract_janine_nel_cv()
    errors = validate_extraction(janine_data)
    
    if errors:
        print("❌ Validation errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Janine Nel CV extraction validated successfully!")
        print(f"📊 Extracted data summary:")
        print(f"  - Personal info: {janine_data['personal_info']['first_name']} {janine_data['personal_info']['last_name']}")
        print(f"  - Employment history: {len(janine_data['employment_history'])} positions")
        print(f"  - Education: {len(janine_data['education'])} degrees")
        print(f"  - Skills: {len(janine_data['skills_detailed'])} skills")
        print(f"  - Primary skills: {len([s for s in janine_data['skills_detailed'] if s['is_primary_skill']])}")
        print(f"  - Certifications: {len(janine_data['certifications'])} certifications")
        print(f"  - Extraction challenges: {len(janine_data['extraction_challenges'])} noted") 
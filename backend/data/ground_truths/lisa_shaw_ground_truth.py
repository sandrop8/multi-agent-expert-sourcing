"""
Ground truth data extraction for Lisa Shaw's CV.
Updated to match EXACT cv_models.py PostgreSQL schema structure.
This demonstrates how to map CV content to our PostgreSQL database schema.
"""

from datetime import date
from typing import Dict, List, Any


def extract_lisa_shaw_cv() -> Dict[str, Any]:
    """
    Extract structured data from Lisa Shaw's CV based on EXACT cv_models.py PostgreSQL schema.
    This serves as ground truth for benchmarking extraction algorithms.
    """

    # File metadata
    file_info = {
        "filename": "Lisa.jpg",
        "original_filename": "Lisa.jpg",
        "file_format": "jpg",
        "file_size": 662 * 1024,  # Approximate size from directory listing
        "content_type": "image/jpeg",
        "processing_status": "pending",
    }

    # EXACT CVPersonalInfo structure matching cv_models.py
    personal_info = {
        # REQUIRED FIELDS - marked as nullable=True but noted as required
        "first_name": "Lisa",
        "last_name": "Shaw",
        "phone": "105 563 1992",
        # OPTIONAL PERSONAL DETAILS
        "email": "firstname@resumetemplate.org",  # Note: generic email from template
        "professional_title": "Recruitment & Sales Management Professional",
        "summary": """A pro-active and innovative Senior Sales Management Professional offering across-the-board proficiency in:
Business Development | Talent Acquisition | Recruitment | Talent Sourcing | Client Services | Candidate Facilitation |
Extensive interpersonal and communication skills with developed ability to analyze problems, find tangible solutions and
implement new systems and procedures in a fast-paced business environment. Possess a strong drive to achieve set
goals and objectives by always delivering high standards of service excellence in line with the company's vision.""",
        # ONLINE PRESENCE URLs
        "website_url": None,  # Not provided in CV
        "linkedin_url": None,  # Not provided in CV
        "xing_url": None,  # Not provided in CV
        "github_url": None,  # Not provided in CV
        # ADDRESS FIELDS (German format) - extracted from "Indian Trail, North Carolina"
        "street": None,  # Not specified in CV
        "street_number": None,  # Not specified in CV
        "plz": None,  # US address, no PLZ
        "city": "Indian Trail",  # Extracted from location
        "country": "United States",  # Inferred from "North Carolina"
        # LANGUAGES (JSON format) - matches cv_models.py JSON field
        "languages": [
            {
                "language": "English",
                "level": "native",
            }  # Inferred from US location and CV language
        ],
        # WORK PREFERENCES - ARRAY(String) field
        "work_preferences": None,  # Not mentioned in CV - would be ["remote", "on_premise"] or null
        # PROFESSIONAL CAPABILITIES & INDUSTRIES - ARRAY(String) field
        "industries": ["Management, Sales & HR"],  # Inferred from professional focus
        # SKILLS SUMMARY - matches cv_models.py ARRAY(String) fields
        "skills_array": [
            "Business Development",
            "Talent Acquisition",
            "Recruitment",
            "Talent Sourcing",
            "Client Services",
            "Candidate Facilitation",
            "Sales Management",
            "Communication",
            "Problem Analysis",
            "Actuarial Services",
            "Healthcare Recruitment",
            "Risk Management",
        ],
        "top_skills": [
            "Business Development",
            "Talent Acquisition",
            "Recruitment",
            "Sales Management",
            "Client Services",
        ],  # Top 5 skills - subset of skills_array
        # FREELANCER FIELDS - Integer and Date fields
        "total_years_experience": 6,  # Calculated from employment dates (2011-2017)
        "hours_per_week_available": None,  # Not mentioned in CV - Integer field
        "available_start_date": None,  # Not mentioned in CV - Date field
        # HOURLY RATE FIELDS - DECIMAL(8,2) fields
        "hourly_rate_single": None,  # Not mentioned in CV
        "hourly_rate_min": None,  # Not mentioned in CV
        "hourly_rate_max": None,  # Not mentioned in CV
    }

    # EXACT CVProfessionalServices structure matching cv_models.py
    professional_services = {
        # Lisa works in "Management, Sales & HR" industry
        "management_sales_hr_services": [
            "business consulting",  # Inferred from "Business Development" focus
            "HR services",  # Inferred from "Talent Acquisition", "Recruitment"
            "sales services",  # Inferred from "Sales Management Professional"
        ],
        # Not applicable for Lisa's profile - null for unused industry services
        "marketing_design_services": None,
        "engineering_services": None,
        "it_services": None,
    }

    # EXACT CVEmployment structure matching cv_models.py
    employment_history = [
        {
            "company_name": "ABC Recruitment",  # String(255), nullable=False
            "job_title": "Senior Sales Management Professional",  # String(255), nullable=False
            "description": """• Increased yearly sales revenue by 18% in 2017 for Graduate Division
• Established the new Graduate Division in 2016
• Augmented personal sales by 20% in 2014 and by 170% in 2016
• Succeeded as the Top Biller in 2013 and 2015""",  # Text, nullable=True
            "location": None,  # String(255), nullable=True
            "start_date": date(2013, 1, 1),  # Date, nullable=True
            "end_date": date(2017, 12, 31),  # Date, nullable=True
            "is_current": False,  # Boolean, default=False, nullable=False
            "duration_months": 60,  # Integer, nullable=True (2013-2017 = ~5 years)
            "employment_order": 0,  # Integer, default=0, nullable=False (Most recent)
        },
        {
            "company_name": "Nova Placement Services",
            "job_title": "Top Consultant",
            "description": "• Selected as Top Consultant in 2011 and 2012 and received the Travel Incentive for both years",
            "location": None,
            "start_date": date(2011, 1, 1),
            "end_date": date(2012, 12, 31),
            "is_current": False,
            "duration_months": 24,  # 2011-2012 = 2 years
            "employment_order": 1,  # Earlier position
        },
    ]

    # EXACT CVEducation structure matching cv_models.py
    education = [
        {
            "institution": "University of Columbia",  # String(255), nullable=False
            "degree": "Master's Degree",  # String(255), nullable=False
            "field_of_study": "International Business",  # String(255), nullable=True
            "graduation_year": 2009,  # Integer, nullable=True
            "grade_gpa": "GPA 3.9",  # String(50), nullable=True
            "description": None,  # Text, nullable=True
            "education_order": 0,  # Integer, default=0, nullable=False (Most recent/highest)
        },
        {
            "institution": "University of Boston",
            "degree": "Bachelor Honors",
            "field_of_study": "International Business",
            "graduation_year": 2008,
            "grade_gpa": "GPA 3.8",
            "description": None,
            "education_order": 1,  # Earlier degree
        },
    ]

    # EXACT CVSkill structure matching cv_models.py
    skills_detailed = [
        # Core business skills from professional profile
        {
            "skill_name": "Business Development",
            "skill_category": "business",
            "proficiency_level": "expert",
            "years_experience": None,
            "is_primary_skill": True,
        },
        {
            "skill_name": "Talent Acquisition",
            "skill_category": "business",
            "proficiency_level": "expert",
            "years_experience": None,
            "is_primary_skill": True,
        },
        {
            "skill_name": "Recruitment",
            "skill_category": "business",
            "proficiency_level": "expert",
            "years_experience": None,
            "is_primary_skill": True,
        },
        {
            "skill_name": "Talent Sourcing",
            "skill_category": "business",
            "proficiency_level": "expert",
            "years_experience": None,
            "is_primary_skill": True,
        },
        {
            "skill_name": "Client Services",
            "skill_category": "business",
            "proficiency_level": "advanced",
            "years_experience": None,
            "is_primary_skill": True,
        },
        {
            "skill_name": "Candidate Facilitation",
            "skill_category": "business",
            "proficiency_level": "advanced",
            "years_experience": None,
            "is_primary_skill": True,
        },
        # Industry specializations
        {
            "skill_name": "Actuarial Services",
            "skill_category": "industry_knowledge",
            "proficiency_level": "advanced",
            "years_experience": None,
            "is_primary_skill": False,
        },
        {
            "skill_name": "Pensions",
            "skill_category": "industry_knowledge",
            "proficiency_level": "advanced",
            "years_experience": None,
            "is_primary_skill": False,
        },
        {
            "skill_name": "Healthcare Recruitment",
            "skill_category": "industry_knowledge",
            "proficiency_level": "advanced",
            "years_experience": None,
            "is_primary_skill": False,
        },
        {
            "skill_name": "Risk Management",
            "skill_category": "industry_knowledge",
            "proficiency_level": "advanced",
            "years_experience": None,
            "is_primary_skill": False,
        },
        {
            "skill_name": "Engineering & Manufacturing",
            "skill_category": "industry_knowledge",
            "proficiency_level": "advanced",
            "years_experience": None,
            "is_primary_skill": False,
        },
        # Soft skills from profile
        {
            "skill_name": "Communication",
            "skill_category": "soft_skill",
            "proficiency_level": "expert",
            "years_experience": None,
            "is_primary_skill": False,
        },
        {
            "skill_name": "Problem Analysis",
            "skill_category": "soft_skill",
            "proficiency_level": "advanced",
            "years_experience": None,
            "is_primary_skill": False,
        },
        {
            "skill_name": "Sales Management",
            "skill_category": "business",
            "proficiency_level": "expert",
            "years_experience": None,
            "is_primary_skill": True,
        },
    ]

    # EXACT CVCertification structure matching cv_models.py (empty for Lisa)
    certifications = []  # No certifications mentioned in Lisa's CV

    # EXACT CVProject structure matching cv_models.py (empty for Lisa)
    projects = []  # No projects mentioned in Lisa's CV

    # Extraction challenges for this CV
    extraction_challenges = [
        "CV is in image format (JPG) requiring OCR",
        "Employment dates are scattered in achievements rather than structured format",
        "No explicit start/end dates for positions - need to infer from achievement years",
        "Skills are mixed throughout different sections (professional profile, career objectives, specializations)",
        "No technical skills mentioned - primarily business/recruitment focused",
        "Contact email appears to be from a template rather than actual email",
        "No social media or portfolio links provided",
        "Employment descriptions are achievement-focused rather than responsibility-focused",
        "Industry selection must be inferred from job titles and specializations",
        "Professional services need to be mapped from skills and industry focus",
        "Total years experience requires calculation from employment date ranges",
        "Freelancer platform fields (availability, rates) not present in traditional CVs",
        "Skills summary vs detailed skills requires categorization and prioritization",
        "Address format conversion from US to German structure needed",
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
        "extraction_challenges": extraction_challenges,
    }


def validate_extraction(data: Dict[str, Any]) -> List[str]:
    """
    Validate the extracted data against our cv_models.py schema requirements.
    Returns list of validation errors.
    """
    errors = []

    # Required file info fields
    required_file_fields = ["filename", "file_format", "file_size", "content_type"]
    for field in required_file_fields:
        if not data["file_info"].get(field):
            errors.append(f"Missing required file field: {field}")

    # Personal info validation - check required fields
    personal = data["personal_info"]
    required_personal_fields = ["first_name", "last_name", "phone"]
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
    lisa_data = extract_lisa_shaw_cv()
    errors = validate_extraction(lisa_data)

    if errors:
        print("❌ Validation errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Lisa Shaw CV extraction validated successfully!")
        print("📊 Extracted data summary:")
        print(
            f"  - Personal info: {lisa_data['personal_info']['first_name']} {lisa_data['personal_info']['last_name']}"
        )
        print(
            f"  - Employment history: {len(lisa_data['employment_history'])} positions"
        )
        print(f"  - Education: {len(lisa_data['education'])} degrees")
        print(f"  - Skills: {len(lisa_data['skills_detailed'])} skills")
        print(
            f"  - Primary skills: {len([s for s in lisa_data['skills_detailed'] if s['is_primary_skill']])}"
        )
        print(
            f"  - Extraction challenges: {len(lisa_data['extraction_challenges'])} noted"
        )

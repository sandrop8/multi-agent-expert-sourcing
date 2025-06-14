"""
Ground truth data extraction for Lisa Shaw's CV.
Updated to match comprehensive schema with industries, professional services, and freelancer platform fields.
This demonstrates how to map CV content to our updated PostgreSQL schema.
"""
from datetime import date
from typing import Dict, List, Any, Optional

def extract_lisa_shaw_cv() -> Dict[str, Any]:
    """
    Extract structured data from Lisa Shaw's CV based on our updated PostgreSQL schema.
    This serves as ground truth for benchmarking extraction algorithms.
    """
    
    # File metadata
    file_info = {
        "filename": "Lisa.jpg",
        "original_filename": "Lisa.jpg", 
        "file_format": "jpg",
        "file_size": 662 * 1024,  # Approximate size from directory listing
        "content_type": "image/jpeg",
        "processing_status": "pending"
    }
    
    # UPDATED: Comprehensive Personal Information (CVPersonalInfo)
    personal_info = {
        # REQUIRED FIELDS (marked for user follow-up if missing)
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
        "website_url": None,      # Not provided in CV
        "linkedin_url": None,     # Not provided in CV
        "xing_url": None,         # Not provided in CV  
        "github_url": None,       # Not provided in CV
        
        # ADDRESS FIELDS (German format) - extracted from "Indian Trail, North Carolina"
        "street": None,           # Not specified in CV
        "street_number": None,    # Not specified in CV
        "plz": None,              # US address, no PLZ
        "city": "Indian Trail",   # Extracted from location
        "country": "United States", # Inferred from "North Carolina"
        
        # LANGUAGES (JSON format)
        "languages": [
            {"language": "English", "level": "native"}  # Inferred from US location and CV language
        ],
        
        # WORK PREFERENCES
        "work_preferences": None,  # Not mentioned in CV
        
        # PROFESSIONAL CAPABILITIES & INDUSTRIES
        # TODO: Infer from job titles and specializations - Lisa works in recruitment/HR
        "industries": ["Management, Sales & HR"],  # Inferred from professional focus
        
        # SKILLS SUMMARY (separate from detailed CVSkill records)
        # TODO: Extract from professional profile and career objectives
        "skills_array": [
            "Business Development", "Talent Acquisition", "Recruitment", "Talent Sourcing", 
            "Client Services", "Candidate Facilitation", "Sales Management", "Communication",
            "Problem Analysis", "Actuarial Services", "Healthcare Recruitment", "Risk Management"
        ],
        "top_skills": [
            "Business Development", "Talent Acquisition", "Recruitment", "Sales Management", "Client Services"
        ],  # Top 5 skills from is_primary_skill=True
        "total_years_experience": None,  # TODO: Calculate from employment dates (2011-2017 = ~6 years)
        
        # FREELANCER PLATFORM AVAILABILITY & PRICING
        # NOTE: These fields are typically not found in CVs and would need user input
        "hours_per_week_available": None,     # Not mentioned in CV
        "available_start_date": None,         # Not mentioned in CV
        "hourly_rate_single": None,           # Not mentioned in CV
        "hourly_rate_min": None,              # Not mentioned in CV
        "hourly_rate_max": None               # Not mentioned in CV
    }
    
    # NEW: Professional Services (CVProfessionalServices)
    # Based on Lisa's industry selection and specializations mentioned in CV
    professional_services = {
        # Lisa works in "Management, Sales & HR" industry
        "management_sales_hr_services": [
            "business consulting",    # Inferred from "Business Development" focus
            "HR services",           # Inferred from "Talent Acquisition", "Recruitment"
            "sales services"         # Inferred from "Sales Management Professional"
            # Could also include: "agile coaching", "project management", "strategy consulting"
        ],
        
        # Not applicable for Lisa's profile
        "marketing_design_services": None,
        "engineering_services": None,
        "it_services": None
    }

    # Employment History (unchanged structure, but added employment_order)
    employment_history = [
        {
            "company_name": "ABC Recruitment",
            "job_title": "Senior Sales Management Professional",  # Inferred from achievements
            "description": """• Increased yearly sales revenue by 18% in 2017 for Graduate Division
            • Established the new Graduate Division in 2016
            • Augmented personal sales by 20% in 2014 and by 170% in 2016
            • Succeeded as the Top Biller in 2013 and 2015""",
            "location": None,
            "start_date": date(2013, 1, 1),  # Earliest mentioned year
            "end_date": date(2017, 12, 31),  # Latest mentioned year
            "is_current": False,
            "duration_months": 60,  # 2013-2017 = ~5 years
            "employment_order": 0  # Most recent
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
            "employment_order": 1  # Earlier position
        }
    ]
    
    # Education (unchanged structure, but added education_order)
    education = [
        {
            "institution": "University of Columbia",
            "degree": "Master's Degree",
            "field_of_study": "International Business",
            "graduation_year": 2009,
            "grade_gpa": "GPA 3.9",
            "description": None,
            "education_order": 0  # Most recent/highest degree
        },
        {
            "institution": "University of Boston", 
            "degree": "Bachelor Honors",
            "field_of_study": "International Business",
            "graduation_year": 2008,
            "grade_gpa": "GPA 3.8",
            "description": None,
            "education_order": 1  # Earlier degree
        }
    ]
    
    # RENAMED: Detailed Skills (CVSkill records) - unchanged from original
    skills_detailed = [
        # Core business skills from professional profile
        {"skill_name": "Business Development", "skill_category": "business", "proficiency_level": "expert", "years_experience": None, "is_primary_skill": True},
        {"skill_name": "Talent Acquisition", "skill_category": "business", "proficiency_level": "expert", "years_experience": None, "is_primary_skill": True},
        {"skill_name": "Recruitment", "skill_category": "business", "proficiency_level": "expert", "years_experience": None, "is_primary_skill": True},
        {"skill_name": "Talent Sourcing", "skill_category": "business", "proficiency_level": "expert", "years_experience": None, "is_primary_skill": True},
        {"skill_name": "Client Services", "skill_category": "business", "proficiency_level": "advanced", "years_experience": None, "is_primary_skill": True},
        {"skill_name": "Candidate Facilitation", "skill_category": "business", "proficiency_level": "advanced", "years_experience": None, "is_primary_skill": True},
        
        # Industry specializations
        {"skill_name": "Actuarial Services", "skill_category": "industry_knowledge", "proficiency_level": "advanced", "years_experience": None, "is_primary_skill": False},
        {"skill_name": "Pensions", "skill_category": "industry_knowledge", "proficiency_level": "advanced", "years_experience": None, "is_primary_skill": False},
        {"skill_name": "Healthcare Recruitment", "skill_category": "industry_knowledge", "proficiency_level": "advanced", "years_experience": None, "is_primary_skill": False},
        {"skill_name": "Risk Management", "skill_category": "industry_knowledge", "proficiency_level": "advanced", "years_experience": None, "is_primary_skill": False},
        {"skill_name": "Engineering & Manufacturing", "skill_category": "industry_knowledge", "proficiency_level": "advanced", "years_experience": None, "is_primary_skill": False},
        
        # Soft skills from profile
        {"skill_name": "Communication", "skill_category": "soft_skill", "proficiency_level": "expert", "years_experience": None, "is_primary_skill": False},
        {"skill_name": "Problem Analysis", "skill_category": "soft_skill", "proficiency_level": "advanced", "years_experience": None, "is_primary_skill": False},
        {"skill_name": "Sales Management", "skill_category": "business", "proficiency_level": "expert", "years_experience": None, "is_primary_skill": True}
    ]
    
    # Certifications (none explicitly mentioned in Lisa's CV)
    certifications = []
    
    # Projects (none explicitly mentioned in Lisa's CV)
    projects = []
    
    # UPDATED: Extraction challenges for new schema
    extraction_challenges = [
        "CV is in image format (JPG) requiring OCR",
        "Employment dates are scattered in achievements rather than structured format",
        "No explicit start/end dates for positions - need to infer from achievement years",
        "Skills are mixed throughout different sections (professional profile, career objectives, specializations)",
        "No technical skills mentioned - primarily business/recruitment focused",
        "Contact email appears to be from a template rather than actual email",
        "No social media or portfolio links provided",
        "Employment descriptions are achievement-focused rather than responsibility-focused",
        # NEW CHALLENGES for updated schema:
        "Industry selection must be inferred from job titles and specializations",
        "Professional services need to be mapped from skills and industry focus",
        "Total years experience requires calculation from employment date ranges",
        "Freelancer platform fields (availability, rates) not present in traditional CVs",
        "Skills summary vs detailed skills requires categorization and prioritization",
        "Address format conversion from US to German structure needed"
    ]
    
    return {
        "file_info": file_info,
        "personal_info": personal_info,
        "professional_services": professional_services,  # NEW
        "employment_history": employment_history,
        "education": education,
        "skills_detailed": skills_detailed,  # RENAMED from "skills"
        "certifications": certifications,
        "projects": projects,
        # "languages" removed - now integrated into personal_info
        "extraction_challenges": extraction_challenges
    }

def validate_extraction(data: Dict[str, Any]) -> List[str]:
    """
    Validate the extracted data against our schema requirements.
    Returns list of validation errors.
    """
    errors = []
    
    # Required file info fields
    required_file_fields = ["filename", "file_format", "file_size", "content_type"]
    for field in required_file_fields:
        if not data["file_info"].get(field):
            errors.append(f"Missing required file field: {field}")
    
    # Personal info validation
    personal = data["personal_info"]
    if not personal.get("full_name"):
        errors.append("Missing full_name in personal_info")
    
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
        print(f"📊 Extracted data summary:")
        print(f"  - Personal info: {lisa_data['personal_info']['full_name']}")
        print(f"  - Employment history: {len(lisa_data['employment_history'])} positions")
        print(f"  - Education: {len(lisa_data['education'])} degrees")
        print(f"  - Skills: {len(lisa_data['skills_detailed'])} skills")
        print(f"  - Primary skills: {len([s for s in lisa_data['skills_detailed'] if s['is_primary_skill']])}")
        print(f"  - Extraction challenges: {len(lisa_data['extraction_challenges'])} noted") 
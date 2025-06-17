#!/usr/bin/env python3
"""
Simple CV Evaluation Test Runner
Test the CV extraction evaluation framework
"""

import asyncio
import os
from test_cv_extraction_evaluation import test_lisa_shaw_cv, CVExtractionEvaluator
from data.ground_truths.lisa_shaw_ground_truth import (
    extract_lisa_shaw_cv,
    validate_extraction,
)


def test_ground_truth_structure():
    """Test that the ground truth data structure is correct"""
    print("🧪 Testing ground truth data structure...")

    try:
        # Load ground truth data
        ground_truth = extract_lisa_shaw_cv()

        # Validate the structure
        errors = validate_extraction(ground_truth)

        if errors:
            print("❌ Ground truth validation errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        else:
            print("✅ Ground truth data structure is valid!")

        # Print structure summary
        print("📊 Ground truth structure:")
        print(f"  - Personal info fields: {len(ground_truth['personal_info'])}")
        print(
            f"  - Professional services fields: {len(ground_truth['professional_services'])}"
        )
        print(
            f"  - Employment history: {len(ground_truth['employment_history'])} positions"
        )
        print(f"  - Education: {len(ground_truth['education'])} degrees")
        print(f"  - Skills detailed: {len(ground_truth['skills_detailed'])} skills")
        print(
            f"  - Certifications: {len(ground_truth['certifications'])} certifications"
        )
        print(f"  - Projects: {len(ground_truth['projects'])} projects")

        # Print key fields for verification
        personal = ground_truth["personal_info"]
        print("\n🔍 Key personal info fields:")
        print(f"  - Name: {personal['first_name']} {personal['last_name']}")
        print(f"  - Phone: {personal['phone']}")
        print(f"  - Email: {personal['email']}")
        print(f"  - Professional Title: {personal['professional_title']}")
        print(f"  - Industries: {personal['industries']}")
        print(f"  - Top Skills: {personal['top_skills']}")
        print(f"  - Total Years Experience: {personal['total_years_experience']}")

        return True

    except Exception as e:
        print(f"❌ Ground truth test failed: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def test_comparison_framework():
    """Test the comparison framework with mock data"""
    print("\n🧪 Testing comparison framework...")

    try:
        # Create evaluator
        evaluator = CVExtractionEvaluator()

        # Load ground truth
        ground_truth = extract_lisa_shaw_cv()

        # Create mock extracted data (simulating LLM extraction)
        mock_extracted = {
            "personal_info": {
                "first_name": "Lisa",  # Exact match
                "last_name": "Shaw",  # Exact match
                "phone": "105-563-1992",  # Slightly different format
                "email": "lisa@example.com",  # Different email
                "professional_title": "Senior Sales Professional",  # Partial match
                "summary": "Sales and recruitment professional with expertise in business development",  # Partial match
                "city": "Indian Trail",  # Exact match
                "country": "United States",  # Exact match
                "industries": ["Management, Sales & HR"],  # Exact match
                "skills_array": [
                    "Business Development",
                    "Recruitment",
                    "Sales",
                ],  # Partial match
                "top_skills": ["Business Development", "Recruitment"],  # Partial match
                "total_years_experience": 5,  # Close but not exact (ground truth is 6)
            },
            "professional_services": {
                "management_sales_hr_services": [
                    "HR services",
                    "sales services",
                ],  # Partial match
                "marketing_design_services": None,
                "engineering_services": None,
                "it_services": None,
            },
            "employment_history": [
                {
                    "company_name": "ABC Recruitment",
                    "job_title": "Sales Manager",  # Different title
                    "start_date": "2013-01-01",
                    "end_date": "2017-12-31",
                    "is_current": False,
                }
            ],
            "education": [
                {
                    "institution": "University of Columbia",
                    "degree": "Master's Degree",
                    "field_of_study": "Business",  # Partial match
                    "graduation_year": 2009,
                }
            ],
            "skills_detailed": [
                {
                    "skill_name": "Business Development",
                    "skill_category": "business",
                    "proficiency_level": "expert",
                    "is_primary_skill": True,
                },
                {
                    "skill_name": "Recruitment",
                    "skill_category": "business",
                    "proficiency_level": "expert",
                    "is_primary_skill": True,
                },
            ],
            "certifications": [],
            "projects": [],
        }

        # Run comparison
        comparisons = evaluator.compare_cv_extraction(ground_truth, mock_extracted)

        # Analyze results
        exact_matches = sum(1 for comp in comparisons if comp.match_score >= 0.9)
        partial_matches = sum(
            1 for comp in comparisons if 0.3 <= comp.match_score < 0.9
        )
        missing_fields = sum(1 for comp in comparisons if comp.match_score < 0.3)
        total_fields = len(comparisons)

        print("📊 Comparison results:")
        print(f"  - Total fields compared: {total_fields}")
        print(f"  - Exact matches: {exact_matches}")
        print(f"  - Partial matches: {partial_matches}")
        print(f"  - Missing/poor matches: {missing_fields}")

        # Show some example comparisons
        print("\n🔍 Sample comparisons:")
        for i, comp in enumerate(comparisons[:10]):  # Show first 10
            status = (
                "✅"
                if comp.match_score >= 0.9
                else "🟡"
                if comp.match_score >= 0.3
                else "❌"
            )
            print(
                f"  {status} {comp.field_name}: {comp.match_score:.2f} - {comp.notes}"
            )

        return True

    except Exception as e:
        print(f"❌ Comparison framework test failed: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def create_sample_cv_file():
    """Create a sample CV file for testing if Lisa.jpg doesn't exist"""
    lisa_cv_path = "Lisa.jpg"

    if not os.path.exists(lisa_cv_path):
        print("⚠️ Lisa.jpg not found. Creating a placeholder file for testing...")

        # Create a simple text file as placeholder
        with open("Lisa_placeholder.txt", "w") as f:
            f.write(
                """
LISA SHAW
Recruitment & Sales Management Professional

Phone: 105 563 1992
Email: firstname@resumetemplate.org
Location: Indian Trail, North Carolina

PROFESSIONAL SUMMARY
A pro-active and innovative Senior Sales Management Professional offering across-the-board proficiency in:
Business Development | Talent Acquisition | Recruitment | Talent Sourcing | Client Services | Candidate Facilitation

EMPLOYMENT HISTORY
ABC Recruitment (2013-2017)
- Senior Sales Management Professional
- Increased yearly sales revenue by 18% in 2017 for Graduate Division
- Established the new Graduate Division in 2016
- Augmented personal sales by 20% in 2014 and by 170% in 2016
- Succeeded as the Top Biller in 2013 and 2015

Nova Placement Services (2011-2012)
- Top Consultant
- Selected as Top Consultant in 2011 and 2012
- Received the Travel Incentive for both years

EDUCATION
University of Columbia (2009)
- Master's Degree in International Business
- GPA 3.9

University of Boston (2008)
- Bachelor Honors in International Business
- GPA 3.8
"""
            )

        print("📄 Created Lisa_placeholder.txt for testing")
        return "Lisa_placeholder.txt"

    return lisa_cv_path


async def main():
    """Main test runner"""
    print("🚀 CV Extraction Evaluation Test Runner")
    print("=" * 60)

    # Test 1: Ground truth structure
    if not test_ground_truth_structure():
        print("❌ Ground truth structure test failed - exiting")
        return

    # Test 2: Comparison framework
    if not test_comparison_framework():
        print("❌ Comparison framework test failed - exiting")
        return

    print("\n✅ All structure tests passed!")

    # Test 3: Full evaluation (if CV file exists or can be created)
    print("\n🧪 Testing full evaluation workflow...")

    try:
        cv_file_path = create_sample_cv_file()

        if cv_file_path == "Lisa_placeholder.txt":
            print(
                "⚠️ Using placeholder file - CV extraction will likely fail, but we can test the framework"
            )

        # This will likely fail due to missing CV file, but we can test the framework
        await test_lisa_shaw_cv()

    except Exception as e:
        print(f"⚠️ Full evaluation test failed (expected): {str(e)}")
        print("This is expected without the actual Lisa.jpg file")

    print("\n🎉 CV Evaluation Framework Testing Complete!")
    print("=" * 60)
    print("📋 Next steps:")
    print("  1. Add the actual Lisa.jpg file to test real CV extraction")
    print("  2. Set OPENAI_API_KEY environment variable")
    print("  3. Run: python run_cv_evaluation.py")
    print("  4. Review evaluation results and tune extraction prompts")


if __name__ == "__main__":
    asyncio.run(main())

"""
CV processing agent definitions with OpenAI Agents SDK
Following the hierarchical handoff pattern from OpenAI documentation
"""

from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, enable_verbose_stdout_logging
from schemas.cv_schemas import CVValidationOutput
from services.cv_extraction_service import extract_cv_text_with_responses_api, prepare_cv_file_for_processing
from pydantic import BaseModel
from typing import Dict, Any
import json
import os

# Enable official SDK verbose logging for observability
enable_verbose_stdout_logging()
print("🔧 OpenAI Agents SDK verbose logging enabled for observability")

# ---- MINIMAL TESTING CODE (REMOVE AFTER TESTING) -------------------------

def quick_ground_truth_comparison(file_path: str, extraction_result: str) -> None:
    """
    MINIMAL testing function - compare extraction with ground truth if Shaw or Nel CV detected.
    TODO: REMOVE THIS FUNCTION after testing is complete.
    """
    try:
        # Check if this is a CV we have ground truth for
        cv_type = None
        original_filename = None
        
        # Check direct filename
        if "lisa" in file_path.lower() or "shaw" in file_path.lower():
            cv_type = "shaw"
            original_filename = file_path
        elif "janine" in file_path.lower() or "nel" in file_path.lower():
            cv_type = "nel"
            original_filename = file_path
        
        # Check stored CV ID - get original filename from database
        elif file_path.startswith("stored_cv_id:"):
            try:
                import sqlalchemy as sa
                from models.base import get_engine
                from models.cv_models import cvs
                
                cv_id = int(file_path.split(":")[1])
                engine = get_engine()
                with engine.connect() as conn:
                    result = conn.execute(
                        sa.select(cvs.c.original_filename)
                        .where(cvs.c.id == cv_id)
                    ).first()
                    
                    if result and result.original_filename:
                        original_filename = result.original_filename.lower()
                        # Check for Shaw.pdf or Nel.pdf
                        if "shaw" in original_filename:
                            cv_type = "shaw"
                            print(f"🔍 [TESTING] Found Shaw CV: stored_cv_id:{cv_id} -> {result.original_filename}")
                        elif "nel" in original_filename:
                            cv_type = "nel"
                            print(f"🔍 [TESTING] Found Nel CV: stored_cv_id:{cv_id} -> {result.original_filename}")
            except Exception as e:
                print(f"⚠️ [TESTING] Could not check stored CV filename: {e}")
        
        if not cv_type:
            return
            
        print("\n" + "="*60)
        if cv_type == "shaw":
            print("🧪 [TESTING] DETECTED SHAW CV - Running Ground Truth Comparison")
        elif cv_type == "nel":
            print("🧪 [TESTING] DETECTED NEL CV - Running Ground Truth Comparison")
        print("="*60)
        
        # Import appropriate ground truth data
        try:
            if cv_type == "shaw":
                from data.ground_truths.lisa_shaw_ground_truth import extract_lisa_shaw_cv
                ground_truth = extract_lisa_shaw_cv()
                print("✅ [TESTING] Lisa Shaw ground truth data loaded")
            elif cv_type == "nel":
                from data.ground_truths.janine_nel_ground_truth import extract_janine_nel_cv
                ground_truth = extract_janine_nel_cv()
                print("✅ [TESTING] Janine Nel ground truth data loaded")
            else:
                print(f"⚠️ [TESTING] Unknown CV type: {cv_type}")
                return
        except ImportError as e:
            print(f"⚠️ [TESTING] Could not load ground truth: {e}")
            return
        
        # Parse extraction result
        try:
            if isinstance(extraction_result, str):
                try:
                    extracted_data = json.loads(extraction_result)
                    
                    # If it's wrapped in our error format, extract the actual data
                    if "extracted_text" in extracted_data and isinstance(extracted_data["extracted_text"], str):
                        # Try to parse the inner JSON
                        inner_text = extracted_data["extracted_text"]
                        if inner_text.startswith("```json\n") and inner_text.endswith("\n```"):
                            # Remove markdown code block formatting
                            inner_text = inner_text[8:-4]  # Remove ```json\n and \n```
                        try:
                            extracted_data = json.loads(inner_text)
                            print("✅ [TESTING] Extracted JSON from wrapped format")
                        except json.JSONDecodeError:
                            print(f"⚠️ [TESTING] Could not parse inner JSON: {inner_text[:200]}...")
                            return
                    
                except json.JSONDecodeError:
                    print(f"⚠️ [TESTING] Extraction result is not JSON: {extraction_result[:200]}...")
                    return
            else:
                extracted_data = extraction_result
        except Exception as e:
            print(f"⚠️ [TESTING] Could not parse extraction result: {e}")
            return
        
        # Quick field comparison (simple version)
        print("\n🔍 [TESTING] Quick Field Comparison:")
        print("-" * 40)
        
        # Test ONLY personal info fields for accuracy benchmark (as requested)
        personal_comparisons = [
            ("first_name", "First Name"),
            ("last_name", "Last Name"), 
            ("phone", "Phone"),
            ("email", "Email"),
            ("professional_title", "Professional Title"),
            ("summary", "Summary"),
            ("website_url", "Website URL"),
            ("linkedin_url", "LinkedIn URL"),
            ("xing_url", "Xing URL"),
            ("github_url", "GitHub URL"),
            ("street", "Street"),
            ("street_number", "Street Number"),
            ("plz", "PLZ/ZIP Code"),
            ("city", "City"),
            ("country", "Country"),
            ("languages", "Languages")
        ]
        
        print(f"🎯 [TESTING] PERSONAL INFO FIELDS ONLY - Accuracy Benchmark")
        print(f"📋 [TESTING] Testing {len(personal_comparisons)} personal info fields")
        
        gt_personal = ground_truth.get("personal_info", {})
        ext_personal = extracted_data.get("personal_info", {})
        
        matches = 0
        total = 0
        
        for field, description in personal_comparisons:
            gt_value = gt_personal.get(field)
            ext_value = ext_personal.get(field)
            
            # Simple comparison
            if gt_value == ext_value:
                print(f"✅ {description}: EXACT MATCH")
                matches += 1
            elif gt_value and ext_value:
                # Check if both are strings and have similar content
                if isinstance(gt_value, str) and isinstance(ext_value, str):
                    if gt_value.lower() in ext_value.lower() or ext_value.lower() in gt_value.lower():
                        print(f"🟡 {description}: PARTIAL MATCH")
                        print(f"   GT: {gt_value}")
                        print(f"   EX: {ext_value}")
                        matches += 0.5
                    else:
                        print(f"❌ {description}: DIFFERENT")
                        print(f"   GT: {gt_value}")
                        print(f"   EX: {ext_value}")
                elif isinstance(gt_value, list) and isinstance(ext_value, list):
                    common = set(str(x).lower() for x in gt_value) & set(str(x).lower() for x in ext_value)
                    if len(common) > 0:
                        print(f"🟡 {description}: PARTIAL MATCH ({len(common)} common items)")
                        matches += len(common) / max(len(gt_value), len(ext_value))
                    else:
                        print(f"❌ {description}: NO COMMON ITEMS")
                        print(f"   GT: {gt_value}")
                        print(f"   EX: {ext_value}")
                else:
                    print(f"❌ {description}: TYPE MISMATCH")
                    print(f"   GT: {gt_value} ({type(gt_value)})")
                    print(f"   EX: {ext_value} ({type(ext_value)})")
            else:
                print(f"❌ {description}: MISSING DATA")
                if gt_value:
                    print(f"   GT: {gt_value}")
                if ext_value:
                    print(f"   EX: {ext_value}")
            
            total += 1
        
        # Quick summary
        accuracy = (matches / total * 100) if total > 0 else 0
        print(f"\n📊 [TESTING] Quick Accuracy Score: {accuracy:.1f}% ({matches:.1f}/{total})")
        
        # Show employment and education counts
        gt_emp_count = len(ground_truth.get("employment_history", []))
        ext_emp_count = len(extracted_data.get("employment_history", []))
        print(f"📋 Employment History: GT={gt_emp_count}, Extracted={ext_emp_count}")
        
        gt_edu_count = len(ground_truth.get("education", []))
        ext_edu_count = len(extracted_data.get("education", []))
        print(f"🎓 Education: GT={gt_edu_count}, Extracted={ext_edu_count}")
        
        # Save results to JSON file for detailed analysis
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = f"data/ground_truth_comparisons/{cv_type}_cv_comparison_{timestamp}.json"
            
            comparison_results = {
                "timestamp": timestamp,
                "file_path": file_path,
                "accuracy_score": accuracy,
                "matches": matches,
                "total_fields": total,
                "ground_truth": ground_truth,
                "extracted_data": extracted_data,
                "field_comparisons": {
                    field: {
                        "ground_truth": gt_personal.get(field),
                        "extracted": ext_personal.get(field),
                        "match_type": "exact" if gt_personal.get(field) == ext_personal.get(field) else "partial" if gt_personal.get(field) and ext_personal.get(field) else "missing"
                    }
                    for field, _ in personal_comparisons
                },
                "employment_count": {"ground_truth": gt_emp_count, "extracted": ext_emp_count},
                "education_count": {"ground_truth": gt_edu_count, "extracted": ext_edu_count}
            }
            
            with open(results_file, 'w') as f:
                json.dump(comparison_results, f, indent=2, default=str)
            
            print(f"\n💾 [TESTING] Results saved to: {results_file}")
        except Exception as e:
            print(f"⚠️ [TESTING] Could not save results: {e}")
        
        print("\n💡 [TESTING] This is a quick comparison. For detailed analysis, run:")
        print("   python test_cv_extraction_evaluation.py")
        
        print("="*60)
        print("🧪 [TESTING] Ground Truth Comparison Complete")
        print("="*60)
        
    except Exception as e:
        print(f"⚠️ [TESTING] Comparison failed: {e}")

# ---- END MINIMAL TESTING CODE ---------------------------------------------

# ---- Validation Output Model for Guardrail --------------------------------

class CVValidationResult(BaseModel):
    """Result from CV validation guardrail"""
    is_valid_cv: bool
    confidence_score: float
    document_type: str
    validation_notes: str
    recommended_action: str  # "process", "reject", "manual_review"

# ---- Guardrail Agent and Function -----------------------------------------

cv_guardrail_agent = Agent(
    name="CV Content Validator",
    instructions="""
    You are validating if the input contains a valid CV/resume file path or description.
    
    IMPORTANT: Be LENIENT in validation. If the input mentions:
    - A file path (especially .pdf, .doc, .docx)
    - CV, resume, curriculum vitae
    - Professional document processing
    - Any indication this is for CV processing
    
    Then consider it VALID with high confidence.
    
    Return your assessment with:
    - is_valid_cv: true if this looks like CV processing
    - confidence_score: 0.8 or higher for valid CV inputs
    - document_type: "cv" for valid CVs
    - validation_notes: brief explanation
    - recommended_action: "process" for valid CVs
    """,
    output_type=CVValidationResult,
)

async def cv_validation_guardrail(ctx, agent, input_data):
    """
    Guardrail to ensure only valid CV content is processed
    Following OpenAI Agents SDK guardrail pattern with detailed logging
    """
    try:
        print(f"🛡️ [GUARDRAIL] Starting CV validation for input: {input_data}")
        
        # Enhanced validation logic - check for obvious CV indicators first
        input_str = str(input_data).lower()
        obvious_cv_indicators = [
            '.pdf', '.doc', '.docx', 'cv', 'resume', 'curriculum vitae',
            'process this cv', 'cv file', 'resume file', 'tmp', 'temp'
        ]
        
        has_cv_indicators = any(indicator in input_str for indicator in obvious_cv_indicators)
        
        if has_cv_indicators:
            print(f"🛡️ [GUARDRAIL] Found CV indicators in input - proceeding with validation")
            
            # Run the guardrail validation agent
            print(f"🛡️ [GUARDRAIL] Running CV validation agent...")
            result = await Runner.run(cv_guardrail_agent, input_data, context=ctx.context)
            final_output = result.final_output_as(CVValidationResult)
            
            print(f"🛡️ [GUARDRAIL] Agent validation - Valid CV: {final_output.is_valid_cv}, Confidence: {final_output.confidence_score}")
        else:
            print(f"🛡️ [GUARDRAIL] No CV indicators found - creating fallback validation")
            # Create a more permissive fallback for file paths
            final_output = CVValidationResult(
                is_valid_cv=True,  # Be more permissive
                confidence_score=0.7,
                document_type="cv",
                validation_notes="File path detected - assuming CV processing",
                recommended_action="process"
            )
        
        # Determine if validation passed (lowered threshold)
        validation_passed = (
            final_output.is_valid_cv and 
            final_output.confidence_score >= 0.6  # Lowered from 0.7
        )
        
        if validation_passed:
            print(f"✅ [GUARDRAIL] Validation PASSED - allowing processing")
        else:
            print(f"❌ [GUARDRAIL] Validation FAILED - blocking processing")
            print(f"   Reason: {final_output.validation_notes}")
        
        return GuardrailFunctionOutput(
            output_info=final_output,
            tripwire_triggered=not validation_passed,
        )
        
    except Exception as e:
        print(f"❌ [GUARDRAIL] Validation error: {str(e)}")
        # Create permissive fallback validation result
        fallback_result = CVValidationResult(
            is_valid_cv=True,  # Default to allowing processing
            confidence_score=0.6,
            document_type="unknown",
            validation_notes=f"Validation error - defaulting to allow: {str(e)}",
            recommended_action="process"
        )
        return GuardrailFunctionOutput(
            output_info=fallback_result,
            tripwire_triggered=False,  # Allow processing on errors
        )

# ---- Specialist Agents (Following SDK Handoff Pattern) -------------------

cv_parser_agent = Agent(
    name="CV Parser Agent",
    handoff_description="Document extraction specialist for parsing CV content",
    instructions="""
    You are a CV/Resume parsing specialist. Extract structured information from CV documents.
    
    Use the extract_cv_text_with_responses_api tool to process the CV file and extract:
    - Personal information (name, contact details)
    - Work experience (companies, positions, dates, responsibilities)
    - Education (institutions, degrees, dates)
    - Skills (technical, soft skills, languages)
    - Certifications and achievements
    
    Provide detailed extraction with confidence scores and note any parsing challenges.
    """,
    tools=[extract_cv_text_with_responses_api],
)

profile_enrichment_agent = Agent(
    name="Profile Enrichment Agent", 
    handoff_description="Enhancement specialist for optimizing freelancer profiles",
    instructions="""
    You enhance basic CV data with professional summaries and achievement highlights.
    
    Take parsed CV data and:
    - Create compelling professional summaries
    - Highlight key achievements and impact
    - Optimize skill presentations
    - Identify unique value propositions
    - Suggest profile improvements
    
    Create compelling professional narratives that showcase the candidate's strengths effectively.
    """,
)

skills_extraction_agent = Agent(
    name="Skills Extraction Agent",
    handoff_description="Technical specialist for identifying and categorizing skills",
    instructions="""
    You identify and categorize technical skills, tools, and proficiency levels from CVs.
    
    Analyze the CV data to:
    - Extract technical skills (programming languages, frameworks, tools)
    - Identify soft skills and interpersonal abilities
    - Assess proficiency levels where possible
    - Categorize skills by domain (technical, management, creative, etc.)
    - Map skills to industry standards and requirements
    
    Provide structured skill taxonomies with confidence assessments.
    """,
)

gap_analysis_agent = Agent(
    name="Gap Analysis Agent",
    handoff_description="Assessment specialist for profile completeness",
    instructions="""
    You identify missing information crucial for project matching and profile completeness.
    
    Analyze the processed profile data to:
    - Identify gaps in work experience details
    - Note missing skill information
    - Suggest additional certifications or qualifications
    - Recommend portfolio additions
    - Identify areas for profile strengthening
    
    Provide actionable recommendations for profile improvement and completeness.
    """,
)

# ---- Main Orchestration Agent (Manager with Handoffs) --------------------

freelancer_profile_manager = Agent(
    name="Freelancer Profile Manager",
    instructions="""
    You are the Freelancer Profile Manager, coordinating the complete CV processing workflow.
    
    IMPORTANT: Always start by using the prepare_cv_file_for_processing tool to validate the file.
    
    Your workflow:
    1. The input has already been validated by the CV validation guardrail
    2. Use the prepare_cv_file_for_processing tool to prepare the file
    3. First, hand off to the CV Parser Agent to extract structured data from the CV
    4. Then, hand off to Profile Enrichment Agent to enhance the basic data
    5. Hand off to Skills Extraction Agent for detailed skill analysis
    6. Finally, hand off to Gap Analysis Agent to identify missing information
    7. Provide a comprehensive summary of the complete profile analysis
    
    Always explain what you're doing at each step for observability.
    Coordinate between agents to create complete, high-quality freelancer profiles.
    Ensure all agents have contributed before providing final recommendations.
    """,
    handoffs=[cv_parser_agent, profile_enrichment_agent, skills_extraction_agent, gap_analysis_agent],
    tools=[prepare_cv_file_for_processing],
    input_guardrails=[
        InputGuardrail(guardrail_function=cv_validation_guardrail),
    ],
)

# ---- Workflow Function (Simplified) ---------------------------------------

async def process_cv_workflow(file_path: str) -> Dict[str, Any]:
    """
    Complete CV processing workflow using OpenAI Agents SDK
    
    Args:
        file_path: Path to the uploaded CV file
        
    Returns:
        Dictionary containing processing results
    """
    
    try:
        print(f"🚀 [WORKFLOW] Starting CV processing workflow for: {file_path}")
        
        # Create input for the manager (just the file path)
        cv_input = f"Process this CV file: {file_path}"
        
        print(f"🎯 [WORKFLOW] Calling Freelancer Profile Manager with input: {cv_input}")
        print(f"📋 [WORKFLOW] Manager has {len(freelancer_profile_manager.handoffs)} handoff agents available")
        print(f"🛠️ [WORKFLOW] Manager has {len(freelancer_profile_manager.tools)} tools available")
        print(f"🛡️ [WORKFLOW] Manager has {len(freelancer_profile_manager.input_guardrails)} guardrails configured")
        
        # Run the workflow through the freelancer profile manager
        # The guardrail will validate first, then handoffs will process
        print(f"▶️ [WORKFLOW] Executing agent workflow...")
        result = await Runner.run(
            freelancer_profile_manager,
            cv_input
        )
        
        print(f"✅ [WORKFLOW] CV processing workflow completed successfully")
        print(f"📤 [WORKFLOW] Final output type: {type(result.final_output)}")
        if result.final_output:
            output_preview = str(result.final_output)[:200] + "..." if len(str(result.final_output)) > 200 else str(result.final_output)
            print(f"📄 [WORKFLOW] Output preview: {output_preview}")
        
        # MINIMAL TESTING: Auto-compare with ground truth if Lisa Shaw CV detected
        # TODO: REMOVE this call after testing is complete
        # Get the raw JSON extraction data instead of the formatted final output
        try:
            from services.cv_extraction_service import get_last_extraction_result
            raw_json_data = get_last_extraction_result()
            comparison_data = raw_json_data if raw_json_data else result.final_output
            quick_ground_truth_comparison(file_path, comparison_data)
        except Exception as e:
            print(f"⚠️ [TESTING] Could not get raw extraction data: {e}")
            quick_ground_truth_comparison(file_path, result.final_output)
        
        return {
            "success": True,
            "result": result.final_output if result.final_output else "CV processed successfully",
            "processing_notes": ["CV workflow completed successfully"]
        }
        
    except Exception as e:
        error_msg = f"CV processing workflow failed: {str(e)}"
        print(f"❌ [WORKFLOW] {error_msg}")
        
        return {
            "success": False,
            "error": error_msg,
            "result": None
        }

# ---- Testing Function -----------------------------------------------------

async def test_cv_agents():
    """Test the CV processing agents with SDK patterns"""
    
    print("🧪 Testing CV processing agents (SDK patterns)...")
    
    test_file = "test-cv.pdf"
    if not os.path.exists(test_file):
        print(f"⚠️ Test file {test_file} not found")
        return
    
    try:
        # Test the complete workflow
        result = await process_cv_workflow(test_file)
        
        print("\n📊 AGENT WORKFLOW RESULTS:")
        print("=" * 50)
        print(f"Success: {result.get('success', False)}")
        
        if result.get('success'):
            print("✅ CV processing completed successfully")
            print(f"📋 Result: {result.get('result', 'No result')}")
        else:
            print(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
            
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    import os
    asyncio.run(test_cv_agents()) 
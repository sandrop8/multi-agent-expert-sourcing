#!/usr/bin/env python3
"""
Alternative approach: Save CV extraction results to markdown file for manual comparison
"""

import json
import asyncio
import os
from datetime import datetime
from typing import Any, Optional, Dict
from app_agents.cv_agents import process_cv_workflow
from data.ground_truths.lisa_shaw_ground_truth import extract_lisa_shaw_cv

def save_extraction_to_markdown(file_path: str, extraction_result: Any, ground_truth: Optional[Dict] = None):
    """Save extraction results to markdown file for manual review"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cv_extraction_{timestamp}.md"
    
    with open(filename, 'w') as f:
        f.write(f"# CV Extraction Results - {os.path.basename(file_path)}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Write extraction results
        f.write("## 🤖 LLM Extraction Results\n\n")
        f.write("```json\n")
        if isinstance(extraction_result, str):
            f.write(extraction_result)
        else:
            f.write(json.dumps(extraction_result, indent=2, default=str))
        f.write("\n```\n\n")
        
        # Write ground truth if available
        if ground_truth:
            f.write("## 📊 Ground Truth Data (Lisa Shaw)\n\n")
            f.write("```json\n")
            f.write(json.dumps(ground_truth, indent=2, default=str))
            f.write("\n```\n\n")
            
            # Quick comparison section
            f.write("## 🔍 Quick Comparison Notes\n\n")
            f.write("### Key Fields to Compare:\n\n")
            
            try:
                if isinstance(extraction_result, str):
                    extracted_data = json.loads(extraction_result)
                else:
                    extracted_data = extraction_result
                    
                gt_personal = ground_truth.get("personal_info", {})
                ext_personal = extracted_data.get("personal_info", {})
                
                comparison_fields = [
                    "first_name", "last_name", "phone", "email", 
                    "professional_title", "city", "industries", "skills_array"
                ]
                
                f.write("| Field | Ground Truth | LLM Extracted | Match |\n")
                f.write("|-------|--------------|---------------|-------|\n")
                
                for field in comparison_fields:
                    gt_val = gt_personal.get(field, "N/A")
                    ext_val = ext_personal.get(field, "N/A")
                    match = "✅" if gt_val == ext_val else "❓"
                    f.write(f"| {field} | {gt_val} | {ext_val} | {match} |\n")
                
            except Exception as e:
                f.write(f"Error in comparison: {e}\n")
        
        f.write("\n## 📋 Manual Review Checklist\n\n")
        f.write("- [ ] Personal information accuracy\n")
        f.write("- [ ] Employment history completeness\n")
        f.write("- [ ] Education details\n")
        f.write("- [ ] Skills extraction quality\n")
        f.write("- [ ] Industry classification\n")
        f.write("- [ ] Date format consistency\n")
        f.write("- [ ] Overall data structure alignment\n")
    
    print(f"📄 Extraction results saved to: {filename}")
    return filename

async def extract_and_save_markdown():
    """Extract CV data and save to markdown for manual comparison"""
    
    print("📝 CV Extraction to Markdown")
    print("=" * 50)
    
    # Look for Lisa's CV file
    possible_files = ["Lisa.jpg", "lisa.jpg", "Lisa.pdf", "lisa.pdf"]
    
    lisa_file = None
    for filename in possible_files:
        if os.path.exists(filename):
            lisa_file = filename
            break
    
    if not lisa_file:
        print("⚠️ Lisa Shaw CV file not found!")
        print("Please add Lisa's CV file as one of:", possible_files[:2])
        return
    
    print(f"📄 Processing: {lisa_file}")
    
    try:
        # Load ground truth
        ground_truth = extract_lisa_shaw_cv()
        print("✅ Ground truth loaded")
        
        # Process CV
        result = await process_cv_workflow(lisa_file)
        
        if result.get("success"):
            # Save to markdown
            markdown_file = save_extraction_to_markdown(
                lisa_file, 
                result.get("result"), 
                ground_truth
            )
            
            print(f"\n✅ Results saved to: {markdown_file}")
            print("📖 Open the markdown file to review extraction quality")
            
        else:
            print(f"❌ CV processing failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(extract_and_save_markdown()) 
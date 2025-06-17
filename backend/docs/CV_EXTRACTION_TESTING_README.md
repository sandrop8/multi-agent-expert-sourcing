# CV Extraction Testing Framework

## Overview

This document describes the CV extraction testing framework we've built to evaluate how well our OpenAI vision-based CV extraction performs against manually curated ground truth data, with perfect alignment to our PostgreSQL database schema.

## 🎯 Key Achievements

### ✅ Database Schema Alignment
- **cv_models.py**: Defines exact PostgreSQL database structure
- **data/ground_truths/lisa_shaw_ground_truth.py**: Ground truth data matching exact field names and data types
- **CV extraction service**: Updated to output data in exact database schema format
- **Evaluation framework**: Compares extracted data against ground truth with detailed metrics

### ✅ Testing Framework Components

1. **Ground Truth Data** (`data/ground_truths/lisa_shaw_ground_truth.py`)
   - Manually analyzed Lisa Shaw's CV
   - Structured data matching `cv_models.py` exactly
   - Field-level validation and error checking

2. **CV Extraction Service** (`services/cv_extraction_service.py`)
   - Updated OpenAI vision prompts to match database schema
   - Comprehensive extraction covering all table structures
   - Detailed extraction rules and field mapping guidelines

3. **Evaluation Framework** (`test_cv_extraction_evaluation.py`)
   - Automated comparison between ground truth and extracted data
   - Field-by-field similarity scoring
   - Detailed metrics and reporting
   - Extensible for testing multiple CVs

4. **Test Runner** (`run_cv_evaluation.py`)
   - Simple test execution without requiring actual CV files
   - Ground truth structure validation
   - Mock data comparison testing
   - Step-by-step evaluation workflow

## 📊 Database Schema Structure

Our PostgreSQL schema (defined in `cv_models.py`) includes:

### Core Tables
- **CVPersonalInfo**: Comprehensive personal data, industries, skills summary, freelancer rates
- **CVProfessionalServices**: Services offered based on industry selection
- **CVEmployment**: Employment history with ordering and duration
- **CVEducation**: Education background with ordering
- **CVSkill**: Individual skills with categories and proficiency
- **CVCertification**: Certifications and credentials
- **CVProject**: Projects and portfolios

### Key Schema Features
- **Required Fields**: `first_name`, `last_name`, `phone` (marked for user follow-up if missing)
- **Array Fields**: `industries`, `skills_array`, `top_skills`, `work_preferences`
- **JSON Fields**: `languages` with structured level information
- **Date Fields**: All dates in YYYY-MM-DD format
- **Ordering Fields**: `employment_order`, `education_order` for proper sequencing

## 🧪 Testing Workflow

### 1. Ground Truth Validation
```bash
cd backend
python run_cv_evaluation.py
```

This validates that our ground truth data structure matches the database schema exactly.

### 2. Comparison Framework Testing
Tests the similarity calculation and field comparison logic with mock data.

### 3. Full CV Extraction Evaluation
```bash
# Set OpenAI API key
export OPENAI_API_KEY="your-api-key"

# Add Lisa Shaw CV file as Lisa.jpg
# Then run full evaluation
python run_cv_evaluation.py
```

### 4. Evaluation Metrics

The framework provides detailed metrics:

- **Overall Accuracy**: Average similarity score across all fields
- **Exact Matches**: Fields with ≥90% similarity
- **Partial Matches**: Fields with 30-90% similarity
- **Missing Fields**: Fields with <30% similarity
- **Field-by-Field Analysis**: Detailed comparison for each database field

## 📋 Evaluation Output Example

```
📊 CV EXTRACTION EVALUATION RESULTS
================================================================================
📄 CV File: Lisa Shaw
⏱️  Extraction Time: 4.23 seconds
📈 Overall Accuracy: 78.5%

📋 FIELD COMPARISON SUMMARY:
  ✅ Exact Matches: 15/32 (46.9%)
  🟡 Partial Matches: 12/32 (37.5%)
  ❌ Missing/Poor: 5/32 (15.6%)

🔍 DETAILED FIELD COMPARISONS:
--------------------------------------------------------------------------------
✅ Personal Info - First Name        | Score: 1.00 | Exact match
✅ Personal Info - Last Name         | Score: 1.00 | Exact match
🟡 Personal Info - Phone             | Score: 0.85 | Partial match (similarity: 0.85)
❌ Personal Info - LinkedIn URL      | Score: 0.00 | Missing extraction for existing ground truth
```

## 🔧 Testing Individual Components

### Test Ground Truth Data Structure
```python
from data.ground_truths.lisa_shaw_ground_truth import extract_lisa_shaw_cv, validate_extraction

ground_truth = extract_lisa_shaw_cv()
errors = validate_extraction(ground_truth)
print(f"Validation errors: {len(errors)}")
```

### Test Comparison Framework
```python
from test_cv_extraction_evaluation import CVExtractionEvaluator

evaluator = CVExtractionEvaluator()
comparisons = evaluator.compare_cv_extraction(ground_truth, extracted_data)
```

### Test CV Extraction Service
```python
from app_agents.cv_agents import process_cv_workflow

result = await process_cv_workflow("Lisa.jpg")
```

## 🎯 Field Mapping Guide

### Personal Info Mapping
| Database Field | Ground Truth | LLM Extraction Focus |
|----------------|--------------|---------------------|
| `first_name` | "Lisa" | Extract first name from any name field |
| `last_name` | "Shaw" | Extract last name from any name field |
| `phone` | "105 563 1992" | Parse phone numbers in any format |
| `industries` | ["Management, Sales & HR"] | Infer from job titles and skills |
| `skills_array` | All skills mentioned | Extract comprehensive skill list |
| `top_skills` | Top 5 primary skills | Identify most important/frequent skills |

### Employment History Mapping
| Database Field | Ground Truth | LLM Extraction Focus |
|----------------|--------------|---------------------|
| `company_name` | "ABC Recruitment" | Extract company names |
| `job_title` | "Senior Sales Management Professional" | Extract or infer job titles |
| `employment_order` | 0 (most recent) | Order by dates, 0 = newest |
| `duration_months` | 60 | Calculate from start/end dates |

## 🚀 Next Steps for Full Implementation

### 1. Add More Test CVs
- Extend ground truth data for all 10 collected CVs
- Test various CV formats (PDF, DOCX, images)
- Include technical and non-technical CVs

### 2. Provider Comparison
- Test Mistral OCR vs OpenAI vs PyPDF2 extraction
- Compare accuracy, speed, and cost metrics
- Optimize provider selection strategy

### 3. Integration with Database
- Implement actual PostgreSQL saving after extraction
- Test database insertion and retrieval
- Validate foreign key relationships

### 4. API Integration
- Add evaluation endpoints to FastAPI
- Create batch processing for multiple CVs
- Implement continuous evaluation monitoring

## 🔍 Current Status

### ✅ Completed
- Database schema definition (`cv_models.py`)
- Ground truth data structure (`data/ground_truths/lisa_shaw_ground_truth.py`)
- CV extraction service with schema alignment
- Comprehensive evaluation framework
- Testing infrastructure

### 🔄 In Progress
- Testing with actual Lisa Shaw CV file
- OpenAI API integration testing
- Field-level accuracy optimization

### 📋 Pending
- Multi-CV evaluation
- Provider comparison testing
- Database integration
- API endpoint implementation

## 💡 Key Benefits

1. **Schema Alignment**: Perfect mapping between extraction and database storage
2. **Evaluation Framework**: Automated testing with detailed metrics
3. **Extensible Design**: Easy to add more CVs and test scenarios
4. **Production Ready**: Proper error handling and validation
5. **Comprehensive Coverage**: Tests all database fields and relationships

This framework provides a solid foundation for evaluating and improving CV extraction quality while ensuring compatibility with our PostgreSQL database schema.

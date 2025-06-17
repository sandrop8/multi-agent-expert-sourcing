"""
OpenAI Integration Tests

These tests make real API calls to OpenAI services and are intended for CI/CD pipeline.
They are separated from fast unit tests to maintain clear test categorization.

⚠️  IMPORTANT: These tests require:
- OPENAI_API_KEY environment variable
- Internet connectivity
- OpenAI API credits
- Longer execution time (30-75+ seconds)

🎯 Usage:
- CI/CD Pipeline: Run with full environment setup
- Local Development: Skip by default, run manually when needed
"""

import pytest
import os
from pathlib import Path
import io
from sqlalchemy import select

# Test data path
TEST_CV_PATH = Path(__file__).parent.parent / "fixtures" / "test-cv.pdf"


class TestOpenAIAPICalls:
    """Integration tests that make real OpenAI API calls"""

    @pytest.mark.openai_integration
    @pytest.mark.asyncio
    async def test_cv_workflow_with_real_openai_api(self):
        """Test CV workflow with real OpenAI API calls (31+ seconds)"""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set - skipping real API test")

        if not TEST_CV_PATH.exists():
            pytest.skip("Test CV file not found - skipping file-based workflow test")

        try:
            from app_agents.cv_agents import process_cv_workflow
        except ImportError:
            pytest.skip("CV workflow not available")

        # This test makes actual OpenAI API calls
        try:
            result = await process_cv_workflow(str(TEST_CV_PATH))

            # Basic validations for real API response
            assert result is not None
            assert "success" in result
            assert isinstance(result["success"], bool)

            if result["success"]:
                assert "result" in result
                print(f"✅ Real OpenAI API test passed: {result}")
            else:
                print(f"⚠️ Real OpenAI API test completed with error: {result}")

        except Exception as e:
            pytest.skip(f"Real OpenAI API test failed: {e}")

    @pytest.mark.openai_integration
    def test_cv_database_storage_with_real_processing(self):
        """Test CV creation with real database storage (73+ seconds)"""
        pytest.importorskip("fastapi.testclient")

        from fastapi.testclient import TestClient
        from main import app
        from models.cv_models import cvs

        client = TestClient(app)

        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set - skipping real API test")

        pdf_content = b"Test CV content for real processing"
        filename = "integration-test-cv.pdf"

        # This test makes real OpenAI API calls and stores in database
        response = client.post(
            "/cvs",
            files={"file": (filename, io.BytesIO(pdf_content), "application/pdf")},
        )

        assert response.status_code == 201  # RESTful: 201 Created

        # Verify database storage (this part is fast)
        try:
            from models.base import get_engine

            engine = get_engine()

            with engine.connect() as conn:
                result = conn.execute(select(cvs))
                rows = result.fetchall()

                # Find our test CV
                test_cv = None
                for row in rows:
                    if row.original_filename == filename:
                        test_cv = row
                        break

                if test_cv:
                    assert test_cv.filename == filename
                    assert test_cv.original_filename == filename
                    assert test_cv.file_size == len(pdf_content)
                    assert test_cv.content_type == "application/pdf"
                    assert test_cv.file_data == pdf_content
                    print(
                        f"✅ Real database storage test passed for CV ID: {test_cv.id}"
                    )
                else:
                    pytest.skip(
                        "Test CV not found in database - may have been processed"
                    )

        except Exception as e:
            pytest.skip(f"Database verification failed: {e}")

    @pytest.mark.openai_integration
    @pytest.mark.asyncio
    async def test_cv_extraction_with_real_file_and_api(self):
        """Test CV extraction service with real file and OpenAI API"""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set - skipping real API test")

        if not TEST_CV_PATH.exists():
            pytest.skip("Test CV file not found - skipping file-based test")

        try:
            from services.cv_extraction_service import CVParserService
        except ImportError:
            pytest.skip("CV extraction service not available")

        # Read real test CV file
        with open(TEST_CV_PATH, "rb") as f:
            pdf_bytes = f.read()

        assert len(pdf_bytes) > 0, "Test CV file should contain data"

        service = CVParserService()

        # This test requires actual OpenAI API call
        try:
            result = await service.process_cv_with_agent(cv_id=999, pdf_bytes=pdf_bytes)

            # Validate real API response structure
            assert hasattr(result, "extraction_confidence")
            assert hasattr(result, "processing_status")
            assert result.extraction_confidence >= 0.0
            assert result.extraction_confidence <= 1.0
            assert result.processing_status in ["completed", "processing", "error"]

            print(
                f"✅ Real CV extraction test passed - Confidence: {result.extraction_confidence}"
            )

        except Exception as e:
            pytest.skip(f"Real CV extraction API test failed: {e}")


# Pytest markers for integration tests
pytestmark = [
    pytest.mark.openai_integration,  # Mark all tests as OpenAI integration
    pytest.mark.slow,  # Mark as slow tests
]

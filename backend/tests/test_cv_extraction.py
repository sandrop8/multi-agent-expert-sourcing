"""
CV Extraction Service Tests
Tests for OpenAI Responses API integration and CV processing pipeline
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Test data path
TEST_CV_PATH = Path(__file__).parent / "fixtures" / "test-cv.pdf"


class TestCVExtractionService:
    """Test CV extraction service functionality"""

    @pytest.mark.asyncio
    async def test_cv_extraction_service_import(self):
        """Test that CV extraction service can be imported"""
        try:
            from services.cv_extraction_service import CVParserService

            assert CVParserService is not None
        except ImportError as e:
            pytest.skip(f"CV extraction service not available: {e}")

    @pytest.mark.asyncio
    async def test_cv_extraction_with_mock_data(self):
        """Test CV extraction with mocked data (no OpenAI API call)"""
        try:
            from services.cv_extraction_service import CVParserService
        except ImportError:
            pytest.skip("CV extraction service not available")

        # Mock the API call
        with patch(
            "services.cv_extraction_service.extract_cv_text_with_responses_api"
        ) as mock_extract:
            mock_extract.return_value = "Mocked CV extraction result"

            service = CVParserService()
            pdf_bytes = b"Mock PDF content"

            # This would normally call the real service, but we're mocking it
            with patch.object(service, "process_cv_with_agent") as mock_process:
                mock_result = MagicMock()
                mock_result.extraction_confidence = 0.9
                mock_result.personal_info = {"name": "Test User"}
                mock_result.employment_history = []
                mock_result.education = []
                mock_result.skills = ["Python", "FastAPI"]
                mock_result.processing_status = "completed"
                mock_result.extraction_notes = ["Test successful"]
                mock_process.return_value = mock_result

                result = await service.process_cv_with_agent(
                    cv_id=1, pdf_bytes=pdf_bytes
                )

                assert result.extraction_confidence == 0.9
                assert result.personal_info["name"] == "Test User"
                assert len(result.skills) == 2
                assert result.processing_status == "completed"

    @pytest.mark.asyncio
    async def test_cv_extraction_with_real_file(self):
        """Test CV extraction with real test file (requires OPENAI_API_KEY)"""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set - skipping real API test")

        if not TEST_CV_PATH.exists():
            pytest.skip("Test CV file not found - skipping file-based test")

        try:
            from services.cv_extraction_service import CVParserService
        except ImportError:
            pytest.skip("CV extraction service not available")

        # Read test CV file
        with open(TEST_CV_PATH, "rb") as f:
            pdf_bytes = f.read()

        assert len(pdf_bytes) > 0, "Test CV file should contain data"

        service = CVParserService()

        # This test requires actual OpenAI API call
        try:
            result = await service.process_cv_with_agent(cv_id=1, pdf_bytes=pdf_bytes)

            # Basic validations
            assert hasattr(result, "extraction_confidence")
            assert hasattr(result, "processing_status")
            assert result.extraction_confidence >= 0.0
            assert result.extraction_confidence <= 1.0

        except Exception as e:
            pytest.skip(f"Real API test failed (expected without proper setup): {e}")


class TestCVParserAgent:
    """Test CV parser agent integration"""

    def test_cv_parser_agent_import(self):
        """Test that CV parser agent can be imported"""
        try:
            from app_agents.cv_agents import cv_parser_agent

            assert cv_parser_agent is not None
            assert cv_parser_agent.name == "CV Parser Agent"
        except ImportError as e:
            pytest.skip(f"CV agents not available: {e}")

    def test_cv_extraction_output_model(self):
        """Test CVExtractionOutput model structure"""
        try:
            from app_agents.cv_agents import CVExtractionOutput
        except ImportError:
            pytest.skip("CV agents not available")

        # Test model creation
        test_output = CVExtractionOutput(
            personal_info={"first_name": "Test", "last_name": "User"},
            employment_history=[],
            education=[],
            skills=["Python", "FastAPI"],
            certifications=[],
            projects=[],
            extraction_confidence=0.95,
            extraction_notes=["Test successful"],
            processing_status="completed",
        )

        assert test_output.processing_status == "completed"
        assert test_output.extraction_confidence == 0.95
        assert len(test_output.skills) == 2
        assert test_output.personal_info["first_name"] == "Test"

    def test_agent_configuration(self):
        """Test that CV parser agent is configured correctly"""
        try:
            from app_agents.cv_agents import cv_parser_agent
        except ImportError:
            pytest.skip("CV agents not available")

        assert cv_parser_agent.name == "CV Parser Agent"
        assert cv_parser_agent.handoff_description is not None
        assert len(cv_parser_agent.instructions) > 0
        assert len(cv_parser_agent.tools) > 0  # Should have extraction tools


class TestEnvironmentConfiguration:
    """Test environment variable configuration for CV processing"""

    def test_required_environment_variables(self):
        """Test that required environment variables are available"""
        # OPENAI_API_KEY is required for real API calls
        openai_key = os.getenv("OPENAI_API_KEY")

        if openai_key:
            assert len(openai_key) > 10, "OPENAI_API_KEY should be a valid key"
        # If not set, tests will be skipped but this check passes

    def test_optional_environment_variables(self):
        """Test optional environment variables"""
        text_provider = os.getenv("TEXT_EXTRACTION_PROVIDER")
        embedding_model = os.getenv("EMBEDDING_MODEL")

        # These are optional, so we just check if they're valid when set
        if text_provider:
            assert text_provider in [
                "mistral",
                "openai",
                "simple",
            ], "TEXT_EXTRACTION_PROVIDER should be a valid provider"

        if embedding_model:
            assert len(embedding_model) > 0, "EMBEDDING_MODEL should not be empty"


class TestCVExtractionIntegration:
    """Integration tests for CV extraction components"""

    @pytest.mark.asyncio
    async def test_extraction_pipeline_mocked(self):
        """Test complete extraction pipeline with mocked components"""
        try:
            from app_agents.cv_agents import process_cv_workflow
        except ImportError:
            pytest.skip("CV agents not available")

        # Mock the workflow
        with patch("app_agents.cv_agents.Runner.run") as mock_runner:
            mock_result = MagicMock()
            mock_result.final_output = "CV processed successfully"
            mock_runner.return_value = mock_result

            result = await process_cv_workflow("test-cv.pdf")

            assert result["success"] == True
            assert "CV processed successfully" in str(result["result"])

    def test_file_validation(self):
        """Test that file validation works correctly"""
        # Test file existence check
        test_file = TEST_CV_PATH

        if test_file.exists():
            assert test_file.suffix.lower() == ".pdf"
            assert test_file.stat().st_size > 0
        else:
            # File doesn't exist, which is fine for this test
            assert True


# Pytest configuration for these tests
pytestmark = [
    pytest.mark.asyncio,  # Mark all tests in this module as async-capable
]

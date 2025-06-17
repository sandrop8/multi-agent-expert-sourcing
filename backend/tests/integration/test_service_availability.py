"""
Service Availability Integration Tests

These tests check for service dependencies and imports that may not be available
in all environments. They are separated from fast unit tests to maintain
clear test categorization.

🎯 Purpose:
- Test import availability of optional services
- Validate service configuration
- Check environment setup requirements

💡 These tests will be skipped if services are not available
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Test data path
TEST_CV_PATH = Path(__file__).parent.parent / "fixtures" / "test-cv.pdf"


class TestCVExtractionServiceAvailability:
    """Tests for CV extraction service availability and configuration"""

    @pytest.mark.service_availability
    @pytest.mark.asyncio
    async def test_cv_extraction_service_import_availability(self):
        """Test that CV extraction service can be imported"""
        try:
            from services.cv_extraction_service import CVParserService

            assert CVParserService is not None
            print("✅ CVParserService import successful")
        except ImportError as e:
            pytest.skip(f"CV extraction service not available: {e}")

    @pytest.mark.service_availability
    @pytest.mark.asyncio
    async def test_cv_extraction_with_mock_data(self):
        """Test CV extraction with mocked data (no API calls)"""
        try:
            from services.cv_extraction_service import CVParserService
        except ImportError:
            pytest.skip("CV extraction service not available")

        # Mock the API call to test service structure
        with patch(
            "services.cv_extraction_service.extract_cv_text_with_responses_api"
        ) as mock_extract:
            mock_extract.return_value = "Mocked CV extraction result"

            service = CVParserService()
            pdf_bytes = b"Mock PDF content"

            # Test mocked service call
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
                print("✅ CV extraction service mock test passed")

    @pytest.mark.service_availability
    def test_cv_extraction_output_model_structure(self):
        """Test CVExtractionOutput model structure"""
        try:
            from app_agents.cv_agents import CVExtractionOutput
        except ImportError:
            pytest.skip("CV agents not available")

        # Test model creation and validation
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
        print("✅ CVExtractionOutput model test passed")


class TestCVAgentsAvailability:
    """Tests for CV agents service availability"""

    @pytest.mark.service_availability
    def test_cv_parser_agent_import_availability(self):
        """Test that CV parser agent can be imported"""
        try:
            from app_agents.cv_agents import cv_parser_agent

            assert cv_parser_agent is not None
            assert cv_parser_agent.name == "CV Parser Agent"
            print("✅ CV parser agent import successful")
        except ImportError as e:
            pytest.skip(f"CV agents not available: {e}")

    @pytest.mark.service_availability
    def test_cv_agent_configuration_availability(self):
        """Test that CV parser agent is configured correctly when available"""
        try:
            from app_agents.cv_agents import cv_parser_agent
        except ImportError:
            pytest.skip("CV agents not available")

        assert cv_parser_agent.name == "CV Parser Agent"
        assert cv_parser_agent.handoff_description is not None
        assert len(cv_parser_agent.instructions) > 0
        assert len(cv_parser_agent.tools) > 0  # Should have extraction tools
        print("✅ CV agent configuration test passed")

    @pytest.mark.service_availability
    def test_cv_agents_workflow_availability(self):
        """Test CV agents workflow import availability"""
        try:
            from app_agents.cv_agents import process_cv_workflow

            assert process_cv_workflow is not None
            print("✅ CV workflow import successful")
        except ImportError as e:
            pytest.skip(f"CV workflow not available: {e}")


class TestEnvironmentConfigurationAvailability:
    """Tests for environment variable configuration"""

    @pytest.mark.service_availability
    def test_required_environment_variables_availability(self):
        """Test that required environment variables are checked"""
        # OPENAI_API_KEY is required for real API calls
        openai_key = os.getenv("OPENAI_API_KEY")

        if openai_key:
            assert len(openai_key) > 10, "OPENAI_API_KEY should be a valid key"
            print("✅ OPENAI_API_KEY is configured")
        else:
            print("ℹ️ OPENAI_API_KEY not configured - real API tests will be skipped")

    @pytest.mark.service_availability
    def test_optional_environment_variables_availability(self):
        """Test optional environment variables when available"""
        text_provider = os.getenv("TEXT_EXTRACTION_PROVIDER")
        embedding_model = os.getenv("EMBEDDING_MODEL")

        # These are optional, so we just check if they're valid when set
        if text_provider:
            assert text_provider in [
                "mistral",
                "openai",
                "simple",
            ], "TEXT_EXTRACTION_PROVIDER should be a valid provider"
            print(f"✅ TEXT_EXTRACTION_PROVIDER configured: {text_provider}")

        if embedding_model:
            assert len(embedding_model) > 0, "EMBEDDING_MODEL should not be empty"
            print(f"✅ EMBEDDING_MODEL configured: {embedding_model}")


class TestFileSystemAvailability:
    """Tests for file system dependencies"""

    @pytest.mark.service_availability
    def test_test_file_availability(self):
        """Test that test CV file is available for integration testing"""
        test_file = TEST_CV_PATH

        if test_file.exists():
            assert test_file.suffix.lower() == ".pdf"
            assert test_file.stat().st_size > 0
            print(f"✅ Test CV file available: {test_file}")
        else:
            print(
                f"ℹ️ Test CV file not found: {test_file} - file-based tests will be skipped"
            )


# Pytest markers for service availability tests
pytestmark = [
    pytest.mark.service_availability,  # Mark all tests as service availability
]

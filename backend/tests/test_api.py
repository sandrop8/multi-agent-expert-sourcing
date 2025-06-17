"""
Comprehensive tests for the Multi-Agent Expert Sourcing API
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy import create_engine, text
import io

from main import app
from models.chat_models import messages
from models.cv_models import cvs


# Import test function from original main
def test_multi_agent_system():
    """Placeholder for test function - import from main_original.py if needed"""
    pass


# Test database setup
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture
def test_engine():
    """Create a test database engine"""
    test_engine = create_engine(
        TEST_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    # Create tables using metadata from models
    from models.base import get_metadata

    metadata = get_metadata()
    metadata.create_all(test_engine)
    return test_engine


@pytest.fixture
def clean_db(test_engine):
    """Ensure clean database state before each test"""
    with test_engine.connect() as conn:
        # Clean all tables before test
        conn.execute(text("DELETE FROM messages"))
        conn.execute(text("DELETE FROM cvs"))
        conn.commit()
    yield
    # Clean again after test
    with test_engine.connect() as conn:
        conn.execute(text("DELETE FROM messages"))
        conn.execute(text("DELETE FROM cvs"))
        conn.commit()


@pytest.fixture
async def client(test_engine):
    """Create test client for FastAPI app with overridden database"""
    from fastapi.testclient import TestClient

    # Override get_engine in service modules where it's actually imported
    with patch("services.chat_service.get_engine", return_value=test_engine):
        with patch("services.cv_service.get_engine", return_value=test_engine):
            with TestClient(app) as client:
                yield client


@pytest.fixture
def mock_runner():
    """Mock the agents Runner for testing"""
    with patch("services.chat_service.Runner") as mock:
        mock_result = MagicMock()
        mock_result.final_output = "Mocked AI response"
        mock.run = AsyncMock(return_value=mock_result)
        yield mock


@pytest.fixture
def mock_db_engine(test_engine):
    """Mock the database engine in services - now returns the test engine"""
    return test_engine


class TestChatEndpoint:
    """Test cases for the /conversations endpoint (RESTful)"""

    def test_successful_conversation_message_creation(
        self, client, mock_runner, mock_db_engine
    ):
        """Test successful conversation message creation with valid prompt"""
        response = client.post(
            "/conversations",
            json={"prompt": "I need a Python developer for my project"},
        )

        assert response.status_code == 201  # RESTful: 201 Created for resource creation
        data = response.json()
        assert "answer" in data
        assert data["answer"] == "Mocked AI response"

        # Verify agent was called
        mock_runner.run.assert_called_once()

    def test_empty_prompt_conversation(self, client, mock_runner, mock_db_engine):
        """Test handling of empty prompt in conversation"""
        response = client.post("/conversations", json={"prompt": ""})

        assert response.status_code == 201  # RESTful: Still creates a resource
        # Should still process empty prompts but return mocked response
        data = response.json()
        assert "answer" in data

    def test_missing_prompt_field_conversation(self, client):
        """Test conversation request without prompt field"""
        response = client.post("/conversations", json={})

        assert response.status_code == 422  # Validation error

    def test_invalid_json_conversation(self, client):
        """Test conversation request with invalid JSON"""
        response = client.post(
            "/conversations",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_conversation_agent_error_handling(self, client, mock_db_engine):
        """Test handling of agent system errors in conversation creation"""
        with patch(
            "services.chat_service.Runner.run", side_effect=Exception("Agent error")
        ):
            response = client.post("/conversations", json={"prompt": "test prompt"})

            assert response.status_code == 500

    @pytest.mark.asyncio
    async def test_conversation_guardrail_rejection(self, client, mock_db_engine):
        """Test handling of guardrail rejections in conversation"""
        with patch(
            "services.chat_service.Runner.run",
            side_effect=Exception("guardrail triggered"),
        ):
            response = client.post(
                "/conversations", json={"prompt": "What's the weather?"}
            )

            assert response.status_code == 201  # RESTful: Still creates resource
            data = response.json()
            assert "expert sourcing" in data["answer"].lower()

    def test_conversation_database_storage(
        self, client, mock_runner, mock_db_engine, clean_db
    ):
        """Test that conversations are stored in database"""
        prompt = "Find me a data scientist"

        response = client.post("/conversations", json={"prompt": prompt})
        assert response.status_code == 201  # RESTful: 201 Created

        # Check database storage
        with mock_db_engine.connect() as conn:
            result = conn.execute(messages.select())
            rows = result.fetchall()

            assert len(rows) == 2  # User message + AI response
            assert rows[0].role == "user"
            assert rows[0].content == prompt
            assert rows[1].role == "assistant"
            assert rows[1].content == "Mocked AI response"

    # Legacy endpoint tests for backward compatibility
    def test_legacy_chat_endpoint(self, client, mock_runner, mock_db_engine):
        """Test legacy /chat endpoint still works (backward compatibility)"""
        response = client.post(
            "/chat", json={"prompt": "I need a Python developer for my project"}
        )

        assert response.status_code == 200  # Legacy endpoints return 200, not 201
        data = response.json()
        assert "answer" in data
        assert data["answer"] == "Mocked AI response"


class TestCVUploadEndpoint:
    """Test cases for the /cvs endpoint (RESTful)"""

    def test_successful_cv_resource_creation_pdf(self, client, mock_db_engine):
        """Test successful CV resource creation with PDF file"""
        pdf_content = b"Mock PDF content for CV"

        # Mock the agent Runner to prevent hanging
        with patch("app_agents.cv_agents.Runner.run") as mock_runner_run:
            mock_result = MagicMock()
            mock_result.final_output = "CV processed successfully by agents"
            mock_runner_run.return_value = mock_result

            response = client.post(
                "/cvs",
                files={
                    "file": ("resume.pdf", io.BytesIO(pdf_content), "application/pdf")
                },
            )

            assert (
                response.status_code == 201
            )  # RESTful: 201 Created for resource creation
            data = response.json()
            assert "CV upload started" in data["message"]
            assert data["filename"] == "resume.pdf"
            assert data["size"] == len(pdf_content)
            assert data["processing_status"] == "processing_started"
            assert "session_id" in data

    def test_successful_cv_resource_creation_word_doc(self, client, mock_db_engine):
        """Test successful CV resource creation with Word document"""
        doc_content = b"Mock Word document content"

        # Mock the agent Runner to prevent hanging
        with patch("app_agents.cv_agents.Runner.run") as mock_runner_run:
            mock_result = MagicMock()
            mock_result.final_output = "CV processed successfully by agents"
            mock_runner_run.return_value = mock_result

            response = client.post(
                "/cvs",
                files={
                    "file": (
                        "resume.doc",
                        io.BytesIO(doc_content),
                        "application/msword",
                    )
                },
            )

            assert response.status_code == 201  # RESTful: 201 Created
            data = response.json()
            assert "CV upload started" in data["message"]
            assert data["filename"] == "resume.doc"

    def test_successful_cv_resource_creation_word_docx(self, client, mock_db_engine):
        """Test successful CV resource creation with Word DOCX document"""
        docx_content = b"Mock DOCX document content"

        # Mock the agent Runner to prevent hanging
        with patch("app_agents.cv_agents.Runner.run") as mock_runner_run:
            mock_result = MagicMock()
            mock_result.final_output = "CV processed successfully by agents"
            mock_runner_run.return_value = mock_result

            response = client.post(
                "/cvs",
                files={
                    "file": (
                        "resume.docx",
                        io.BytesIO(docx_content),
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
                },
            )

            assert response.status_code == 201  # RESTful: 201 Created
            data = response.json()
            assert "CV upload started" in data["message"]
            assert data["filename"] == "resume.docx"

    def test_cv_creation_invalid_file_type_text(self, client):
        """Test CV creation rejection with text file"""
        text_content = b"This is just a text file"

        response = client.post(
            "/cvs",
            files={"file": ("resume.txt", io.BytesIO(text_content), "text/plain")},
        )

        assert response.status_code == 400
        assert "Only PDF and Word documents are allowed" in response.json()["detail"]

    def test_cv_creation_invalid_file_type_image(self, client):
        """Test CV creation rejection with image file"""
        image_content = b"Fake image content"

        response = client.post(
            "/cvs",
            files={"file": ("photo.jpg", io.BytesIO(image_content), "image/jpeg")},
        )

        assert response.status_code == 400
        assert "Only PDF and Word documents are allowed" in response.json()["detail"]

    def test_cv_creation_file_too_large(self, client):
        """Test CV creation rejection when file exceeds size limit"""
        # Create a file larger than 10MB
        large_content = b"x" * (11 * 1024 * 1024)  # 11MB

        response = client.post(
            "/cvs",
            files={
                "file": (
                    "large-resume.pdf",
                    io.BytesIO(large_content),
                    "application/pdf",
                )
            },
        )

        assert response.status_code == 400
        assert "File size exceeds 10MB limit" in response.json()["detail"]

    def test_cv_creation_missing_file(self, client):
        """Test CV creation with missing file parameter"""
        response = client.post("/cvs")

        assert response.status_code == 422  # Validation error

    # NOTE: Real OpenAI API test moved to tests/integration/test_openai_integration.py

    @pytest.mark.asyncio
    async def test_cv_creation_database_error_handling(self, client, test_engine):
        """Test handling of database errors during CV creation"""
        # Mock the begin method on the test engine to raise an exception
        with patch.object(
            test_engine, "begin", side_effect=Exception("Database connection failed")
        ):
            pdf_content = b"Test CV content"

            response = client.post(
                "/cvs",
                files={
                    "file": ("test.pdf", io.BytesIO(pdf_content), "application/pdf")
                },
            )

            assert response.status_code == 500
            assert "Upload failed" in response.json()["detail"]

    # Legacy endpoint tests for backward compatibility
    def test_legacy_upload_cv_endpoint(self, client, mock_db_engine):
        """Test legacy /upload-cv endpoint still works (backward compatibility)"""
        pdf_content = b"Mock PDF content for CV"

        with patch("app_agents.cv_agents.Runner.run") as mock_runner_run:
            mock_result = MagicMock()
            mock_result.final_output = "CV processed successfully by agents"
            mock_runner_run.return_value = mock_result

            response = client.post(
                "/upload-cv",
                files={
                    "file": ("resume.pdf", io.BytesIO(pdf_content), "application/pdf")
                },
            )

            assert response.status_code == 200  # Legacy endpoints return 200, not 201


class TestCVsListEndpoint:
    """Test cases for the /cvs collection endpoint (RESTful)"""

    def test_empty_cvs_collection(self, client, mock_db_engine, clean_db):
        """Test CVs collection endpoint with no CV resources"""
        response = client.get("/cvs")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_cvs_collection_with_resources(self, client, mock_db_engine, clean_db):
        """Test CVs collection endpoint with existing CV resources"""
        # Add test CVs to database
        with mock_db_engine.begin() as conn:
            conn.execute(
                cvs.insert(),
                [
                    {
                        "filename": "cv1.pdf",
                        "original_filename": "cv1.pdf",
                        "file_size": 1024,
                        "content_type": "application/pdf",
                        "file_data": b"CV 1 content",
                        "uploaded_at": datetime.utcnow(),
                        "processed": False,
                    },
                    {
                        "filename": "cv2.docx",
                        "original_filename": "cv2.docx",
                        "file_size": 2048,
                        "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "file_data": b"CV 2 content",
                        "uploaded_at": datetime.utcnow(),
                        "processed": True,
                    },
                ],
            )

        response = client.get("/cvs")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 2

        # CVs are returned in reverse chronological order (newest first)
        # cv2.docx was inserted after cv1.pdf, so it should come first
        cv1 = data[0]
        assert cv1["filename"] == "cv2.docx"
        assert cv1["file_size"] == 2048
        assert (
            cv1["content_type"]
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        assert cv1["processed"]

        # Check second CV (cv1.pdf)
        cv2 = data[1]
        assert cv2["filename"] == "cv1.pdf"
        assert cv2["file_size"] == 1024
        assert cv2["content_type"] == "application/pdf"
        assert not cv2["processed"]

    def test_cvs_collection_order(self, client, mock_db_engine, clean_db):
        """Test that CVs collection returns resources in reverse chronological order (newest first)"""
        # Add CVs with different timestamps
        with mock_db_engine.begin() as conn:
            conn.execute(
                cvs.insert(),
                [
                    {
                        "filename": "old-cv.pdf",
                        "original_filename": "old-cv.pdf",
                        "file_size": 1024,
                        "content_type": "application/pdf",
                        "file_data": b"Old CV",
                        "uploaded_at": datetime(2023, 1, 1),
                        "processed": False,
                    },
                    {
                        "filename": "new-cv.pdf",
                        "original_filename": "new-cv.pdf",
                        "file_size": 1024,
                        "content_type": "application/pdf",
                        "file_data": b"New CV",
                        "uploaded_at": datetime(2023, 12, 31),
                        "processed": False,
                    },
                ],
            )

        response = client.get("/cvs")
        data = response.json()

        # Should be in reverse chronological order (newest first)
        assert data[0]["filename"] == "new-cv.pdf"
        assert data[1]["filename"] == "old-cv.pdf"

    @pytest.mark.asyncio
    async def test_cvs_collection_database_error_handling(self, client, test_engine):
        """Test handling of database errors in CVs collection endpoint"""
        # Mock the connect method on the test engine to raise an exception
        with patch.object(
            test_engine, "connect", side_effect=Exception("Database connection failed")
        ):
            response = client.get("/cvs")

            assert response.status_code == 500

    # Legacy endpoint tests for backward compatibility
    def test_legacy_cvs_list_endpoint(self, client, mock_db_engine, clean_db):
        """Test legacy /cvs endpoint still works (backward compatibility)"""
        response = client.get("/cvs")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestCVProcessingSessionsEndpoint:
    """Test cases for the /cv-processing-sessions endpoint (RESTful)"""

    def test_get_processing_session_success(self, client):
        """Test retrieving CV processing session by ID"""
        session_id = "test-session-123"

        # Patch at the module level where the function is called
        with patch("api.v1.cv.get_status_for_frontend") as mock_status:
            mock_status.return_value = {
                "session_id": session_id,
                "status": "completed",
                "progress": 100,
            }

            response = client.get(f"/cv-processing-sessions/{session_id}")

            assert response.status_code == 200
            data = response.json()
            assert data["session_id"] == session_id
            assert data["status"] == "completed"
            assert data["progress"] == 100

    def test_get_processing_session_error(self, client):
        """Test error handling when retrieving processing session"""
        session_id = "invalid-session"

        # Patch at the module level where the function is called
        with patch("api.v1.cv.get_status_for_frontend") as mock_status:
            mock_status.side_effect = Exception("Session not found")

            response = client.get(f"/cv-processing-sessions/{session_id}")

            assert response.status_code == 500
            assert "Error retrieving processing session" in response.json()["detail"]

    # Legacy endpoint tests for backward compatibility
    def test_legacy_cv_status_endpoint(self, client):
        """Test legacy /cv-status/{session_id} endpoint still works (backward compatibility)"""
        session_id = "test-session-123"

        # Patch at the module level where the function is called
        with patch("api.v1.cv.get_status_for_frontend") as mock_status:
            mock_status.return_value = {
                "session_id": session_id,
                "status": "processing",
            }

            response = client.get(f"/cv-status/{session_id}")

            assert response.status_code == 200
            data = response.json()
            assert data["session_id"] == session_id


class TestHistoryEndpoint:
    """Test cases for the /conversations collection endpoint (RESTful)"""

    def test_empty_conversation_history(self, client, mock_db_engine, clean_db):
        """Test conversation history endpoint with no messages"""
        response = client.get("/conversations")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_conversation_history_with_messages(self, client, mock_db_engine, clean_db):
        """Test conversation history endpoint with existing messages"""
        # Add test messages
        with mock_db_engine.begin() as conn:
            conn.execute(
                messages.insert(),
                [
                    {"role": "user", "content": "Hello", "ts": datetime.utcnow()},
                    {
                        "role": "assistant",
                        "content": "Hi there",
                        "ts": datetime.utcnow(),
                    },
                ],
            )

        response = client.get("/conversations")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 2
        assert data[0]["role"] == "user"
        assert data[0]["content"] == "Hello"
        assert data[1]["role"] == "assistant"
        assert data[1]["content"] == "Hi there"

    def test_conversation_history_limit_parameter(self, client, mock_db_engine):
        """Test conversation history endpoint with limit parameter"""
        # Add multiple test messages
        with mock_db_engine.begin() as conn:
            test_messages = [
                {"role": "user", "content": f"Message {i}", "ts": datetime.utcnow()}
                for i in range(10)
            ]
            conn.execute(messages.insert(), test_messages)

        response = client.get("/conversations?limit=5")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 5

    def test_conversation_history_order(self, client, mock_db_engine, clean_db):
        """Test that conversation history returns messages in chronological order"""
        # Add messages with different timestamps
        with mock_db_engine.begin() as conn:
            conn.execute(
                messages.insert(),
                [
                    {"role": "user", "content": "First", "ts": datetime(2023, 1, 1)},
                    {
                        "role": "assistant",
                        "content": "Second",
                        "ts": datetime(2023, 1, 2),
                    },
                    {"role": "user", "content": "Third", "ts": datetime(2023, 1, 3)},
                ],
            )

        response = client.get("/conversations")
        data = response.json()

        # Should be in chronological order (oldest first)
        assert data[0]["content"] == "First"
        assert data[1]["content"] == "Second"
        assert data[2]["content"] == "Third"

    # Legacy endpoint tests for backward compatibility
    def test_legacy_history_endpoint(self, client, mock_db_engine, clean_db):
        """Test legacy /history endpoint still works (backward compatibility)"""
        response = client.get("/history")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestCompanyEndpoint:
    """Test cases for the /companies endpoint (RESTful)"""

    def test_successful_company_resource_creation(self, client):
        """Test successful company resource creation"""
        company_data = {
            "website_url": "https://example.com",
            "linkedin_url": "https://linkedin.com/company/example",
        }

        # Mock the company service
        with patch(
            "services.company_service.CompanyService.start_company_profiling_crew"
        ) as mock_service:
            mock_service.return_value = {
                "message": "Company profiling started",
                "website_url": "https://example.com",
                "status": "processing",
            }

            response = client.post("/companies", json=company_data)

            assert (
                response.status_code == 201
            )  # RESTful: 201 Created for resource creation
            data = response.json()
            assert "Company profiling started" in data["message"]
            assert data["website_url"] == "https://example.com"

    def test_company_creation_invalid_data(self, client):
        """Test company creation with invalid data"""
        invalid_data = {}  # Missing required website_url

        response = client.post("/companies", json=invalid_data)

        assert response.status_code == 422  # Validation error

    def test_company_creation_service_error(self, client):
        """Test handling of service errors during company creation"""
        company_data = {"website_url": "https://example.com"}

        # Mock the company service to raise an exception
        with patch(
            "services.company_service.CompanyService.start_company_profiling_crew"
        ) as mock_service:
            mock_service.side_effect = Exception("CrewAI service error")

            response = client.post("/companies", json=company_data)

            # The endpoint should handle the exception and return a proper HTTP error
            assert response.status_code == 500

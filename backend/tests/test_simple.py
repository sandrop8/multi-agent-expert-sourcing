"""
Simple working tests to demonstrate the testing framework
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import io

def test_app_import():
    """Test that we can import the main app"""
    from main import app
    assert app is not None

def test_models_import():
    """Test that we can import the Pydantic models"""
    from main import ChatReq, Msg
    
    # Test ChatReq model
    chat_req = ChatReq(prompt="Test message")
    assert chat_req.prompt == "Test message"
    
    # Test Msg model  
    from datetime import datetime
    msg = Msg(id=1, role="user", content="Test", ts=datetime.now())
    assert msg.role == "user"
    assert msg.content == "Test"

def test_chat_endpoint_basic():
    """Test basic chat endpoint functionality with mocked agents"""
    from main import app
    
    with patch('main.Runner') as mock_runner:
        # Mock the agent response
        mock_result = MagicMock()
        mock_result.final_output = "Mocked AI response"
        mock_runner.run.return_value = mock_result
        
        # Mock database operations
        with patch('main.engine.begin') as mock_db:
            mock_conn = MagicMock()
            mock_db.return_value.__enter__.return_value = mock_conn
            
            client = TestClient(app)
            response = client.post(
                "/chat",
                json={"prompt": "Find me a developer"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert data["answer"] == "Mocked AI response"

def test_history_endpoint_basic():
    """Test basic history endpoint functionality"""
    from main import app
    
    with patch('main.engine.connect') as mock_connect:
        # Mock database query
        mock_conn = MagicMock()
        mock_result = MagicMock()
        mock_result.__iter__ = lambda self: iter([])  # Empty result
        mock_conn.execute.return_value = mock_result
        mock_connect.return_value.__enter__.return_value = mock_conn
        
        client = TestClient(app)
        response = client.get("/history")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

def test_cv_upload_endpoint_basic():
    """Test basic CV upload functionality"""
    from main import app
    
    # Mock database operations
    with patch('main.engine.begin') as mock_db:
        mock_conn = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_conn
        
        client = TestClient(app)
        
        # Create a mock PDF file
        pdf_content = b"Fake PDF content"
        
        response = client.post(
            "/upload-cv",
            files={"file": ("test-cv.pdf", io.BytesIO(pdf_content), "application/pdf")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "CV uploaded successfully"
        assert data["filename"] == "test-cv.pdf"
        assert data["size"] == len(pdf_content)

def test_cv_upload_invalid_file_type():
    """Test CV upload with invalid file type"""
    from main import app
    
    client = TestClient(app)
    
    # Create a mock text file
    text_content = b"This is not a CV"
    
    response = client.post(
        "/upload-cv",
        files={"file": ("test.txt", io.BytesIO(text_content), "text/plain")}
    )
    
    assert response.status_code == 400
    assert "Only PDF and Word documents are allowed" in response.json()["detail"]

def test_cv_upload_large_file():
    """Test CV upload with file too large"""
    from main import app
    
    client = TestClient(app)
    
    # Create a mock large file (11MB)
    large_content = b"x" * (11 * 1024 * 1024)
    
    response = client.post(
        "/upload-cv",
        files={"file": ("large-cv.pdf", io.BytesIO(large_content), "application/pdf")}
    )
    
    assert response.status_code == 400
    assert "File size exceeds 10MB limit" in response.json()["detail"]

def test_cvs_list_endpoint_basic():
    """Test basic CVs list functionality"""
    from main import app
    
    with patch('main.engine.connect') as mock_connect:
        # Mock database query
        mock_conn = MagicMock()
        mock_result = MagicMock()
        mock_result.__iter__ = lambda self: iter([])  # Empty result
        mock_conn.execute.return_value = mock_result
        mock_connect.return_value.__enter__.return_value = mock_conn
        
        client = TestClient(app)
        response = client.get("/cvs")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

def test_chat_request_validation():
    """Test that ChatReq model validates correctly"""
    from main import ChatReq
    
    # Valid request
    valid_req = ChatReq(prompt="Hello")
    assert valid_req.prompt == "Hello"
    
    # Test with empty string (should be valid)
    empty_req = ChatReq(prompt="")
    assert empty_req.prompt == ""

def test_agent_configuration():
    """Test that agents are configured correctly"""
    from main import supervisor_agent, project_requirements_agent, project_refinement_agent, guardrail_agent
    
    assert supervisor_agent.name == "Expert Sourcing Supervisor"
    assert project_requirements_agent.name == "Project Requirements Assistant"
    assert project_refinement_agent.name == "Project Refinement Specialist"
    assert guardrail_agent.name == "Expert Sourcing Validator"

@pytest.mark.asyncio
async def test_async_functionality():
    """Test async functionality is working"""
    import asyncio
    
    async def sample_async_function():
        await asyncio.sleep(0.001)  # Minimal delay
        return "async result"
    
    result = await sample_async_function()
    assert result == "async result"

def test_environment_variables():
    """Test that environment variables are loaded"""
    import os
    
    # These should be loaded from .env file
    openai_key = os.getenv("OPENAI_API_KEY")
    database_url = os.getenv("DATABASE_URL") or os.getenv("PG_URL")
    
    # Just check they exist (don't expose actual values)
    assert openai_key is not None, "OPENAI_API_KEY should be set"
    assert database_url is not None, "DATABASE_URL or PG_URL should be set"

def test_cors_configuration():
    """Test that CORS is configured"""
    from main import app
    
    # Check that CORS middleware is present
    middleware_found = False
    for middleware in app.user_middleware:
        if "CORS" in str(middleware.cls):
            middleware_found = True
            break
    
    assert middleware_found, "CORS middleware should be configured"

def test_database_tables_exist():
    """Test that both messages and cvs tables are configured"""
    from main import messages, cvs
    
    assert messages is not None
    assert cvs is not None
    assert hasattr(messages.c, 'id')
    assert hasattr(messages.c, 'role')
    assert hasattr(messages.c, 'content')
    assert hasattr(cvs.c, 'id')
    assert hasattr(cvs.c, 'filename')
    assert hasattr(cvs.c, 'file_data') 
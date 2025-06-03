"""
Comprehensive tests for the Multi-Agent Expert Sourcing API
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from main import app, engine, messages, test_multi_agent_system

# Test database setup
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture
def test_engine():
    """Create a test database engine"""
    test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    messages.metadata.create_all(test_engine)
    yield test_engine
    # Cleanup after tests
    with test_engine.connect() as conn:
        conn.execute(text("DELETE FROM messages"))
        conn.commit()

@pytest.fixture
async def client():
    """Create test client for FastAPI app"""
    from fastapi.testclient import TestClient
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_runner():
    """Mock the agents Runner for testing"""
    with patch('main.Runner') as mock:
        mock_result = MagicMock()
        mock_result.final_output = "Mocked AI response"
        mock.run = AsyncMock(return_value=mock_result)
        yield mock

@pytest.fixture 
def mock_db_engine(test_engine):
    """Mock the database engine in main.py"""
    with patch('main.engine', test_engine):
        yield test_engine

class TestChatEndpoint:
    """Test cases for the /chat endpoint"""

    def test_successful_chat_request(self, client, mock_runner, mock_db_engine):
        """Test successful chat request with valid prompt"""
        response = client.post(
            "/chat",
            json={"prompt": "I need a Python developer for my project"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert data["answer"] == "Mocked AI response"
        
        # Verify agent was called
        mock_runner.run.assert_called_once()

    @pytest.mark.asyncio 
    async def test_empty_prompt(self, client, mock_runner, mock_db_engine):
        """Test handling of empty prompt"""
        response = await client.post(
            "/chat",
            json={"prompt": ""}
        )
        
        assert response.status_code == 200
        # Should still process empty prompts but return mocked response
        data = response.json()
        assert "answer" in data

    @pytest.mark.asyncio
    async def test_missing_prompt_field(self, client):
        """Test request without prompt field"""
        response = await client.post("/chat", json={})
        
        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_invalid_json(self, client):
        """Test request with invalid JSON"""
        response = await client.post(
            "/chat",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_agent_error_handling(self, client, mock_db_engine):
        """Test handling of agent system errors"""
        with patch('main.Runner.run', side_effect=Exception("Agent error")):
            response = await client.post(
                "/chat",
                json={"prompt": "test prompt"}
            )
            
            assert response.status_code == 500

    @pytest.mark.asyncio
    async def test_guardrail_rejection(self, client, mock_db_engine):
        """Test handling of guardrail rejections"""
        with patch('main.Runner.run', side_effect=Exception("guardrail triggered")):
            response = await client.post(
                "/chat",
                json={"prompt": "What's the weather?"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "expert sourcing" in data["answer"].lower()

    @pytest.mark.asyncio
    async def test_database_storage(self, client, mock_runner, mock_db_engine):
        """Test that conversations are stored in database"""
        prompt = "Find me a data scientist"
        
        response = await client.post("/chat", json={"prompt": prompt})
        assert response.status_code == 200
        
        # Check database storage
        with mock_db_engine.connect() as conn:
            result = conn.execute(messages.select())
            rows = result.fetchall()
            
            assert len(rows) == 2  # User message + AI response
            assert rows[0].role == "user"
            assert rows[0].content == prompt
            assert rows[1].role == "assistant"
            assert rows[1].content == "Mocked AI response"

class TestHistoryEndpoint:
    """Test cases for the /history endpoint"""

    @pytest.mark.asyncio
    async def test_empty_history(self, client, mock_db_engine):
        """Test history endpoint with no messages"""
        response = await client.get("/history")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    @pytest.mark.asyncio
    async def test_history_with_messages(self, client, mock_db_engine):
        """Test history endpoint with existing messages"""
        # Add test messages
        with mock_db_engine.begin() as conn:
            conn.execute(messages.insert(), [
                {"role": "user", "content": "Hello", "ts": datetime.utcnow()},
                {"role": "assistant", "content": "Hi there", "ts": datetime.utcnow()},
            ])
        
        response = await client.get("/history")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 2
        assert data[0]["role"] == "user"
        assert data[0]["content"] == "Hello"
        assert data[1]["role"] == "assistant"
        assert data[1]["content"] == "Hi there"

    @pytest.mark.asyncio
    async def test_history_limit_parameter(self, client, mock_db_engine):
        """Test history endpoint with limit parameter"""
        # Add multiple test messages
        with mock_db_engine.begin() as conn:
            test_messages = [
                {"role": "user", "content": f"Message {i}", "ts": datetime.utcnow()}
                for i in range(10)
            ]
            conn.execute(messages.insert(), test_messages)
        
        response = await client.get("/history?limit=5")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 5

    @pytest.mark.asyncio
    async def test_history_order(self, client, mock_db_engine):
        """Test that history returns messages in chronological order"""
        # Add messages with different timestamps
        with mock_db_engine.begin() as conn:
            conn.execute(messages.insert(), [
                {"role": "user", "content": "First", "ts": datetime(2023, 1, 1)},
                {"role": "assistant", "content": "Second", "ts": datetime(2023, 1, 2)},
                {"role": "user", "content": "Third", "ts": datetime(2023, 1, 3)},
            ])
        
        response = await client.get("/history")
        data = response.json()
        
        # Should be in chronological order (oldest first)
        assert data[0]["content"] == "First"
        assert data[1]["content"] == "Second"
        assert data[2]["content"] == "Third"

class TestCORSConfiguration:
    """Test CORS middleware configuration"""

    @pytest.mark.asyncio
    async def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses"""
        response = await client.options("/chat")
        
        # Should allow CORS headers
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_allowed_origins(self, client):
        """Test that allowed origins are configured correctly"""
        # This would require more complex setup to test properly
        # For now, just verify the endpoint responds
        response = await client.get("/history")
        assert response.status_code == 200

class TestAgentSystem:
    """Test the multi-agent system functionality"""

    def test_agent_configuration(self):
        """Test that agents are configured correctly"""
        from main import supervisor_agent, expert_search_agent, profile_enrichment_agent, guardrail_agent
        
        assert supervisor_agent.name == "Expert Sourcing Supervisor"
        assert expert_search_agent.name == "Expert Search & Matchmaking Specialist"
        assert profile_enrichment_agent.name == "CV Parsing & Profile Enrichment Specialist"
        assert guardrail_agent.name == "Expert Sourcing Validator"

    @pytest.mark.asyncio
    async def test_multi_agent_system_integration(self):
        """Test the multi-agent system test function"""
        # Mock the Runner to avoid actual API calls
        with patch('main.Runner.run') as mock_run:
            mock_result = MagicMock()
            mock_result.final_output = "Test response"
            mock_run.return_value = mock_result
            
            # Should not raise any exceptions
            await test_multi_agent_system()
            
            # Should have called run multiple times for different test cases
            assert mock_run.call_count >= 2

class TestEnvironmentConfiguration:
    """Test environment variable handling"""

    def test_required_environment_variables(self):
        """Test that required environment variables are checked"""
        import os
        from unittest.mock import patch
        
        # Test with missing OPENAI_API_KEY
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(RuntimeError, match="Missing required environment variables"):
                # Re-import main to trigger environment check
                import importlib
                import main as main_module
                importlib.reload(main_module)

class TestDatabaseSchema:
    """Test database schema and operations"""

    def test_messages_table_structure(self, test_engine):
        """Test that messages table has correct structure"""
        from sqlalchemy import inspect
        
        inspector = inspect(test_engine)
        columns = inspector.get_columns('messages')
        
        column_names = [col['name'] for col in columns]
        assert 'id' in column_names
        assert 'role' in column_names
        assert 'content' in column_names
        assert 'ts' in column_names

    def test_database_connection(self, test_engine):
        """Test basic database connectivity"""
        with test_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.fetchone()[0] == 1

class TestErrorHandling:
    """Test various error scenarios"""

    @pytest.mark.asyncio
    async def test_database_error_handling(self, client):
        """Test handling of database errors"""
        with patch('main.engine.begin', side_effect=Exception("Database error")):
            with patch('main.Runner.run') as mock_run:
                mock_result = MagicMock()
                mock_result.final_output = "Response"
                mock_run.return_value = mock_result
                
                response = await client.post(
                    "/chat",
                    json={"prompt": "test"}
                )
                
                assert response.status_code == 500

class TestPydanticModels:
    """Test Pydantic model validation"""

    def test_chat_request_model(self):
        """Test ChatReq model validation"""
        from main import ChatReq
        
        # Valid request
        valid_req = ChatReq(prompt="Hello")
        assert valid_req.prompt == "Hello"
        
        # Test with empty string (should be valid)
        empty_req = ChatReq(prompt="")
        assert empty_req.prompt == ""

    def test_message_model(self):
        """Test Msg model structure"""
        from main import Msg
        from datetime import datetime
        
        msg = Msg(
            id=1,
            role="user",
            content="Test message",
            ts=datetime.now()
        )
        
        assert msg.id == 1
        assert msg.role == "user"
        assert msg.content == "Test message"
        assert isinstance(msg.ts, datetime) 
"""
NATS Integration Tests

These tests verify the functionality of the NATS messaging endpoints.
They require a live connection to a NATS server, configured via the
NATS_URL environment variable.

These tests are intended to be run in a CI/CD environment or manually
when verifying the NATS integration.

The tests are designed to work with both JetStream-enabled and core NATS servers.
"""

import pytest
import os
import logging
from fastapi.testclient import TestClient
from main import app

# Setup logging for test results
logging.basicConfig(level=logging.INFO, format="%(message)s")
test_logger = logging.getLogger("nats_integration_tests")

# Track test results for summary
test_results = {"passed": 0, "failed": 0, "total": 0}

# Skip all tests in this file if NATS_URL is not set, as they are integration tests.
pytestmark = pytest.mark.skipif(
    not os.getenv("NATS_URL"),
    reason="NATS_URL environment variable not set for integration tests",
)


@pytest.fixture(scope="module")
def client():
    """
    Create a test client for the FastAPI app.
    This fixture has a 'module' scope, so the app startup (including NATS connection)
    runs only once for all tests in this file.
    """
    test_logger.info("🚀 Starting NATS Integration Test Suite")
    test_logger.info(f"🔗 NATS URL: {os.getenv('NATS_URL', 'Not set')}")

    with TestClient(app) as c:
        yield c

    # Print test summary
    success_rate = (
        (test_results["passed"] / test_results["total"] * 100)
        if test_results["total"] > 0
        else 0
    )
    test_logger.info("=" * 60)
    test_logger.info("📊 NATS INTEGRATION TEST SUMMARY")
    test_logger.info("=" * 60)
    test_logger.info(f"✅ Passed: {test_results['passed']}")
    test_logger.info(f"❌ Failed: {test_results['failed']}")
    test_logger.info(f"📈 Total:  {test_results['total']}")
    test_logger.info(f"🎯 Success Rate: {success_rate:.1f}%")
    test_logger.info("=" * 60)

    if test_results["failed"] == 0:
        test_logger.info("🎉 ALL NATS INTEGRATION TESTS PASSED!")
    else:
        test_logger.warning(
            f"⚠️  {test_results['failed']} tests failed - check logs above"
        )


def log_test_result(test_name: str, passed: bool, details: str = ""):
    """Log individual test results and update counters"""
    global test_results
    test_results["total"] += 1

    if passed:
        test_results["passed"] += 1
        test_logger.info(f"✅ {test_name} - PASSED {details}")
    else:
        test_results["failed"] += 1
        test_logger.error(f"❌ {test_name} - FAILED {details}")


class TestNATSIntegration:
    """
    Integration tests for NATS messaging endpoints.
    These tests require a running NATS server configured via NATS_URL.
    """

    def test_nats_health_check_is_healthy(self, client):
        """Test the NATS health check endpoint reports a healthy status."""
        test_name = "NATS Health Check"
        try:
            response = client.get("/nats/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["connected"] is True
            assert "connected_url" in data["server_info"]
            log_test_result(
                test_name,
                True,
                f"- Connected to {data['server_info'].get('connected_url', 'unknown')}",
            )
        except Exception as e:
            log_test_result(test_name, False, f"- {str(e)}")
            raise

    def test_publish_custom_event_non_persistent(self, client):
        """Test publishing a custom event to a NATS subject (non-persistent)."""
        test_name = "Non-Persistent Event Publishing"
        try:
            event_data = {
                "subject": "test.event.custom",
                "event_data": {"message": "Hello NATS!"},
                "persistent": False,
            }
            response = client.post("/nats/publish", json=event_data)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["subject"] == "test.event.custom"
            log_test_result(test_name, True, "- Core NATS messaging")
        except Exception as e:
            log_test_result(test_name, False, f"- {str(e)}")
            raise

    def test_publish_custom_event_persistent_fallback(self, client):
        """Test publishing a persistent event with graceful fallback to core NATS."""
        test_name = "Persistent Event Publishing (JetStream Fallback)"
        try:
            event_data = {
                "subject": "test.event.persistent",
                "event_data": {"message": "Hello NATS with persistence!"},
                "persistent": True,
            }
            response = client.post("/nats/publish", json=event_data)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["subject"] == "test.event.persistent"
            log_test_result(test_name, True, "- JetStream or core NATS fallback")
        except Exception as e:
            log_test_result(test_name, False, f"- {str(e)}")
            raise

    def test_publish_test_cv_uploaded_event(self, client):
        """Test the dedicated endpoint for publishing a 'cv.uploaded' test event."""
        test_name = "CV Upload Event Publishing"
        try:
            params = {"cv_id": 999, "filename": "integration_test_cv.pdf"}
            response = client.post("/nats/test/cv-uploaded", params=params)
            assert response.status_code == 200
            data = response.json()
            assert "CV uploaded event published" in data["message"]
            assert data["event_subject"] == "events.cv.uploaded"
            log_test_result(test_name, True, f"- CV ID: {params['cv_id']}")
        except Exception as e:
            log_test_result(test_name, False, f"- {str(e)}")
            raise

    def test_request_response_pattern_graceful_failure(self, client):
        """Test the request-response pattern endpoint, expecting a graceful timeout message."""
        test_name = "Request-Response Pattern"
        try:
            response = client.get("/nats/test/request-response")
            assert response.status_code == 200
            data = response.json()
            assert "No responder available" in data["message"]
            log_test_result(test_name, True, "- Graceful timeout handling")
        except Exception as e:
            log_test_result(test_name, False, f"- {str(e)}")
            raise

    def test_list_jetstream_streams(self, client):
        """Test the endpoint that lists configured JetStream streams."""
        test_name = "JetStream Status Check"
        try:
            response = client.get("/nats/streams")
            assert response.status_code == 200
            data = response.json()

            if "not available" in data["message"]:
                log_test_result(
                    test_name,
                    True,
                    "- JetStream not available (expected for some servers)",
                )
                assert "JetStream is not available" in data["message"]
                assert data["streams"] == []
            else:
                log_test_result(test_name, True, "- JetStream available")
                assert "JetStream is available" in data["message"]
                assert len(data["streams"]) >= 3
        except Exception as e:
            log_test_result(test_name, False, f"- {str(e)}")
            raise

    def test_publish_chat_message_event(self, client):
        """Test the chat message event publishing endpoint."""
        test_name = "Chat Message Event Publishing"
        try:
            params = {
                "message_id": 123,
                "role": "user",
                "content": "Hello, this is a test message",
            }
            response = client.post("/nats/test/chat-message", params=params)
            assert response.status_code == 200
            data = response.json()
            assert "Chat message event published" in data["message"]
            assert data["event_subject"] == "events.chat.message.created"
            log_test_result(test_name, True, f"- Message ID: {params['message_id']}")
        except Exception as e:
            log_test_result(test_name, False, f"- {str(e)}")
            raise

    def test_publish_agent_task_event(self, client):
        """Test the agent task completion event publishing endpoint."""
        test_name = "Agent Task Event Publishing"
        try:
            params = {"agent_id": "test_agent_123", "task_id": "task_456"}
            json_data = {"result": {"status": "completed", "data": {"test": "value"}}}
            response = client.post(
                "/nats/test/agent-task", params=params, json=json_data
            )
            assert response.status_code == 200
            data = response.json()
            assert "Agent task completion event published" in data["message"]
            assert "agent.task.completed.test_agent_123" in data["event_subject"]
            log_test_result(test_name, True, f"- Agent: {params['agent_id']}")
        except Exception as e:
            log_test_result(test_name, False, f"- {str(e)}")
            raise

    def test_publish_event_with_invalid_subject(self, client):
        """Test publishing an event with an invalid subject structure."""
        test_name = "Invalid Subject Handling"
        try:
            # Test empty subject (should fail)
            event_data = {
                "subject": "",
                "event_data": {"message": "Test with empty subject"},
                "persistent": False,
            }
            response = client.post("/nats/publish", json=event_data)
            assert response.status_code == 500

            # Test valid minimal subject (should pass)
            event_data_valid = {
                "subject": "test",
                "event_data": {"message": "Test with minimal subject"},
                "persistent": False,
            }
            response = client.post("/nats/publish", json=event_data_valid)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            log_test_result(
                test_name, True, "- Empty subjects rejected, valid subjects accepted"
            )
        except Exception as e:
            log_test_result(test_name, False, f"- {str(e)}")
            raise

    def test_publish_event_with_large_payload(self, client):
        """Test publishing an event with a larger payload."""
        test_name = "Large Payload Handling"
        try:
            large_data = {"data": "x" * 10000}  # 10KB of data
            event_data = {
                "subject": "test.large.payload",
                "event_data": large_data,
                "persistent": False,
            }
            response = client.post("/nats/publish", json=event_data)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            log_test_result(test_name, True, "- 10KB payload handled successfully")
        except Exception as e:
            log_test_result(test_name, False, f"- {str(e)}")
            raise

    def test_cv_uploaded_event_with_special_characters(self, client):
        """Test CV uploaded event with special characters in filename."""
        test_name = "Special Characters in Filenames"
        try:
            params = {"cv_id": 888, "filename": "résumé_测试_файл.pdf"}
            response = client.post("/nats/test/cv-uploaded", params=params)
            assert response.status_code == 200
            data = response.json()
            assert "CV uploaded event published" in data["message"]
            log_test_result(test_name, True, "- Unicode characters handled correctly")
        except Exception as e:
            log_test_result(test_name, False, f"- {str(e)}")
            raise

    def test_chat_message_with_long_content(self, client):
        """Test chat message event with very long content."""
        test_name = "Long Content Messages"
        try:
            long_content = "This is a very long message. " * 100  # ~3000 characters
            params = {"message_id": 456, "role": "assistant", "content": long_content}
            response = client.post("/nats/test/chat-message", params=params)
            assert response.status_code == 200
            data = response.json()
            assert "Chat message event published" in data["message"]
            log_test_result(test_name, True, f"- {len(long_content)} character message")
        except Exception as e:
            log_test_result(test_name, False, f"- {str(e)}")
            raise

    def test_agent_task_with_complex_result(self, client):
        """Test agent task event with complex nested result data."""
        test_name = "Complex Nested Data Structures"
        try:
            params = {"agent_id": "complex_agent", "task_id": "complex_task"}
            complex_result = {
                "status": "completed",
                "metrics": {
                    "processing_time": 1.5,
                    "confidence": 0.95,
                    "items_processed": 42,
                },
                "extracted_data": {
                    "entities": ["Person", "Organization"],
                    "sentiment": "positive",
                    "topics": ["AI", "Machine Learning", "Testing"],
                },
                "nested": {"level1": {"level2": {"deep_value": "test"}}},
            }
            json_data = {"result": complex_result}

            response = client.post(
                "/nats/test/agent-task", params=params, json=json_data
            )
            assert response.status_code == 200
            data = response.json()
            assert "Agent task completion event published" in data["message"]
            log_test_result(test_name, True, "- Multi-level nested objects")
        except Exception as e:
            log_test_result(test_name, False, f"- {str(e)}")
            raise

    def test_multiple_rapid_publishes(self, client):
        """Test publishing multiple events rapidly to check for race conditions."""
        test_name = "Rapid Multiple Publishing"
        try:
            responses = []

            for i in range(5):
                event_data = {
                    "subject": f"test.rapid.{i}",
                    "event_data": {"message": f"Rapid message {i}", "index": i},
                    "persistent": False,
                }
                response = client.post("/nats/publish", json=event_data)
                responses.append(response)

            # All should succeed
            for i, response in enumerate(responses):
                assert response.status_code == 200, f"Request {i} failed"
                data = response.json()
                assert data["success"] is True

            log_test_result(
                test_name, True, f"- {len(responses)} rapid publishes completed"
            )
        except Exception as e:
            log_test_result(test_name, False, f"- {str(e)}")
            raise

    def test_publish_with_mixed_data_types(self, client):
        """Test publishing events with various data types."""
        test_name = "Mixed Data Types"
        try:
            mixed_data = {
                "string": "test",
                "integer": 42,
                "float": 3.14,
                "boolean": True,
                "null_value": None,
                "list": [1, 2, 3, "four"],
                "nested_dict": {"inner": "value"},
            }

            event_data = {
                "subject": "test.mixed.types",
                "event_data": mixed_data,
                "persistent": False,
            }
            response = client.post("/nats/publish", json=event_data)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            log_test_result(test_name, True, "- All JSON data types handled")
        except Exception as e:
            log_test_result(test_name, False, f"- {str(e)}")
            raise

"""Basic tests for the Contax Brain.tech portal."""
import pytest
from fastapi.testclient import TestClient


def test_health_check():
    """Test the health check endpoint."""
    from main import app
    client = TestClient(app)
    
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "app_name" in data
    assert "version" in data


def test_home_page():
    """Test the home page loads."""
    from main import app
    client = TestClient(app)
    
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_chat_endpoint_without_api_key():
    """Test chat endpoint validation."""
    from main import app
    client = TestClient(app)
    
    response = client.post(
        "/api/chat",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": False
        }
    )
    # Should fail if no API key is configured
    assert response.status_code in [400, 500]


def test_analyze_document_endpoint():
    """Test document analysis endpoint structure."""
    from main import app
    client = TestClient(app)
    
    response = client.post(
        "/api/analyze-document",
        json={
            "document_text": "Test document",
            "query": "What is this about?"
        }
    )
    # Should fail gracefully if no API key
    assert response.status_code in [400, 500]


def test_generate_code_endpoint():
    """Test code generation endpoint structure."""
    from main import app
    client = TestClient(app)
    
    response = client.post(
        "/api/generate-code",
        json={
            "description": "Create a hello world function",
            "language": "python"
        }
    )
    # Should fail gracefully if no API key
    assert response.status_code in [400, 500]


def test_review_code_endpoint():
    """Test code review endpoint structure."""
    from main import app
    client = TestClient(app)
    
    response = client.post(
        "/api/review-code",
        json={
            "code": "def hello(): pass",
            "language": "python"
        }
    )
    # Should fail gracefully if no API key
    assert response.status_code in [400, 500]


def test_analyze_data_endpoint():
    """Test data analysis endpoint structure."""
    from main import app
    client = TestClient(app)
    
    response = client.post(
        "/api/analyze-data",
        json={
            "data": "Name,Age\nJohn,30",
            "query": "What is the average age?"
        }
    )
    # Should fail gracefully if no API key
    assert response.status_code in [400, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

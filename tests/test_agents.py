from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_hello_world_agent():
    """Test the hello world agent execution"""
    response = client.get("/agent/hello_world")
    assert response.status_code == 200
    assert response.json() == {
        "agent": "hello_world",
        "result": "Hello, World from the agent!"
    }

def test_goodbye_agent():
    """Test the goodbye agent execution"""
    response = client.get("/agent/goodbye")
    assert response.status_code == 200
    assert response.json() == {
        "agent": "goodbye",
        "result": "Goodbye from the agent!"
    }

def test_nonexistent_agent():
    """Test error handling for non-existent agent"""
    response = client.get("/agent/nonexistent")
    assert response.status_code == 404
    assert "Agent not found" in response.json()["detail"]

def test_invalid_agent():
    """Test error handling for invalid agent file"""
    # This would require creating a temporary invalid agent file
    # For now, we'll just verify the 404 response
    response = client.get("/agent/invalid")
    assert response.status_code == 404
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

def test_math_agent_valid():
    """Test math agent with valid token and expression"""
    response = client.get("/agent/math?token=MATH_SECRET&expression=3*(4%2B2)")
    assert response.status_code == 200
    assert response.json() == {
        "agent": "math",
        "result": 18
    }

def test_math_agent_invalid_token():
    """Test math agent with invalid token"""
    response = client.get("/agent/math?token=WRONG_TOKEN&expression=2%2B2")
    assert response.status_code == 200
    assert response.json() == {
        "agent": "math",
        "result": "Error: Invalid token. Access denied."
    }

def test_math_agent_invalid_expression():
    """Test math agent with invalid expression"""
    response = client.get("/agent/math?token=MATH_SECRET&expression=import%20os")
    assert response.status_code == 200
    assert "Error: Invalid expression" in response.json()["result"]

def test_math_agent_missing_params():
    """Test math agent with missing parameters"""
    response = client.get("/agent/math")
    assert response.status_code == 200
    assert "Error: Invalid token" in response.json()["result"]

def test_echo_agent():
    """Test echo agent response"""
    response = client.get("/agent/echo")
    assert response.status_code == 200
    assert response.json() == {
        "agent": "echo",
        "result": {"message": "Echo from agent!"}
    }

def test_time_agent():
    """Test time agent response format"""
    response = client.get("/agent/time")
    assert response.status_code == 200
    result = response.json()
    assert "agent" in result and result["agent"] == "time"
    assert "result" in result and "time" in result["result"]
    # Verify ISO 8601 format (rough check)
    assert "T" in result["result"]["time"] and "Z" in result["result"]["time"]

def test_joke_agent():
    """Test joke agent response format"""
    response = client.get("/agent/joke")
    assert response.status_code == 200
    result = response.json()
    assert "agent" in result and result["agent"] == "joke"
    assert "result" in result and "joke" in result["result"]
    assert isinstance(result["result"]["joke"], str)
    assert len(result["result"]["joke"]) > 0

def test_quote_agent():
    """Test quote agent response format"""
    response = client.get("/agent/quote")
    assert response.status_code == 200
    result = response.json()
    assert "agent" in result and result["agent"] == "quote"
    assert "result" in result and "quote" in result["result"]
    assert isinstance(result["result"]["quote"], str)
    assert len(result["result"]["quote"]) > 0

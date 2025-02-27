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

def test_classifier_agent_with_input():
    """Test classifier agent with input text."""
    response = client.get("/agent/classifier?INPUT_TEXT=Hello,%20how%20are%20you?")
    assert response.status_code == 200
    result = response.json()
    assert "classification" in result
    assert "confidence" in result
    assert result["classification"] in ["Greeting/Question", "Greeting", "Question", "Command", "Statement"]
    assert isinstance(result["confidence"], float)

def test_classifier_agent_no_input():
    """Test classifier agent with no input text (should return an error)."""
    response = client.get("/agent/classifier")  # No INPUT_TEXT provided
    assert response.status_code == 200  # Expecting a 200 OK, even with the error message
    result = response.json()
    assert result == {"error": "INPUT_TEXT is not provided or is not a valid string."}

def test_classifier_agent_empty_input():
    """Test with empty input string"""
    response = client.get("/agent/classifier?INPUT_TEXT=")  # Empty INPUT_TEXT
    assert response.status_code == 200
    result = response.json()
    assert result == {"error": "INPUT_TEXT is not provided or is not a valid string."}

def test_classifier_agent_statement():
    """Test with a simple statement."""
    response = client.get("/agent/classifier?INPUT_TEXT=This%20is%20a%20statement.")
    assert response.status_code == 200
    result = response.json()
    # Ensure the response includes the necessary keys
    assert "classification" in result
    assert "confidence" in result
    # For a simple statement, we expect the classification to be "Statement"
    assert result["classification"] == "Statement"
    assert isinstance(result["confidence"], float)



def test_summarizer_agent():
    """Test summarizer agent"""
    response = client.get("/agent/summarizer?TEXT_TO_SUMMARIZE=FastAPI%20is%20an%20efficient%20framework.%20It%20simplifies%20API%20development.%20This%20agent%20summarizes%20text.")
    assert response.status_code == 200
    result = response.json()
    assert "agent" in result and result["agent"] == "summarizer"
    assert "result" in result and "summary" in result["result"] and "explanation" in result["result"]
    assert isinstance(result["result"]["summary"], str)
    assert isinstance(result["result"]["explanation"], str)

def test_summarizer_agent_max_length():
    """Test summarizer agent with max_length parameter"""
    response = client.get("/agent/summarizer?TEXT_TO_SUMMARIZE=This%20is%20a%20very%20long%20text%20that%20we%20want%20to%20shorten%20to%20a%20reasonable%20length.&max_length=5")
    assert response.status_code == 200
    result = response.json()
    assert "agent" in result and result["agent"] == "summarizer"
    assert "result" in result and "summary" in result["result"] and "explanation" in result["result"]
    assert isinstance(result["result"]["summary"], str)
    assert isinstance(result["result"]["explanation"], str)
    assert len(result["result"]["summary"]) <= 5 + 3  # 5 characters + ellipsis

def test_summarizer_agent_no_input():
    """Test summarizer agent with no input text (should return an error)."""
    response = client.get("/agent/summarizer")  # No TEXT_TO_SUMMARIZE provided
    assert response.status_code == 200  # Expecting a 200 OK, even with the error message
    result = response.json()
    assert "error" in result
    assert result["error"] == "TEXT_TO_SUMMARIZE is not provided or is not a valid string."
    
# Add to existing tests in tests/test_agents.py
def test_textrank_summarizer_agent_with_input():
    """Test TextRank summarizer agent with input text."""
    long_text = (
        "This is the first sentence. This is the second sentence, and it's a bit longer. "
        "Here is a third sentence.  And finally, a fourth sentence."
    )
    response = client.get(f"/agent/textrank_summarizer?TEXT_TO_SUMMARIZE={long_text}")
    assert response.status_code == 200
    result = response.json()
    assert result["agent"] == "textrank_summarizer"
    assert "summary" in result["result"]
    # Basic check: summary is shorter than original
    assert len(result["result"]["summary"]) < len(long_text)

    # Test num_sentences parameter
    response = client.get(f"/agent/textrank_summarizer?TEXT_TO_SUMMARIZE={long_text}&num_sentences=1")
    assert response.status_code == 200
    result = response.json()
    assert len(result["result"]["summary"].split('.')) <= 2

def test_textrank_summarizer_agent_no_input():
    """Test TextRank summarizer with no input."""
    response = client.get("/agent/textrank_summarizer")
    assert response.status_code == 200
    result = response.json()
    assert result == {
        "agent": "textrank_summarizer",
        "result": {"error": "TEXT_TO_SUMMARIZE is not provided or is not a valid string."}
    }
def test_textrank_summarizer_short_input():
    """Test Textrank summarizer with short input."""
    response = client.get(f"/agent/textrank_summarizer?TEXT_TO_SUMMARIZE=short+text")
    assert response.status_code == 200, result
    result = response.json()
    assert result["agent"] == "textrank_summarizer"
    assert "summary" in result["result"]
    assert result["result"]["summary"] == "short text"

def test_textrank_summarizer_empty_input():
    """Test TextRank summarizer with empty input"""
    response = client.get(f"/agent/textrank_summarizer?TEXT_TO_SUMMARIZE=")
    assert response.status_code == 200
    result = response.json()
    assert result == {  # Check for the exact error response structure
        "agent": "textrank_summarizer",
        "result": {"error": "TEXT_TO_SUMMARIZE is not provided or is not a valid string."}
    }
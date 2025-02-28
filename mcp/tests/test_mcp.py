import pytest
from unittest.mock import patch, MagicMock
from app.mcp_adapter import MCPAdapter
from agents.dspy_integration import load_agent
import os

@pytest.fixture
def mock_env_vars():
    """Set up mock environment variables for testing."""
    with patch.dict(os.environ, {
        'MCP_API_KEY': 'test_key',
        'MCP_ENDPOINT': 'http://test-endpoint.com'
    }):
        yield

@pytest.fixture
def mock_requests():
    """Mock requests library for testing."""
    with patch('requests.post') as mock_post, patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        mock_get.return_value = mock_response
        yield mock_post, mock_get

def test_mcp_adapter_initialization(mock_env_vars):
    """Test MCPAdapter initialization with environment variables."""
    adapter = MCPAdapter()
    assert adapter.api_key == 'test_key'
    assert adapter.endpoint == 'http://test-endpoint.com'

def test_mcp_adapter_initialization_missing_env():
    """Test MCPAdapter initialization with missing environment variables."""
    with pytest.raises(ValueError):
        MCPAdapter()

def test_send_context(mock_env_vars, mock_requests):
    """Test sending context data through MCPAdapter."""
    mock_post, _ = mock_requests
    adapter = MCPAdapter()
    context = {"test": "data"}
    
    result = adapter.send_context(context)
    
    assert result == {"status": "success"}
    mock_post.assert_called_once_with(
        'http://test-endpoint.com/send',
        json={"context": context},
        headers={"Authorization": "Bearer test_key"}
    )

def test_get_response(mock_env_vars, mock_requests):
    """Test getting response from MCPAdapter."""
    _, mock_get = mock_requests
    adapter = MCPAdapter()
    
    result = adapter.get_response()
    
    assert result == {"status": "success"}
    mock_get.assert_called_once_with(
        'http://test-endpoint.com/response',
        headers={"Authorization": "Bearer test_key"}
    )

def test_agent_mcp_integration(mock_env_vars, mock_requests, tmp_path):
    """Test MCP integration in an agent."""
    # Create a temporary test agent
    agent_code = """
def agent_main():
    context = {"test": "data"}
    updated_context = update_context(context)
    return {"result": "test", "context": updated_context}
"""
    agent_file = tmp_path / "test_agent.py"
    agent_file.write_text(agent_code)
    
    # Load and run the agent
    agent_module = load_agent(str(agent_file))
    result = agent_module.agent_main()
    
    assert "result" in result
    assert "context" in result
    assert result["result"] == "test"
    assert result["context"] == {"status": "success"}

def test_agent_mcp_integration_no_env(tmp_path):
    """Test agent behavior when MCP is not configured."""
    # Create a temporary test agent
    agent_code = """
def agent_main():
    context = {"test": "data"}
    updated_context = update_context(context)
    return {"result": "test", "context": updated_context}
"""
    agent_file = tmp_path / "test_agent.py"
    agent_file.write_text(agent_code)
    
    # Load and run the agent
    agent_module = load_agent(str(agent_file))
    result = agent_module.agent_main()
    
    assert "result" in result
    assert "context" in result
    assert result["result"] == "test"
    assert result["context"] == {}
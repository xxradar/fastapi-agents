from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json
from app.main import app
from app.mcp_adapter import MCPAdapter

client = TestClient(app)

def test_calculator_agent():
    """Test the calculator agent with a simple expression."""
    # Create test data
    test_expression = "3 + 4 * 2"
    expected_result = 11  # Following standard operator precedence: 3 + (4 * 2) = 11
    
    # Mock the MCP adapter
    with patch('app.mcp_adapter.MCPAdapter.send_context') as mock_send_context:
        # Configure the mock to return a predefined context
        mock_send_context.return_value = {
            "expression": test_expression,
            "previous_result": None
        }
        
        # Make the request
        response = client.post(
            "/agents/calculator",
            json={"expression": test_expression}
        )
        
        # Verify the response
        assert response.status_code == 200
        result = response.json()
        assert result["agent"] == "calculator"
        assert "result" in result
        assert result["result"]["result"] == expected_result

def test_multi_step_reasoning_agent():
    """Test the multi-step reasoning agent."""
    # Create test data
    test_hypothesis = "The Earth is flat"
    
    # Mock the MCP adapter to return a final answer after one iteration
    with patch('app.mcp_adapter.MCPAdapter.send_context') as mock_send_context:
        # Configure the mock to return a final answer
        mock_send_context.return_value = {
            "final_answer": "The Earth is an oblate spheroid",
            "context": {
                "iteration": 1,
                "hypothesis": test_hypothesis
            }
        }
        
        # Make the request
        response = client.post(
            "/agents/multi_step_reasoning",
            json={"hypothesis": test_hypothesis}
        )
        
        # Verify the response
        assert response.status_code == 200
        result = response.json()
        assert result["agent"] == "multi_step_reasoning"
        assert "result" in result
        assert "final_answer" in result["result"]
        assert result["result"]["final_answer"] == "The Earth is an oblate spheroid"

def test_workflow_coordinator_agent():
    """Test the workflow coordinator agent."""
    # Mock the MCP adapter
    with patch('app.mcp_adapter.MCPAdapter.send_context') as mock_send_context:
        # Configure the mock to return a predefined context
        mock_send_context.return_value = {
            "aggregated_result": "Aggregated results from all sub-agents",
            "workflow_status": "completed"
        }
        
        # Make the request
        response = client.post("/agents/workflow_coordinator", json={})
        
        # Verify the response
        assert response.status_code == 200
        result = response.json()
        assert result["agent"] == "workflow_coordinator"
        assert "result" in result
        assert result["result"] == "Aggregated results from all sub-agents"

def test_workflow_decisioning_agent():
    """Test the workflow decisioning agent."""
    # Create test data
    test_task = "Please analyze and report the data"
    
    # Mock the MCP adapter
    with patch('app.mcp_adapter.MCPAdapter.send_context') as mock_send_context:
        # Configure the mock to return a predefined context
        mock_send_context.return_value = {
            "decision": "Data analysis workflow selected",
            "steps": ["collect", "analyze", "report"],
            "status": "completed"
        }
        
        # Make the request
        response = client.post(
            "/agents/workflow_decisioning",
            json={"task_description": test_task}
        )
        
        # Verify the response
        assert response.status_code == 200
        result = response.json()
        assert result["agent"] == "workflow_decisioning"
        assert "result" in result
        # The exact structure of the result depends on the implementation
        # but we can at least check that it's not an error
        assert "error" not in result["result"]
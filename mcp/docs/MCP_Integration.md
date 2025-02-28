# MCP Integration Guide

## Overview

The Module Context Protocol (MCP) integration enables advanced context sharing and inter-module communication between agents. This guide explains how to use the MCP features in your agents and how to configure the system.

## Configuration

### Environment Variables

The following environment variables must be set in your `.env` file:

```env
MCP_API_KEY=your_mcp_api_key
MCP_ENDPOINT=https://your-mcp-endpoint.com/api
```

## Using MCP in Agents

### MCPAdapter

The `MCPAdapter` class provides methods for sending and receiving context data:

```python
from app.mcp_adapter import MCPAdapter

# The adapter is automatically injected into your agent module
# You can access it via the mcp_adapter attribute

def agent_main():
    # Your agent logic here
    context = {"key": "value"}
    
    # Send context to MCP
    updated_context = update_context(context)
    
    return {"result": "output", "context": updated_context}
```

### Available Methods

1. `update_context(context: dict) -> dict`
   - Sends context data to the MCP endpoint
   - Returns updated context from MCP
   - Automatically injected into all agent modules

2. `mcp_adapter.send_context(context: dict) -> dict`
   - Direct access to send context data
   - Returns the response from MCP

3. `mcp_adapter.get_response() -> dict`
   - Retrieves the latest response from MCP

## Error Handling

The MCP integration includes built-in error handling:

- If MCP is not configured (missing environment variables), agents will continue to function without context sharing
- Failed context updates will return an empty dictionary
- All errors are logged for debugging

## MCP Showcase Agents

The following agents demonstrate different aspects of MCP functionality:

### 1. Calculator Agent

**Purpose**: Evaluates arithmetic expressions with context sharing.

**Implementation**:
```python
# Build initial context
context = {
    "expression": processed_expression,
    "previous_result": None
}

# Update context via MCP
updated_context = mcp_adapter.send_context(context)

# Safely evaluate the expression
result = safe_arithmetic_eval(processed_expression)

return {"result": result, "context": updated_context}
```

**Usage**:
```bash
curl -X POST http://localhost:8000/agents/calculator \
  -H "Content-Type: application/json" \
  -d '{"expression": "3 + 4 * 2"}'
```

### 2. Multi-Step Reasoning Agent

**Purpose**: Iteratively refines a hypothesis through context updates.

**Implementation**:
```python
hypothesis = HYPOTHESIS
context = {
    "hypothesis": hypothesis,
    "iteration": 0,
    "history": [hypothesis]
}
max_iterations = 5

for i in range(max_iterations):
    context["iteration"] = i
    # Update context via MCP
    updated_context = mcp_adapter.send_context(context)
    
    # Check if MCP returned a final answer
    if "final_answer" in updated_context:
        return {
            "result": {
                "final_answer": updated_context["final_answer"],
                "context": updated_context["context"]
            }
        }
    
    # Otherwise, refine the hypothesis
    hypothesis += " refined"
    context["hypothesis"] = hypothesis
    context["history"].append(hypothesis)
```

**Usage**:
```bash
curl -X POST http://localhost:8000/agents/multi_step_reasoning \
  -H "Content-Type: application/json" \
  -d '{"hypothesis": "The Earth is flat"}'
```

### 3. Workflow Coordinator Agent

**Purpose**: Coordinates and aggregates responses from multiple sub-agents.

**Implementation**:
```python
# Simulate results from sub-agents
sub_agent_results = {
    "agent1": "Result from agent 1",
    "agent2": "Result from agent 2",
    "agent3": "Result from agent 3"
}

# Create workflow context
context = {
    "sub_agent_results": sub_agent_results,
    "workflow_status": "in_progress"
}

# Update context via MCP
updated_context = mcp_adapter.send_context(context)

# Process updated context to produce final output
final_output = updated_context.get(
    "aggregated_result",
    "Aggregated results: " + ", ".join(sub_agent_results.values())
)

return {"result": final_output, "context": updated_context}
```

**Usage**:
```bash
curl -X POST http://localhost:8000/agents/workflow_coordinator \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 4. Workflow Decisioning Agent

**Purpose**: Selects and executes sub-agents based on task description keywords.

**Implementation**:
```python
# Decide which sub-agents to run based on keywords
sub_agent_results = {}
selected_agents = []
lower_desc = task_description.lower()

if "analyze" in lower_desc:
    sub_agent_results["analysis"] = "Performed comprehensive data analysis"
    selected_agents.append("analysis")
# ... more keyword checks ...

# Build the initial workflow context
context = {
    "task_description": task_description,
    "selected_agents": selected_agents,
    "sub_agent_results": sub_agent_results,
    "workflow_status": "in_progress",
    "steps": steps
}

# Update context via MCP
context = mcp_adapter.send_context(context)

# Generate final output
final_output = context.get(
    "aggregated_result",
    "Aggregated results: " + ", ".join(sub_agent_results.values())
)
```

**Usage**:
```bash
curl -X POST http://localhost:8000/agents/workflow_decisioning \
  -H "Content-Type: application/json" \
  -d '{"task_description": "Please analyze and report the data"}'
```

## Example Agent with MCP

```python
def agent_main():
    """Example agent that uses MCP for context sharing."""
    # Process some data
    result = "Hello, World!"
    
    # Share context with MCP
    context = {
        "output": result,
        "timestamp": "2024-02-25T12:00:00Z"
    }
    
    # Update context using MCP
    updated_context = update_context(context)
    
    # Return result with context
    return {
        "result": result,
        "context": updated_context
    }
```

## Testing

To test MCP integration:

```bash
# Run the test suite
pytest tests/test_mcp.py

# Test a specific agent with MCP
curl -X POST http://localhost:8000/agents/your-agent \
  -H "Content-Type: application/json" \
  -d '{"context": {"key": "value"}}'
```

## Troubleshooting

1. **MCP Not Initialized Warning**
   - Check that MCP_API_KEY and MCP_ENDPOINT are set in your .env file
   - Verify that the MCP endpoint is accessible

2. **Context Update Failures**
   - Check network connectivity
   - Verify API key permissions
   - Review MCP endpoint logs

3. **Response Structure Mismatches**
   - Ensure agent return structures match expected formats in tests
   - Check for nested vs. flat result structures

## Next Steps

1. Create agents that leverage MCP for advanced context sharing
2. Implement context-aware decision making
3. Build multi-step reasoning workflows using shared context
4. Develop agents that collaborate through shared context
5. Implement more complex workflow coordination patterns
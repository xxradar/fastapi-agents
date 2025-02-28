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

## Next Steps

1. Create agents that leverage MCP for advanced context sharing
2. Implement context-aware decision making
3. Build multi-step reasoning workflows using shared context
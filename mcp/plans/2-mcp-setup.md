file: 2-mcp-setup.md

# Step 2: MCP Integration

This step focuses on integrating the Module Context Protocol (MCP) into the FastAPI Agent System. The goal is to enable advanced context sharing and inter-module communication, which will enhance state management and reasoning across agents.

---

## Requirements

- **Incorporate MCP Libraries and Utilities:**
  - Research and select appropriate MCP libraries or create a custom Python adapter.
  - Ensure that the MCP adapter can send context data to and receive responses from an MCP endpoint.
  - Example functionality should include methods like `send_context()` and `get_response()` using HTTP calls.

- **Update Common Agent Interfaces:**
  - Modify the standard agent interface (the expected structure of single file agents) to include MCP-specific hooks.
  - For example, agents should be able to:
    - **Send Context:** Share relevant state information (e.g., current input, previous outputs) via the MCP adapter.
    - **Receive Context:** Accept updated context or configuration information from the MCP system.
  - Consider adding placeholder variables or functions (e.g., `update_context(context)`) that agents can call during their execution.

- **Configuration and Environment Setup:**
  - Add environment variables for MCP integration (e.g., `MCP_API_KEY`, `MCP_ENDPOINT`) in your `.env` file.
  - Ensure these variables are loaded securely using libraries like `python-dotenv`.

---

## Pseudocode Example

Below is a pseudocode example of a simple MCP adapter and how it might be used within an agent:

```python
import requests

class MCPAdapter:
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint.rstrip('/')
        self.api_key = api_key

    def send_context(self, context_data: dict) -> dict:
        """
        Sends context data to the MCP endpoint.
        """
        url = f"{self.endpoint}/send"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"context": context_data}
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_response(self) -> dict:
        """
        Retrieves the response from the MCP endpoint.
        """
        url = f"{self.endpoint}/response"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

# Usage within an agent module:
def update_context_for_agent(current_context: dict):
    # This function can be called by agents to update or retrieve shared context.
    mcp_adapter = MCPAdapter(endpoint="https://mcp.example.com/api", api_key="YOUR_MCP_API_KEY")
    result = mcp_adapter.send_context(current_context)
    return result

def agent_main():
    """
    Example Agent with MCP Integration.
    
    This agent performs its core task and then sends its state to the MCP system.
    
    Usage:
      Set any required global variables and call agent_main().
    """
    # Core agent logic here...
    output = "Agent processed its task."
    
    # Prepare context data for MCP sharing.
    context = {
        "output": output,
        "additional_info": "Sample context data for MCP integration"
    }
    
    # Update context using MCP adapter.
    updated_context = update_context_for_agent(context)
    
    # Return combined output.
    return {"result": output, "updated_context": updated_context}
```

---

## Documentation

- **MCP Setup Documentation:**  
  - Document the MCP integration steps, adapter usage, and configuration in a new file (e.g., `/docs/MCP_Integration.md`).
  - Include references to the MCP Framework source and any example implementations.

---

## Logging and Testing

- **Logging:**  
  - Create a new logs file '/logs/2-logs.md' and update it after completing each MCP integration task.
  - Log summaries of tasks completed, any encountered issues, and decisions made.

- **Testing:**  
  - Add automated tests in the `/tests` folder to verify:
    - The MCP adapter functions correctly (e.g., sending and receiving context data).
    - Agents that include MCP hooks behave as expected.
  - Run tests using:
    ```bash
    pytest tests/
    ```
  - Update the logs with test results.

---

## Summary

By completing Step 2, you will:
- Integrate MCP libraries/utilities into your FastAPI backend.
- Update agent interfaces to support context sharing and dynamic communication.
- Document the integration process thoroughly.
- Ensure that all changes are tracked via logs and validated through automated tests.

This step lays the foundation for building advanced, context-aware agents in subsequent phases.

--- Future Development (as context only)
## Step 3: Implement MCP Showcase Agents

- **Develop MCP Agents (Approx. 5):**  
  - Create a set of agents that utilize MCP features for advanced context handling and decision-making.
  - Use a mix of GET and POST endpoints where appropriate.
  - Examples might include context-aware calculators, multi-step reasoning agents, or workflow coordinators.
  
- **Testing and Logging:**  
  - Validate that each MCP agent correctly processes and shares context.
  - Update logs and tests accordingly.
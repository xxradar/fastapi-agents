# Implementation Guide for MCP-LLM Agents

This master guide outlines the major steps to extend the base FastAPI Agent System with MCP (Module Context Protocol) capabilities. Each major phase has its own detailed plans document in the `/plans` folder.

---

## Logging and Testing Instructions

### Logging
1. **Create a Logs File:**  
   - Create a new file at `/logs/<plan #>-logs.md` in the repository root.
2. **Update After Each Step:**  
   - After completing each integration step, update the corresponding `/logs` document (e.g., `/logs/1-logs.md`) with:
      - A summary of tasks completed.
      - Test results and any issues encountered.
      - Notes or decisions made during the step.
3. **Commit Logs Regularly:**  
   - Ensure that each update is committed with clear commit messages referencing the log entry.

### Testing
1. **Set Up the Tests Folder:**  
   - Create a `/tests` folder (if it doesn't already exist).
2. **Add Tests:**  
   - Add automated tests for all new endpoints, including:
      - GET endpoints for direct agent calls (e.g., `/agent/{agent_name}`).
      - The new POST endpoint for dynamic agents (`/agents/{agent_name}`).
    - Include tests that verify:
      - Correct output for valid requests.
      - Proper error handling for missing parameters or invalid agent names.
3. **Run Tests:**  
   - Execute the tests using:
      ```bash
      pytest tests/
      ```
4. **Log Testing Results:**  
   - After running tests, update the corresponding logs file with a summary of the test results, including any failures or issues and steps taken to resolve them.

---

## Step 1: Environment Setup and Refactoring

- **MCP Setup:**  
  - Install additional dependencies:
    ```bash
    pip install requests
    ```
  - Configure environment variables for MCP in your `.env` file:
    ```
    MCP_API_KEY=your_mcp_api_key
    MCP_ENDPOINT=https://your-mcp-endpoint.com/api
    ```
  
- **Refactor Application Structure:**  
  - Split `main.py` to extract agent routes into a separate routes file (e.g., `app/routes.py`).
  - Update `main.py` to initialize the FastAPI app and include the new routes:
    ```python
    from fastapi import FastAPI
    from app.routes import router as agent_router

    app = FastAPI(title="MCP-LLM Agents")
    app.include_router(agent_router)
    ```
  - Ensure that the dynamic agent execution endpoint `/agent/{agent_name}` remains available for direct GET calls, while the dynamic (parameterized) endpoint will use the plural route `/agents/{agent_name}` for POST requests.

---

## Step 2: MCP Integration

- **Integrate MCP Framework:**  
  - Create an MCP adapter class (`app/mcp_adapter.py`) to handle context sharing and module communication:
    ```python
    class MCPAdapter:
        def __init__(self):
            self.endpoint = os.environ.get("MCP_ENDPOINT")
            self.api_key = os.environ.get("MCP_API_KEY")
            # Initialize adapter with environment variables
            
        def send_context(self, context_data: dict) -> dict:
            """Sends context data to the MCP endpoint."""
            # Implementation details
            
        def get_response(self) -> dict:
            """Retrieves the response from the MCP endpoint."""
            # Implementation details
    ```
  - Update common agent interfaces to include MCP-specific hooks for improved state management and reasoning.
  
- **Documentation:**  
  - Document MCP setup steps and configuration in the `/docs` folder (e.g., in `MCP_Integration.md`).

---

## Step 3: Implement MCP Showcase Agents

- **Develop MCP Agents:**  
  - Create a set of agents that utilize MCP features for advanced context handling and decision-making.
  - Implement the following MCP agents:
  
  1. **Context-Aware Calculator Agent** (`agents/calculator.py`):
     - Evaluates arithmetic expressions with context sharing via MCP.
     - Accessible via POST at `/agents/calculator`.
     - Example payload: `{"expression": "3 + 4 * 2"}`.
  
  2. **Multi-Step Reasoning Agent** (`agents/multi_step_reasoning.py`):
     - Iteratively refines a hypothesis by sharing and updating context through MCP.
     - Accessible via POST at `/agents/multi_step_reasoning`.
     - Example payload: `{"hypothesis": "Initial hypothesis based on input data."}`.
  
  3. **Workflow Coordinator Agent** (`agents/workflow_coordinator.py`):
     - Coordinates and aggregates responses from multiple sub-agents using MCP for shared context.
     - Accessible via POST at `/agents/workflow_coordinator`.
     - No additional parameters required.
  
  4. **Workflow Decisioning Agent** (`agents/workflow_decisioning.py`):
     - Examines a task description, selects sub-agents based on keywords, executes them, and updates shared state using MCP.
     - Accessible via POST at `/agents/workflow_decisioning`.
     - Example payload: `{"task_description": "Please analyze and report the data"}`.
  
- **Testing and Logging:**  
  - Validate that each MCP agent correctly processes and shares context.
  - Update logs and tests accordingly.

---

## Step 4: Final Testing, Documentation, and Release

- **Testing:**  
  - Run comprehensive tests (both automated and manual) on all endpoints.
  - Verify that dedicated routes for direct agents and dynamic routes (POST `/agents/{agent_name}`) function correctly.
  
- **Documentation Updates:**  
  - Update all documentation in the `/docs` folder to reflect new MCP features.
  - Revise the README to include usage instructions and a list of all agents.
  - Add the MIT License to the repository.
  
- **Final Commit and Release:**  
  - Ensure that all logs (in `/logs`) and tests are up-to-date.
  - Commit all changes with clear messages and prepare the repo for public release.

---

## Summary

This implementation guide extends the base FastAPI Agent System with advanced capabilities by integrating MCP for enhanced context sharing. The phases include:

1. **Environment Setup and Refactoring:** Install dependencies, configure environment variables, and refactor the app.
2. **MCP Integration:** Incorporate MCP for enhanced context sharing.
3. **MCP Showcase Agents:** Build and test agents that utilize MCP features.
4. **Final Testing, Documentation, and Release:** Comprehensive testing, documentation updates, and final commit for public release.

This guide serves as the master roadmap for the mcp folder within the mono repo, guiding the development process through advanced agent integration.

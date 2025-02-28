**/plans/1-frameworks.md**

# Plan for Adding Frameworks (MCP & LLM Integration)

## Objective

- **Integrate MCP and LLM frameworks** (Google and OpenAI) into the existing FastAPI agent system.
- Maintain all agents as single file agents.
- **Refactor Application Structure:**  
  - Extract agent routes into a separate routes file.
  - Update endpoints:
    - Direct agents will use GET at `/agent/{agent_name}`.
    - Dynamic agents will be accessed via a POST at `/agents/{agent_name}`.
- Establish a solid foundation for advanced context-sharing and LLM-powered agent features.

---

## Logging and Testing Instructions

### Logging
1. **Create a Logs File:**  
   - Create a new file at `/logs/1-logs.md` in the repository root.
2. **Update After Each Step:**  
   - After completing each integration step (e.g., environment setup, refactoring, endpoint updates), update `/logs/1-logs.md` with:
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
   - After running tests, update `/logs/1-logs.md` with a summary of the test results, including any failures or issues and steps taken to resolve them.

--- 

## Overview

This phase builds on the base Repo 1 implementation (Hello World Agent System) by adding support for MCP and LLM integrations. The integration will:
- Add required dependencies and environment variables for MCP and LLM.
- Refactor the application to separate static (direct) agent endpoints and dynamic agent endpoints.
- Ensure the dynamic endpoint now accepts POST requests and is accessible at the pluralized route `/agents/{agent_name}`.
- Preserve the single file agent approach for simplicity and modularity.

---

## Implementation Steps

### 1. Environment Setup

- **Install Additional Dependencies:**  
  - Add SDKs for OpenAI and Google LLM integration (e.g., `openai`, `requests`).
  - Optionally, add any MCP-specific libraries if available.
  - Update `requirements.txt`:
    ```bash
    pip install openai requests
    ```
- **Configure Environment Variables:**  
  - In your `.env` file, add:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    GOOGLE_API_KEY=your_google_api_key
    MCP_API_KEY=your_mcp_api_key
    ```
- **Maintain Single File Agents:**  
  - All agents (e.g., `hello_world.py`, `math.py`, etc.) remain in the `agents/` directory.

---

### 2. Refactor Application Structure

- **Create a Dedicated Routes File:**  
  - Create a new file `app/routes.py` to hold all agent-related endpoints.
  - Move the agent execution logic from `main.py` to `routes.py` while preserving the dynamic loading functionality.
- **Update `main.py`:**  
  - Refactor `main.py` to initialize the FastAPI app and include routes from `routes.py`.
  - Example:
    ```python
    from fastapi import FastAPI
    from app.routes import router as agent_router

    app = FastAPI(title="MCP-LLM Agents")
    app.include_router(agent_router)
    ```
- **Log Instruction:**  
  - Update `/logs/1-add-frameworks.md` with a summary of the refactoring tasks completed.

---

### 3. Update Endpoints

- **Direct Agent Endpoints (GET):**  
  - All static agents continue to be available via the endpoint:
    ```
    GET /agent/{agent_name}
    ```
- **Dynamic Agent Endpoint (POST):**  
  - Refactor the dynamic agent endpoint to accept POST requests.
  - New endpoint: 
    ```
    POST /agents/{agent_name}
    ```
  - **Pseudocode for the Dynamic Endpoint:**
    ```python
    @app.post("/agents/{agent_name}")
    async def execute_dynamic_agent(agent_name: str, payload: dict):
        """
        Execute a dynamic agent with additional parameters provided in the request body.
        """
        agent_file = os.path.join("agents", f"{agent_name}.py")
        if not os.path.exists(agent_file):
            raise HTTPException(status_code=404, detail="Agent not found.")
        
        try:
            agent_module = load_agent(agent_file)
            # Update agent globals with payload values if supported
            for key, value in payload.items():
                if hasattr(agent_module, key):
                    setattr(agent_module, key, value)
            
            output = run_agent(agent_module)
            return {"agent": agent_name, "result": output}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error executing agent: {str(e)}")
    ```
- **Log Instruction:**  
  - Document the changes to endpoints and update `/logs/1-add-frameworks.md`.

---

### 4. Validate and Test

- **Local Testing:**  
  - Start the server using:
    ```bash
    uvicorn app.main:app --reload
    ```
  - Verify that:
    - GET `/agent/{agent_name}` still returns correct responses.
    - POST `/agents/{agent_name}` correctly processes dynamic parameters from the JSON payload.
- **Automated Tests:**  
  - Update your test suite (in `/tests`) to cover both GET and POST endpoints.
- **Log Instruction:**  
  - Record test outcomes and any issues in `/logs/1-add-frameworks.md`.

---

### 5. Documentation and Next Steps

- **Documentation Updates:**  
  - Update `/docs/Implementation_Guide.md` to reflect the new endpoints and integration details.
  - Document MCP and LLM configuration and usage in `/docs/llm-guide.md` and related documents.
- **Final Review:**  
  - Ensure all changes are documented, tests are passing, and logs are updated.
- **Plan Next Phase:**  
  - The next phase will include MCP integration with advanced agents and the addition of LLM-powered agents.

---

## Summary

This plan establishes the foundation for integrating MCP and LLM frameworks into the FastAPI agent system. It covers:
- Environment setup for MCP and LLM.
- Refactoring the application to separate direct and dynamic agent endpoints.
- Changing the dynamic agent endpoint to a POST route at `/agents/{agent_name}`.
- Validating the changes through testing and updating documentation.

This document will be saved as **/plans/1-add-frameworks.md** and serves as the roadmap for the initial framework integration phase.

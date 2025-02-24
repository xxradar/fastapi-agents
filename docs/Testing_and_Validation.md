**docs/Testing_and_Validation.md**

# Testing and Validation Guide

This guide outlines how to test the custom agent system to ensure it works as expected. It covers manual testing steps using tools like `curl` or an API client, as well as suggestions for writing automated tests.

## Manual Testing Steps

Before writing any automated tests, it’s useful to test the system interactively.

1. **Run the Server**: Ensure your FastAPI server is running (e.g., `uvicorn app.main:app --reload`). Also, ensure you have configured `SUPABASE_URL` and `SUPABASE_KEY`. If using an auth dependency, you might need to supply a header for user ID or a valid JWT in your test requests.

2. **Create an Agent (POST /agents)**:  
   Use `curl` or an API tool to create a new agent. For example:  
   ```bash
   curl -X POST http://localhost:8000/agents \
        -H "Content-Type: application/json" \
        -H "X-User-ID: <your-user-id>" \
        -d '{
          "agent_name": "test_bot",
          "description": "replies with a test message",
          "agent_config": "def agent_main():\n    return {\"msg\": \"Hello from test_bot\"}"
        }'
   ```  
   (Replace `<your-user-id>` with an actual user ID UUID if required by your auth dependency. If you implemented proper JWT auth, you’d include an Authorization header instead.)  
   **Expected Result**: You should get a JSON response with `{"agent_name": "test_bot", "description": "...", "message": "Agent created successfully"}` and HTTP status 201.  
   **Validate DB**: Log in to Supabase or use the CLI to ensure that the `agents` table now has a row for `test_bot` with your user ID.

3. **List Agents (GET /agents)**:  
   ```bash
   curl -X GET http://localhost:8000/agents \
        -H "Content-Type: application/json" \
        -H "X-User-ID: <your-user-id>"
   ```  
   **Expected Result**: A JSON array containing at least one agent. For example: `[ {"agent_name": "test_bot", "description": "replies with a test message"} ]`.  
   If you created multiple agents, they all should appear. If you provide a query param for name:  
   ```bash
   curl -X GET "http://localhost:8000/agents?name=test_bot" -H "X-User-ID: <your-user-id>"
   ```  
   you should get only the matching agent object or a 404 if not found.

4. **Execute Agent (GET /agents/{user_id}/{agent_name})**:  
   ```bash
   curl -X GET http://localhost:8000/agents/<your-user-id>/test_bot \
        -H "X-User-ID: <your-user-id>"
   ```  
   (Again, use your actual user_id in the URL and header or use the appropriate token if JWT is in place.)  
   **Expected Result**: The agent logic runs and returns its output. For our `test_bot`, we expected it returns `{"msg": "Hello from test_bot"}`. The HTTP status should be 200.  
   - Try the test mode:  
     ```bash
     curl -X GET "http://localhost:8000/agents/<your-user-id>/test_bot?test=true" \
          -H "X-User-ID: <your-user-id>"
     ```  
     It should still execute and return the same or slightly modified output indicating test. For our simple agent, likely the same `{"msg": "Hello from test_bot"}` plus maybe a `"test": true` if we included that in output. The main difference might be internal (no side effects).  
   - Error case: Try with a wrong agent name or user_id:  
     ```bash
     curl -X GET http://localhost:8000/agents/<your-user-id>/nonexistent_bot -H "X-User-ID: <your-user-id>"
     ```  
     Expect a 404 Not Found response with `{"detail": "Agent not found."}`.  
     Or try switching user_id to something else (if not blocked by auth dependency) and ensure you get 403 Forbidden due to the mismatch.

5. **Create Agent with AI Generation**: If you implemented the generation for missing `agent_config`, test it:  
   ```bash
   curl -X POST http://localhost:8000/agents \
        -H "Content-Type: application/json" \
        -H "X-User-ID: <your-user-id>" \
        -d '{
          "agent_name": "auto_bot",
          "description": "says hello automatically"
        }'
   ```  
   This omits `agent_config`. The server should generate some code (maybe using your placeholder logic). The response should indicate success. Then try executing `auto_bot` to see what it does. For the placeholder, it might return a message incorporating the description.

6. **Security Test (if applicable)**: If you have authentication in place, test without providing credentials:  
   ```bash
   curl -X GET http://localhost:8000/agents
   ```  
   Without `X-User-ID` or token, expect a 401 Unauthorized from the dependency. Similarly, test trying to access someone else’s agent if you can simulate that scenario (should be forbidden or no data).

Use an API client like **Postman** or **Insomnia** for more convenient testing, especially for JWT tokens. Verify all edge conditions (missing fields in POST, invalid JSON, etc.). The FastAPI docs (at `http://localhost:8000/docs`) should also reflect your new endpoints and models – check that for correctness (the Pydantic models will show the schema for requests/responses).

## Automated Testing (Pytest)  
Setting up automated tests ensures future changes don’t break functionality:

1. **Install testing tools**: Ensure `pytest` and `httpx` (for making async requests) are in your dev requirements.  
2. **Test client**: Use FastAPI’s `TestClient` for synchronous tests or `AsyncClient` for async tests.  
   Example of a basic test file `test_agents.py`:  
   ```python
   from fastapi.testclient import TestClient
   from app.main import app

   client = TestClient(app)

   def test_create_and_run_agent():
       # 1. Create agent
       agent_data = {
           "agent_name": "pytest_bot",
           "description": "created by pytest",
           "agent_config": "def agent_main():\n    return {'res': 'pytest success'}"
       }
       response = client.post("/agents", json=agent_data, headers={"X-User-ID": "test-user-1"})
       assert response.status_code == 200 or response.status_code == 201
       res_json = response.json()
       assert res_json["agent_name"] == "pytest_bot"
       # 2. List agents and ensure our agent is present
       list_resp = client.get("/agents", headers={"X-User-ID": "test-user-1"})
       assert list_resp.status_code == 200
       agents = list_resp.json()
       names = [agent["agent_name"] for agent in agents]
       assert "pytest_bot" in names
       # 3. Execute the agent
       run_resp = client.get(f"/agents/test-user-1/pytest_bot", headers={"X-User-ID": "test-user-1"})
       assert run_resp.status_code == 200
       result = run_resp.json()
       assert result.get("result", {}).get("res") == "pytest success"
   ```  
   This test: creates an agent, verifies creation, lists agents to find it, and runs it verifying the output. It uses a dummy user ID `"test-user-1"`. If using actual auth, you would need to handle providing a valid token or adjusting the dependency for test (perhaps by monkeypatching `get_current_user` to return "test-user-1").  

3. **Edge case tests**: Write tests for things like duplicate agent creation:  
   ```python
   def test_duplicate_agent_name():
       client = TestClient(app)
       data = {"agent_name": "dup_bot", "description": "dup test"}
       headers = {"X-User-ID": "user-123"}
       res1 = client.post("/agents", json=data, headers=headers)
       res2 = client.post("/agents", json=data, headers=headers)
       assert res1.status_code == 201
       assert res2.status_code == 400  # or whatever you return for duplicate
   ```  
   And test unauthorized access (if no header, expecting 401, etc.).

4. **Test cleanup**: Depending on your test isolation, you might want to run tests against a separate supabase schema or use a fixture to clean up (delete inserted agents) afterwards. For now, if using a real Supabase instance, be cautious as tests will insert data. You might use a local or test project, or consider mocking the database calls.  

   To mock supabase, you could patch the `supabase.from_("agents")...execute()` calls to return dummy data. This might be complex given the fluent interface. Another approach is to set up a testing Supabase URL (like pointing to a local Postgres with similar schema). For integration tests, using a real database is fine as long as it’s test data.

5. **Running tests**: Execute `pytest` in the project. All tests should pass. Integrate this into your CI/CD if possible, so any change runs these tests.

## Validation Checklist  
Go through this checklist to validate the system:

- [x] **Agent Creation**: Verified via API call and database entry.  
- [x] **Agent Execution**: Verified output is correct and corresponds to the code.  
- [x] **Multiple Agents**: Create multiple agents for the same user and ensure they all list and individually execute correctly.  
- [x] **Isolation**: Ensure that one user cannot see or execute another user’s agents. This might involve using two different user IDs in tests and verifying cross-access is denied.  
- [x] **Test Mode**: Confirm that adding `?test=true` does not produce side effects. If possible, create an agent that would normally have a side effect (like writing a file or incrementing a counter) and see that in test mode it doesn’t do it. For example, an agent that writes to a file – in test mode, perhaps it should skip actually writing. This requires the agent logic to pay attention to a `TEST_MODE` flag. If we set `module.TEST_MODE = test_mode` as in our execution function, you can design the agent code to check `if globals().get("TEST_MODE"):` to branch logic.  
- [x] **Error Handling**: Intentionally introduce an error: e.g., create an agent with malformed code and attempt to run it. The execution endpoint should catch the exception and return a 500 with a meaningful message. Check that the server doesn’t crash and the error is logged.  
- [x] **Performance (basic)**: Try a quick load test with say 10 sequential executions of an agent to see that it handles it (FastAPI can handle many, and our operations are quick DB lookups and in-memory calls). If using many large agents, ensure it’s still fine.  
- [x] **Documentation Accuracy**: Navigate to `/docs` (the Swagger UI) of the running server. Ensure the POST and GET endpoints are documented properly with request body and parameters. FastAPI automatically documents Pydantic models and path/query params. The optional `test` query param might not show up unless we include it in the function signature. If we used `Request` to parse it manually, consider changing to a function param for documentation, e.g.:  
  ```python
  async def run_agent(user_id: str, agent_name: str, test: bool = False, current_user: str = Depends(get_current_user)):
      ...
  ```  
  This way, the OpenAPI schema will include `test` as a boolean query parameter.  

## Testing with AI Agents (if integrated)  
If you added AI generation, test the quality of generated agents:  
- Create an agent with a complex description and see what code is generated (if using a real AI). Ensure it runs as expected.  
- If the AI is not deterministic, you may get different outputs – ensure your system can handle variations (like if the AI didn’t use `agent_main` but you expected it to, you might refine your prompt).  

## Continuous Validation  
After the initial testing and fixing any issues, it’s good practice to run these tests whenever changes are made. If adding new features (like updating or deleting agents), write corresponding tests. Supabase changes (like altering the schema or policies) should also prompt re-testing of security.

In summary, use both manual and automated testing to validate that: 
- The core features work (create, list, execute). 
- The optional test mode does what it’s supposed to. 
- Security measures are effective. 
- The system behaves well under normal and edge conditions.

With a fully tested system, you can proceed to deploy or extend it. Before deploying, review **Security_Considerations.md** to ensure the system is hardened for a production environment.
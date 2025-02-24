**docs/Architecture.md**

# System Architecture

## Overview  
The **FastAPI Custom Agent System** is composed of a web API layer, a database layer, and dynamic execution components that together enable user-defined “agents”. At a high level, the architecture includes:  

- **FastAPI Application** – Handles HTTP requests, routing, and execution of agent logic.  
- **Supabase Database** – Stores agent definitions (and potentially user info) in a Postgres database with Row-Level Security for data isolation.  
- **Agent Manager** – A component within the FastAPI app responsible for creating, storing, and executing agent code (either in-memory or via files).  
- **Authentication & Authorization** – (Optional) Uses Supabase Auth for identifying users via JWTs, ensuring each user accesses only their agents.  
- **AI Code Generator** – (Optional) An AI-assisted module that can generate agent code from a description, used during agent creation if needed.

## Component Details

### FastAPI Application  
The FastAPI app exposes endpoints for agent management under an `/agents` route namespace. Key sub-components include:  
- **APIRouter/Endpoints**: FastAPI endpoints for creating agents (`POST /agents`), listing/querying agents (`GET /agents`), and executing an agent (`GET /agents/{user_id}/{agent_name}` with an optional `?test` query param). These routes parse incoming requests, interact with the database, and trigger agent execution.  
- **Pydantic Models**: Used for request validation and response serialization. For example, a `AgentCreate` model validates the JSON body for creating a new agent (including fields like `agent_name` and `description`).  
- **Agent Execution Logic**: The code that runs an agent’s behavior. This can be a generic handler that looks up an agent by user and name, then executes its `agent_config`. Depending on configuration, it may interpret `agent_config` as Python code, a prompt, or parameters that define the agent’s actions.

### Supabase Database  
Supabase (backed by PostgreSQL) serves as the persistent store:  
- **Agents Table**: Stores agent definitions with columns for user ID, agent name, configuration, etc. This is the core table enabling multi-user agent storage.  
- **Users**: If using Supabase Auth, user accounts are managed by Supabase. Each authenticated user has a UUID (`auth.uid()`) that we use as `user_id` in the agents table to link agents to their owner.  
- **Row-Level Security (RLS)**: The agents table should have RLS enabled. A policy ensures that each user can `SELECT` and `UPDATE/DELETE` only their own agents (e.g., `USING (auth.uid() = user_id)` in the policy) ([Row Level Security | Supabase Docs](https://supabase.com/docs/guides/database/postgres/row-level-security#:~:text=create%20policy%20,their%20own%20todos)). This provides a database-enforced security layer in addition to application-layer checks.  
- **Supabase Client**: The FastAPI app uses Supabase’s Python client or REST API to perform queries. The client requires the project URL and an API key to initialize a connection ([Python: Initializing | Supabase Docs](https://supabase.com/docs/reference/python/initializing#:~:text=import%20os%20from%20supabase%20import,create_client%2C%20Client)). For example, using `create_client(supabase_url, supabase_key)` yields a client through which we can call `.from_("agents").insert({...}).execute()` to insert a new agent ([Building a CRUD API with FastAPI and Supabase: A Step-by-Step Guide](https://blog.theinfosecguy.xyz/building-a-crud-api-with-fastapi-and-supabase-a-step-by-step-guide#:~:text=user%20%3D%20supabase.from_%28,hased_password%7D%29%5C%20.execute)).

### Agent Manager  
The Agent Manager is a conceptual part of the FastAPI app that handles the lifecycle of agents: creation, storage, retrieval, and execution. It abstracts the details of how agent logic is executed. Key responsibilities:  
- **Storing Agents**: Receives agent definitions via the API and stores them in Supabase. It may also keep an in-memory registry (dictionary) of active agent functions or track file locations if using file-based agents.  
- **Dynamic Execution**: When an execution request comes in, the manager fetches the agent’s config. If the agent’s logic is stored as code, the manager will execute it. This could mean running a Python function directly (in-memory) or importing and calling a function from a generated file. The execution is dynamic because it depends on user-defined content.  
- **Test Mode Handling**: The manager interprets the `test` query parameter. In test mode, it might route the execution to a sandbox environment or use dummy data to prevent side effects. For instance, an agent that normally writes to a database could skip that step in test mode. The manager ensures the output is returned without committing any persistent changes when `test=true`.  

### Authentication & Authorization (Optional)  
If the system integrates Supabase Auth, each request should include a JWT (JSON Web Token) from the authenticated user. The FastAPI app can decode and verify this token to get the `user_id` of the requester. This is used to:  
- Validate that `user_id` in the path (for execution or listing) matches the authenticated user’s ID.  
- Ensure that users can’t create or access agents on behalf of others.  
- Provide the `user_id` when inserting new agents into the database.  

On the Supabase side, using the anon key enforces that the JWT is sent with each request. The Supabase Python client’s `execute()` calls can include the JWT so that RLS policies apply. If using the service key (which bypasses RLS ([Authorization via Row Level Security | Supabase Features](https://supabase.com/features/row-level-security#:~:text=4,bypassrls%20privilege%20for%20administrative%20tasks))), the application must itself enforce authorization checks.  

### AI Code Generator (Optional Component)  
An optional AI-assisted coding tool can be integrated when creating agents. For example, if a user provides a description of the agent’s desired functionality, the system can use an AI (like OpenAI’s GPT) to generate the Python code for the agent. This component would:  
- Take a description or high-level instructions from the user.  
- Use a prompt to an AI service to generate code (a function or script) that implements the described agent logic.  
- Return the generated code to be stored in `agent_config` (and possibly saved as a file).  
- This code is then executed when the agent is invoked.  

This feature can greatly enhance usability, allowing non-developers to create agents with natural language. However, it introduces additional considerations (code validation, security sandboxing, etc., discussed in **Security_Considerations.md**).

## Data Flow

### 1. Agent Creation Flow  
1. **Request**: The user sends a **POST** request to `/agents` with a JSON body containing `agent_name`, `description`, and optionally the agent logic or config. The request must include authentication (e.g., a bearer token) if auth is enabled.  
2. **FastAPI Processing**: The request is received by the FastAPI app’s `/agents` endpoint handler. The JSON is validated against the `AgentCreate` Pydantic model.  
3. **(Optional AI Generation)**: If the user did not provide explicit code and a description is present, the handler can invoke the AI Code Generator. The generator returns a code snippet or configuration for the agent.  
4. **Database Insert**: The agent details (user_id, name, description, config code) are inserted into the Supabase `agents` table via the Supabase client. For example:  
   ```python
   supabase.from_("agents").insert({
       "user_id": current_user_id,
       "agent_name": agent_name,
       "description": description,
       "agent_config": agent_code_str
   }).execute()
   ```  
   The Supabase client returns a result indicating success or failure ([Building a CRUD API with FastAPI and Supabase: A Step-by-Step Guide](https://blog.theinfosecguy.xyz/building-a-crud-api-with-fastapi-and-supabase-a-step-by-step-guide#:~:text=user%20%3D%20supabase.from_%28,hased_password%7D%29%5C%20.execute)).  
5. **Response**: The API returns a response to the client. On success, this might include the new agent’s ID or details, or a message confirming creation. On failure (e.g., duplicate name or DB error), an error message is returned.  
6. **Post-creation**: The Agent Manager may also load the new agent into an in-memory registry or save the code to a file at this point, preparing it for fast execution on subsequent calls (depending on the chosen execution strategy).

### 2. Agent Retrieval/Listing Flow  
1. **Request**: The client sends a **GET** request to `/agents`. If a specific agent is requested, it might be `/agents?name=<agent_name>` or a RESTful endpoint like `/agents/{agent_name}` (depending on implementation). If no specific name is given, the user’s entire agent list is requested.  
2. **FastAPI Processing**: The request hits the FastAPI handler for listing agents. Authentication is checked to identify the user.  
3. **Database Query**: The handler queries Supabase for agent records belonging to the user. For example:  
   ```python
   result = supabase.from_("agents").select("*").eq("user_id", current_user_id).execute()
   agents = result.data
   ```  
   This uses an equality filter on `user_id` to fetch only the current user’s agents (Supabase RLS would also enforce this if configured).  
4. **Response**: The API returns the list of agents or the details of the requested agent. The response structure might include fields like `agent_name`, `description`, and possibly the `agent_config` (or parts of it, if it’s large or sensitive).  

### 3. Agent Execution Flow  
1. **Request**: The client invokes an agent via **GET** request to `/agents/{user_id}/{agent_name}`. For example, `GET /agents/123e4567-e89b-12d3-a456-426614174000/my_agent?test=true`. The `user_id` in the URL identifies the owner, and `agent_name` identifies which agent to run. The query param `test=true` requests a test run.  
2. **FastAPI Routing**: FastAPI matches this URL to a path with parameters. The application likely has a single function handling `GET /agents/{user_id}/{agent_name}` (where both are path parameters) ([Path Parameters - FastAPI](https://fastapi.tiangolo.com/tutorial/path-params/#:~:text=app%20%3D%20FastAPI)). The values are passed into the function automatically by FastAPI. The `test` parameter is captured as an optional query parameter (e.g., function argument `test: bool = False`), which FastAPI will set to `True` if `?test=true` is present ([Query Parameters - FastAPI](https://fastapi.tiangolo.com/tutorial/query-params/#:~:text=%40app.get%28,skip%20%3A%20skip%20%2B%20limit)).  
3. **Authentication & Authorization**: The handler confirms the requesting user is authorized. If using JWT, it ensures the `user_id` in the token matches the `user_id` parameter (they must be invoking their own agent). Otherwise, the request is rejected (HTTP 401/403).  
4. **Fetch Agent Config**: The agent’s details are retrieved from Supabase to get the latest `agent_config`. For instance:  
   ```python
   res = supabase.from_("agents").select("*")\
           .eq("user_id", user_id).eq("agent_name", agent_name).execute()
   agent_record = res.data[0] if res.data else None
   ```  
   If `agent_record` is not found, return a 404 Not Found response.  
5. **Execute Logic**: If found, the system executes the agent:  
   - **In-Memory Mode**: The `agent_config` might be a code string that we `exec` or a reference to a pre-loaded function. The Agent Manager will run the code. For example, if `agent_config` is a Python function code, the manager might do:  
     ```python
     exec(agent_record["agent_config"], globals())
     result = globals().get("agent_main")()  # assuming agent_main() is defined in the code
     ```  
     (In practice, we’d encapsulate this for safety.)  
   - **File-Based Mode**: If a file was generated for this agent (e.g., `agents/123e4567_my_agent.py`), the manager imports and calls it. For example:  
     ```python
     import importlib
     module_name = f"agents.{user_id}_{agent_name}"
     agent_module = importlib.import_module(module_name)
     result = agent_module.run()  # assuming each agent file has a run() function
     ```  
   - **Handling `test`**: If `test` is True, the manager might alter the execution context. For instance, set a flag `IS_TEST_MODE=True` that the agent code can check, or wrap calls to external services in mocks. The goal is to simulate the agent’s behavior without permanent changes. The agent code itself can also check for a `test` parameter and adjust its logic.  
6. **Result**: Capture the result of the agent’s execution. This could be any JSON-serializable output (string, dict, etc.). The handler then returns this as the HTTP response body. For example, if an agent returns `{"message": "Hello, World"}`, the API response will contain that JSON.  
7. **Post-Execution**: Optionally, log the execution or any errors. If not in test mode, you might record usage statistics or agent output to a history log (could be another Supabase table for audit or debugging).

## Dynamic Endpoint Routing  
It’s important to note that the agent execution uses a **dynamic route**. We don’t explicitly write separate functions for each agent; instead, FastAPI’s path parameters handle it. By defining a path like `/agents/{user_id}/{agent_name}`, the app can accept any `user_id` and `agent_name` and route them to one handler ([Path Parameters - FastAPI](https://fastapi.tiangolo.com/tutorial/path-params/#:~:text=app%20%3D%20FastAPI)). This is simpler than programmatically adding routes for each new agent. The handler function uses the parameters to look up and execute the correct agent. 

Alternatively, for more advanced use, FastAPI does allow adding routes at runtime using `app.add_api_route()` ([python - Add route to FastAPI with custom path parameters - Stack Overflow](https://stackoverflow.com/questions/73291228/add-route-to-fastapi-with-custom-path-parameters#:~:text=app%20%3D%20FastAPI,APIRouter)). For example, after creating a new agent, one could register a new route function specific to that agent. However, this is typically not necessary (and would require regenerating the OpenAPI schema manually). The chosen design here keeps things flexible with a single dynamic route.

## Summary  
This architecture ensures a clear separation of concerns: FastAPI handles request/response and user interaction, Supabase handles data persistence and security, and the Agent Manager handles dynamic code execution. By storing agent definitions in the database and loading them on-demand, the system can scale to many users and agents without hard-coding new endpoints. The use of dynamic execution (with caution and security in mind) gives users the power to extend the system’s functionality. 

Proceed to **Technical_Specifications.md** for a low-level description of APIs and data models, or to **Implementation_Guide.md** for how to build this step by step.
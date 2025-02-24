**docs/Technical_Specifications.md**

# Technical Specifications

This document details the specific API endpoints, request/response formats, database schema, and expected behaviors of the custom agent system. It serves as a reference for developers implementing or interacting with the API.

## API Endpoints Overview  
All endpoints are prefixed under `/agents` and return JSON responses. Authentication (e.g., via a Bearer token) is required for all operations that involve a specific `user_id`. The API endpoints include:

- **POST `/agents`** – Create a new custom agent.  
- **GET `/agents`** – List all agents for the authenticated user (or optionally retrieve a specific agent’s details).  
- **GET `/agents/{user_id}/{agent_name}`** – Execute a custom agent for a given user. Supports `?test=true` query for test mode.

### POST `/agents` – Create Agent  
**Description:** Creates a new custom agent for the authenticated user.  

**Request Body:** JSON object with the following fields:  
- `agent_name` (string) – The unique name of the agent to create. This name, combined with the user’s ID, identifies the agent.  
- `description` (string) – A human-readable description of what the agent does.  
- `agent_config` (string or object) – The configuration or code defining the agent’s behavior. This could be a Python code snippet as a string, a JSON with structured parameters, or any format the system expects to execute. *(If this field is not provided or is empty, the system may generate code based on the description using an AI assistant.)*  

Example:  
```json
{
  "agent_name": "weather_bot",
  "description": "Provides weather information for a given city",
  "agent_config": "def agent_main():\n    return {'forecast': 'sunny'}"
}
```  

**Behavior:**  
- The server validates that `agent_name` is provided and not already used by this user. If missing or duplicate, respond with `400 Bad Request` (duplicate might also be `409 Conflict`).  
- If an `agent_config` is provided directly, the server may do basic validation (e.g., ensure it’s a safe string or valid JSON). If not provided, the server will attempt to generate it (this may involve calling an AI service or using a template).  
- On validation success, the server inserts a new record into the `agents` table in Supabase with the user’s ID, agent_name, description, and config. The insertion can be done via Supabase Python client:  
  ```python
  supabase.from_("agents").insert({...}).execute()
  ```  
  This returns the inserted record on success ([Building a CRUD API with FastAPI and Supabase: A Step-by-Step Guide](https://blog.theinfosecguy.xyz/building-a-crud-api-with-fastapi-and-supabase-a-step-by-step-guide#:~:text=user%20%3D%20supabase.from_%28,hased_password%7D%29%5C%20.execute)).  
- The server responds with `201 Created` on success. The response JSON should include the created agent’s details, e.g.,:  
  ```json
  {
    "agent_name": "weather_bot",
    "description": "Provides weather information for a given city",
    "message": "Agent created successfully"
  }
  ```  
  Optionally include an `id` or confirmation of `user_id` association.  
- If there’s an error (e.g., database failure or constraints violation), respond with an appropriate error code and message.

**Authentication:** The request must include credentials (e.g., JWT in Authorization header). The server uses this to identify `user_id`. The `user_id` is **not** expected in the request body to avoid tampering – it’s derived from the auth token or session.

### GET `/agents` – List or Retrieve Agents  
**Description:** Retrieves the list of all agents for the authenticated user. Optionally, can retrieve details of a single agent if a query parameter or sub-route is used.  

**Query Parameters:** (optional)  
- `name` (string) – If provided, filter the results to the agent with this name (for the current user). If not provided, return all agents for the user.

**Behavior:**  
- If `name` is not given: Query the Supabase `agents` table for all entries with `user_id = current_user_id`.  
- If `name` is given: Query the table for `user_id = current_user_id AND agent_name = name`.  
- This uses the Supabase client select functionality, for example:  
  ```python
  query = supabase.from_("agents").select("agent_name, description")\
           .eq("user_id", current_user_id)
  if name:
      query = query.eq("agent_name", name)
  result = query.execute()
  agents = result.data
  ```  
- On success, respond with `200 OK` and a JSON list of agents. For example:  
  ```json
  [
    {
      "agent_name": "weather_bot",
      "description": "Provides weather information for a given city"
    },
    {
      "agent_name": "stock_bot",
      "description": "Gives stock price updates"
    }
  ]
  ```  
  If a specific name was requested, it may return a single object (or a list of one object). If no agents exist, return an empty list `[]`.  
- If the user is not authenticated or authorized, respond with `401 Unauthorized`. (If using RLS and the anon key on the Supabase side, an unauthorized request might simply return no data, but the app should explicitly check auth at the API layer too.)

**Note:** This endpoint does not return the `agent_config` field in the above example for brevity/security. In an actual implementation, you might exclude the full config when listing all agents (especially if it’s large or sensitive). However, if a single agent’s detail is requested (via query param or a separate endpoint like `/agents/{name}`), you could include the config or additional info.

### GET `/agents/{user_id}/{agent_name}` – Execute Agent  
**Description:** Executes the specified agent’s logic and returns the result. This is a dynamic endpoint allowing users to invoke any of their agents by name.  

**Path Parameters:**  
- `user_id` – The user’s unique ID (as stored in Supabase). This should match the authenticated user’s ID (the system must verify this).  
- `agent_name` – The name of the agent to execute.  

**Query Parameters:**  
- `test` (boolean, optional) – If `true`, run the agent in **test mode**. Default is `false` if omitted. (FastAPI will interpret `?test=true` as the boolean value True in the function argument ([Query Parameters - FastAPI](https://fastapi.tiangolo.com/tutorial/query-params/#:~:text=%40app.get%28,skip%20%3A%20skip%20%2B%20limit)).)

**Behavior:**  
1. **Authentication Check:** The server ensures that the requester is authorized to run this agent. Typically, the `user_id` in the URL must match the user ID from the auth token. If not, return `403 Forbidden`.  
2. **Retrieve Agent:** Query the Supabase `agents` table for a record with matching `user_id` and `agent_name`. If not found, return `404 Not Found`.  
3. **Execute Agent Logic:** If found, the agent’s configuration or code is retrieved. The server then executes it:  
   - If the `agent_config` is code (Python function), the server executes it in a controlled environment (see **Security Considerations**). For example, use `exec` to compile the code and call a predefined function (like `agent_main()` or `run()`).  
   - If `agent_config` is a reference to a file or module, import and execute that.  
   - If there is a standard interface (say every agent config is expected to have a function that takes no args and returns a result), the server will invoke that uniformly.  
   - **Test Mode:** If `test=true`, set a flag or modify execution to avoid external side effects. For example, if the agent code tries to call an external API or write to a database, the system might stub those calls out or just simulate a response.  
   - Pseudocode for execution:  
     ```python
     agent = get_agent_from_db(user_id, agent_name)
     if agent:
         code = agent["agent_config"]
         if in_memory_mode:
             exec(code, safe_globals)
             output = safe_globals["agent_main"]()  # assuming agent_main is defined
         else:  # file-based mode
             mod = importlib.import_module(f"agents.{user_id}_{agent_name}")
             output = mod.run()  # assuming each agent file has a run function
         if test_mode:
             output = mark_as_test(output)
         return JSONResponse(output)
     else:
         raise HTTPException(status_code=404, detail="Agent not found")
     ```  
     In the above pseudocode, `safe_globals` would be a restricted dict of globals for execution, and `mark_as_test` might annotate or adjust output to indicate it was a test run, depending on requirements.  
4. **Response:** On successful execution, return `200 OK` and the result of the agent’s function as JSON. The format of this result depends on the agent. It could be simple (e.g., a string message or a dictionary of data). For example:  
   ```json
   {"forecast": "sunny"}  
   ```  
   If the agent logic itself returns a complex object, ensure it’s serializable (or convert it). In test mode, you might include an extra field like `"test": true` in the output to distinguish it, or simply trust that it was a dry run internally.  
5. **Error handling:** If the agent’s execution throws an exception or times out, catch it and return a 500 Internal Server Error with details. You might also return a 400 if the agent code is invalid or caused a known issue (since the agent_config is user-provided, errors are possible). Logging the error for debugging is recommended.

**Security:** This endpoint is the most sensitive. It executes dynamic code, so ensure you implement the safeguards discussed in **Security_Considerations.md** (like running in a sandbox or with limited permissions). Only the agent owner should reach this point of execution – always validate `user_id` against the authenticated user.

## Database Schema  
The primary table involved is `agents`. Below is the specification for the `agents` table in Supabase (PostgreSQL):

- **Table Name:** `agents`  
- **Columns:**  
  - `id` (uuid or bigserial primary key) – Unique identifier for each agent record. Often auto-generated.  
  - `user_id` (uuid or text) – Identifier for the user who owns the agent. If using Supabase Auth, this is the user’s UUID from the `auth.users` table. This field is indexed for efficient lookup by user.  
  - `agent_name` (text) – The name of the agent. This, in combination with `user_id`, should be unique. You can enforce a unique constraint on (`user_id`, `agent_name`) to prevent duplicate agent names per user.  
  - `description` (text) – A brief description of the agent’s purpose.  
  - `agent_config` (text or json) – The stored configuration or code for the agent. This might be a large text blob if storing code. JSON is also possible if the agent is defined by a set of parameters. Choose a data type that fits your use case (for arbitrary code, text is simplest).  
  - `created_at` (timestamp with time zone, default now()) – Timestamp of creation (optional but recommended).  
  - `updated_at` (timestamp with time zone, default now()) – Timestamp of last update (optional, update on modification).  

**Row-Level Security:** Enable RLS on the `agents` table to restrict access. Example policy in SQL:  
```sql
-- Enable RLS
ALTER TABLE public.agents ENABLE ROW LEVEL SECURITY;

-- Allow owners to select their agents
CREATE POLICY "Allow agent owner to read" 
ON public.agents FOR SELECT 
USING (auth.uid() = user_id);

-- Allow owners to modify their agents
CREATE POLICY "Allow agent owner to modify" 
ON public.agents FOR UPDATE USING (auth.uid() = user_id);

-- (Similarly, a policy for DELETE if needed)
```  
These policies use Supabase’s `auth.uid()` function to get the JWT’s user ID and compare to the row’s user_id ([Row Level Security | Supabase Docs](https://supabase.com/docs/guides/database/postgres/row-level-security#:~:text=create%20policy%20,their%20own%20todos)). With these in place, even if the endpoint didn’t thoroughly check user IDs, the database would enforce that a user can only read/update their own records.

**Relationships:** If using Supabase Auth, the `user_id` in `agents` could have a foreign key relationship to `auth.users.id` (Supabase might not allow direct FK to the auth schema, but it's implicitly related). It’s primarily for logical association. Ensure to handle cascading deletes carefully (if a user is deleted, their agents should be deleted as well, either manually or via policy).

## Data Model (Application Level)  
In the FastAPI application, define Pydantic models to mirror the data structure:  
- `AgentCreate` – for POST request body validation, with fields: `agent_name: str`, `description: str`, `agent_config: Optional[str]`. It can include `user_id: str` if we expect the client to send it, but typically we’ll derive user_id from auth, so it might be excluded to prevent spoofing.  
- `Agent` – for responses, representing an agent record. Fields: `agent_name: str`, `description: str`, maybe `agent_config: str` (if you want to return it) and `user_id: str` (to confirm ownership) or `id`. This could be used to format output data from the database.  
- Optionally, a model for `AgentRunResponse` – the output of an agent execution. This could be basically `Any` type since it’s dynamic. Or you can leave it untyped and let FastAPI handle the serialization.

Example Pydantic models code snippet:  
```python
from pydantic import BaseModel
from typing import Optional, Any

class AgentCreate(BaseModel):
    agent_name: str
    description: str
    agent_config: Optional[str] = None

class Agent(BaseModel):
    id: Optional[str]
    user_id: str
    agent_name: str
    description: str
    agent_config: Optional[str] = None

class AgentRunResponse(BaseModel):
    result: Any
    test: Optional[bool] = False
```  
The `AgentRunResponse` can be used to standardize the execution output (wrapping the agent’s raw output into a JSON object with maybe a `result` field and a `test` flag).

## Expected Behavior and Edge Cases  
- **Duplicate Agent Names:** The system should prevent a user from creating two agents with the same name. This can be enforced by checking before insert or relying on a unique constraint in the DB (and catching the error). Return a clear error message if a duplicate is attempted.  
- **Agent Name Constraints:** Define what characters are allowed in `agent_name` (e.g., alphanumeric and underscores). If using file-based approach, agent_name might be used in filenames, so restrict to safe characters to avoid path issues. Validate on create.  
- **Large Agent Config:** If `agent_config` is very large (e.g., long code), consider a limit or store in a text field type that can handle it (Postgres TEXT or even using Supabase Storage if extremely large). The API might not return the full config on list endpoints to save bandwidth.  
- **Performance Considerations:** Each execution call hits the database to get the agent config. Caching strategies could be employed (cache the agent code in memory with a timestamp, etc., invalidating when updated). However, initially clarity and correctness are more important than premature optimization.  
- **Test Mode Differences:** Clearly define what “test mode” does. By default, the documentation assumes it prevents side effects. If an agent, for example, sends an email or writes to a different DB in normal mode, in test mode it should skip or simulate those actions. Ensure the agent developers (users) know how to check for test mode in their code (maybe by reading an environment variable or global flag set by the system). The system itself could handle certain common side effects by stubbed functions in test.  
- **Security Errors:** If a user tries to access another user’s agent (e.g., by altering the URL path), the system should respond with 403 Forbidden (or 404 Not Found, not revealing the existence of the agent). With proper auth and RLS, this situation would normally yield no data, and the API can decide to return 404 to not hint at unauthorized resources.  
- **Supabase Errors:** Supabase client calls return a response object that may contain `.data` (result) or `.error`. Always check for `.error` after a query or insert. If an error exists, handle it (log it, return a 500 or 400 to client depending on type). For example, an insert that violates a constraint might return an error that you use to inform the user.

This technical specification should be used in tandem with the **Implementation Guide** to develop the system, and with the **Testing and Validation** guide to verify each aspect works as intended.
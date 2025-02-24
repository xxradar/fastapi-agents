**docs/Implementation_Guide.md**

# Implementation Guide

This guide provides step-by-step instructions to implement the custom agent system by modifying the base **hello_world_agent** repository. It covers setting up the environment, adding new code, and using AI assistance for faster development. Follow the steps in order to integrate all features.

## Prerequisites  
- **Base Project**: Ensure you have the base FastAPI project (hello_world_agent) set up locally. It should be running a simple FastAPI app (likely a “Hello World” example).  
- **Supabase Project**: A Supabase project created, with the `agents` table set up as per the Technical Specifications. You should have the Supabase URL and API keys ready.  
- **Python 3.9+** (recommended) and environment prepared with required packages (FastAPI, Uvicorn, supabase-py).

## 1. Configure Supabase in the Project  
First, integrate the Supabase client into your FastAPI app so you can communicate with the database.

**a. Install supabase-py** (if not already installed):  
```bash
pip install supabase
```  
This provides the `create_client` function to connect to Supabase.

**b. Create a configuration file** for Supabase (or use environment variables). For example, in the project root, create a file `config.py` with content:  
```python
import os
SUPABASE_URL = os.environ.get("SUPABASE_URL", "<your-supabase-url>")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "<your-supabase-key>")
```  
*(Replace the default values with your actual URL and key or ensure environment variables are set.)*

**c. Initialize Supabase client** in the app. You can create a module `db/supabase.py` (or just within your main app file) to create the client. For instance:  
```python
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
```  
This uses the URL and key to create a client ([Python: Initializing | Supabase Docs](https://supabase.com/docs/reference/python/initializing#:~:text=import%20os%20from%20supabase%20import,create_client%2C%20Client)). You might wrap this in a function or class, but a module-level client is fine for simplicity. The client will be used to perform all DB operations (insert, select, etc.).  

**d. Secure the credentials**: Ensure `config.py` is in `.gitignore` if it contains secrets. Alternatively, use environment variables exclusively and load them (e.g., with Pydantic’s BaseSettings or python-dotenv). Do not hard-code the service role key in code that might be exposed.

## 2. Define the Data Models  
Define Pydantic models for the agent data. Open (or create) a file, e.g., `models.py` in your FastAPI app directory.

Add the following models:  
```python
from pydantic import BaseModel
from typing import Optional

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
```  
These correspond to the request input and database schema. `AgentCreate` will be used to validate incoming data when creating an agent. The `Agent` model can be used if you need to output agent details (though you might omit `agent_config` in responses for security).  

FastAPI will automatically use these models for data validation and documentation.

*AI Tip:* *Use an AI coding assistant (like GitHub Copilot) by typing out the class definitions and letting it auto-complete fields based on the context you’ve given (e.g., it might guess the fields for `AgentCreate` after you type a couple). Always double-check the AI’s output against your intended schema.*

## 3. Implement the Create Agent Endpoint (POST /agents)  
Open your FastAPI app file (commonly `main.py` or `app.py`). We will add a new endpoint function for creating agents.

**a. Import necessary modules:**  
At the top, import FastAPI and the Pydantic model and supabase client:  
```python
from fastapi import FastAPI, HTTPException, Depends
from .models import AgentCreate
from db.supabase import supabase
```  
Also consider importing a dependency for auth if needed (e.g., `from fastapi.security import HTTPBearer` if you plan to use token auth).

**b. Initialize FastAPI app** (if not already present):  
```python
app = FastAPI()
```  
*(If the base already has this, skip.)*

**c. Endpoint function for POST /agents:**  
```python
@app.post("/agents")
async def create_agent(agent: AgentCreate, current_user: str = Depends(get_current_user)):
    # current_user could be a dependency that returns authenticated user's ID
    user_id = current_user  # assuming this is a string/UUID of logged-in user
    # 1. Check for duplicate agent name for this user
    res = supabase.from_("agents").select("id").eq("user_id", user_id).eq("agent_name", agent.agent_name).execute()
    if res.data and len(res.data) > 0:
        raise HTTPException(status_code=400, detail="Agent name already exists.")
    # 2. Generate agent config if not provided
    agent_code = agent.agent_config
    if not agent_code:
        agent_code = generate_agent_code(agent.description)  # AI generation (to implement)
    # 3. Insert into database
    insert_res = supabase.from_("agents").insert({
        "user_id": user_id,
        "agent_name": agent.agent_name,
        "description": agent.description,
        "agent_config": agent_code
    }).execute()
    if insert_res.error:
        # Log error (insert_res.error) for debugging
        raise HTTPException(status_code=500, detail="Failed to create agent.")
    # 4. Optionally load agent into memory or create file
    load_agent_to_runtime(user_id, agent.agent_name, agent_code)
    return {"agent_name": agent.agent_name, "description": agent.description, "message": "Agent created successfully"}
```  
Let’s break down what this does:  
   - It uses a dependency `get_current_user` to retrieve the authenticated user’s ID (you will implement this function to verify a token or session and return the user’s ID; for now, assume it works).  
   - Checks Supabase for an existing agent with the same name for that user. If found, returns an HTTP 400.  
   - If the `agent_config` wasn’t provided, calls a placeholder `generate_agent_code` function. **You need to implement `generate_agent_code(description: str) -> str`** which uses an AI or template to create a code string. This could call an external API (OpenAI) or simply return a default function that prints “Hello” plus the description. For now, you could stub it to return a basic function code or raise NotImplemented if you plan to integrate AI later.  
   - Inserts the new agent into the `agents` table. Uses the supabase client’s `insert` method ([Building a CRUD API with FastAPI and Supabase: A Step-by-Step Guide](https://blog.theinfosecguy.xyz/building-a-crud-api-with-fastapi-and-supabase-a-step-by-step-guide#:~:text=user%20%3D%20supabase.from_%28,hased_password%7D%29%5C%20.execute)). If an error occurs during insert (e.g., database down or constraint violation not caught earlier), it returns a 500 error.  
   - Calls `load_agent_to_runtime` – this is another helper you’ll implement. If you choose in-memory execution, this might compile the code and store the function in a dictionary. If file-based, this could write the code to a new `.py` file. For example, file-based implementation:  
     ```python
     def load_agent_to_runtime(user_id: str, agent_name: str, code: str):
         filename = f"agents/{user_id}_{agent_name}.py"
         with open(filename, "w") as f:
             f.write(code)
     ```  
     In-memory implementation might compile the code:  
     ```python
     agent_namespace = {}
     exec(code, agent_namespace)
     AGENTS[(user_id, agent_name)] = agent_namespace.get("agent_main")
     ```  
     where `AGENTS` is a dict defined at module level to store functions. Document this in **Agent_Creation_Process.md**.  
   - Returns a success message with agent details. FastAPI will serialize this dict to JSON.

**d. Register the route:** In FastAPI, the `@app.post("/agents")` decorator already registers the route. If you are using an `APIRouter`, make sure to include it in the app. For example, you might define these in a router and then do `app.include_router(router)`. The base example likely doesn’t, so defining directly on `app` is fine.

*AI Tip:* *When writing the function, you can use Copilot or ChatGPT to suggest code. For instance, start by writing a comment `# Insert new agent into DB` and let the AI complete the supabase insertion code. Since this is a common pattern, the AI might produce exactly what you need or something close, which you can adjust. Always review the suggested code for correctness (e.g., making sure it uses the right table and fields).*

## 4. Implement the List/Retrieve Agents Endpoint (GET /agents)  
Still in `main.py`, add a GET endpoint to fetch the user’s agents.

```python
@app.get("/agents")
async def list_agents(current_user: str = Depends(get_current_user), name: str = None):
    user_id = current_user
    query = supabase.from_("agents").select("agent_name, description").eq("user_id", user_id)
    if name:
        query = query.eq("agent_name", name)
    res = query.execute()
    if res.error:
        raise HTTPException(status_code=500, detail="Failed to retrieve agents.")
    data = res.data  # This will be a list of dicts
    # If name was provided but not found, data could be an empty list
    if name and len(data) == 0:
        raise HTTPException(status_code=404, detail="Agent not found.")
    return data
```  

This endpoint:  
   - Uses the same `get_current_user` dependency to identify `user_id`.  
   - Accepts an optional query parameter `name`. FastAPI will automatically pass `name` from the URL’s query string (e.g., `/agents?name=weather_bot`) into the function argument. If not provided, `name` is `None`.  
   - Builds a Supabase query to select agent_name and description for the user. (We’re deliberately not selecting `agent_config` here to reduce data size; if you need it for a detail view, you can include it or create a separate endpoint.)  
   - If `name` filter is present, adds it to the query.  
   - Executes the query. Checks for errors and returns a 500 if something went wrong with the DB call.  
   - If a specific name was requested but nothing found, returns 404. Otherwise returns the data list (FastAPI will convert to JSON).  
   - This is a very straightforward use of Supabase’s `.select` and `.eq` methods. Supabase returns `.data` which is a list of rows (each row is a dict with keys as column names). We return that directly. FastAPI will put it in a JSON array.  
   - No explicit Pydantic model is used for the response here, but you could create an `AgentList` model if you want to document it in OpenAPI. For brevity, raw return is fine.

**Testing note:** After implementing, you can run the server and test this by creating some agents (via POST), then calling GET `/agents` and `/agents?name=some_name` to see if it returns correctly.

## 5. Implement the Execute Agent Endpoint (GET /agents/{user_id}/{agent_name})  
This is the core of dynamic execution. Add the following endpoint to your FastAPI app:

```python
from fastapi import Request  # if you need to inspect query params manually

@app.get("/agents/{user_id}/{agent_name}")
async def run_agent(user_id: str, agent_name: str, request: Request, current_user: str = Depends(get_current_user)):
    # 1. Authorization check
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Cannot execute agents of another user.")
    # 2. Parse test query param
    test_mode = request.query_params.get("test")
    test_mode = True if str(test_mode).lower() == "true" else False
    # 3. Fetch agent from database
    res = supabase.from_("agents").select("*").eq("user_id", user_id).eq("agent_name", agent_name).execute()
    if res.error or not res.data:
        raise HTTPException(status_code=404, detail="Agent not found.")
    agent_record = res.data[0]
    agent_code = agent_record.get("agent_config")
    # 4. Execute the agent code
    try:
        output = execute_agent_code(user_id, agent_name, agent_code, test_mode)
    except Exception as e:
        # Log the exception e for debugging
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")
    # 5. Return the result
    return {"result": output, "test": test_mode}
```  

Explanation:  
   - **Authorization**: We ensure the `user_id` from the URL matches the authenticated user. This prevents one user from running another’s agent. If they don’t match, respond 403.  
   - **Test Mode Detection**: We retrieve the `test` query parameter. Here, instead of letting FastAPI handle it as a bool parameter (which it could, by using `test: bool = False` in the function signature), we manually parse it from `Request` for demonstration. If the string is "true" (case-insensitive), we set `test_mode = True`. Otherwise False. (Using FastAPI’s automatic query param is simpler: you can just have `test: bool = False` in the function signature and omit the manual parsing – FastAPI will do the conversion ([Query Parameters - FastAPI](https://fastapi.tiangolo.com/tutorial/query-params/#:~:text=%40app.get%28,skip%20%3A%20skip%20%2B%20limit)).)  
   - **Fetch Agent**: Query Supabase for the specific agent. We expect either an empty result (if not found) or one record. If not found or any error in query, return 404. The agent’s config (code) is extracted.  
   - **Execute Agent Code**: We call a helper function `execute_agent_code(user_id, agent_name, code, test_mode)`. This function you must implement. It handles the actual running of the agent logic in a safe way. Implementation strategies:  
     - *In-Memory:* `execute_agent_code` can use `exec` on the `code` string within a limited namespace and then call a known function name. For example, if you enforce that generated code always has a function `agent_main()` defined, do:  
       ```python
       def execute_agent_code(uid, name, code, test):
           # maybe use a global cache: if (uid,name) code was loaded before, reuse it
           ns = {"__name__": "__agent__"}
           # Provide a test flag in the namespace
           ns["TEST_MODE"] = test
           exec(code, ns)
           if "agent_main" in ns:
               return ns["agent_main"]()
           else:
               raise RuntimeError("No entry function found in agent code.")
       ```  
       You might want to add further restrictions to `ns` to prevent dangerous builtins (see Security doc).  
     - *File-Based:* If you created a file when the agent was added (via `load_agent_to_runtime`), you can import and run it:  
       ```python
       def execute_agent_code(uid, name, code, test):
           module_name = f"agents.{uid}_{name}"
           spec = importlib.util.spec_from_file_location(module_name, f"agents/{uid}_{name}.py")
           module = importlib.util.module_from_spec(spec)
           spec.loader.exec_module(module)
           # Now module has whatever was in the file
           if hasattr(module, "run"):
               # Optionally set a test flag in module
               module.TEST_MODE = test
               return module.run()
           elif hasattr(module, "agent_main"):
               module.TEST_MODE = test
               return module.agent_main()
           else:
               raise RuntimeError("No runnable function in agent module.")
       ```  
       This approach writes the file and loads it fresh on each execution (ensuring the latest code is run). Alternatively, you could import once and cache the module.  
   - **Handle exceptions**: Wrap the execution in try/except. Any error (syntax error in code, runtime error, etc.) will throw an exception. We catch it and return a 500 error to the user, including a message (in practice, avoid sending the raw error in detail in production, but it’s useful for debugging in dev).  
   - **Return output**: Returns a JSON with the result. We include the `test` flag for clarity. If the output is not JSON serializable by default, FastAPI will error. Common outputs like dicts, lists, strings, numbers are fine. If the agent returns a custom object, convert it (e.g., via `jsonable_encoder` or by adjusting the agent to return primitives).

**Testing**: After implementing, test with a simple agent. For example, create an agent with config `def agent_main(): return "hello"`. Then call `GET /agents/{user_id}/<that_agent_name>` and see if you get `"result": "hello"`. Also test `?test=true` to ensure it’s handled.

*AI Tip:* *Leverage AI assistance for writing `execute_agent_code`. For instance, you can prompt ChatGPT with: “How to safely exec a Python function from a string?” or ask Copilot by writing the signature and a comment `# Execute the agent code safely`. These tools might suggest using `exec` or even `ast` parsing. Use their suggestions as a starting point, but you must incorporate safety measures from the Security doc.*

## 6. Authentication (get_current_user Dependency)  
If your application uses authentication tokens, you need to implement `get_current_user`. This function could decode a JWT from the `Authorization` header and verify it (using Supabase’s JWT secret). Alternatively, if not using JWT, you might accept an API key or session. For the scope of this documentation:  
- If Supabase Auth is used, the easiest method in a secure environment is to use the Supabase client’s auth. However, since we’re building a custom API, you might manually decode.  
- A placeholder approach: require a header `X-User-ID` for simplicity in testing. (Not secure, but useful for initial development.) Then `get_current_user` just reads that header and returns it.  

Example placeholder:  
```python
from fastapi import Header

def get_current_user(user_id: str = Header(...)):
    # In production, replace this with proper JWT verification
    return user_id
```  
This will require every request to include `X-User-ID` header (Supabase Auth user id). Again, for real security, integrate a JWT check using PyJWT and Supabase’s public key. 

Make sure to update `current_user: str = Depends(get_current_user)` in each endpoint if you adjust how it works.

## 7. Using AI to Generate Agent Code (Optional)  
Implement `generate_agent_code(description: str) -> str` if you plan to support AI-based code generation. Initially, you can stub it as:  
```python
def generate_agent_code(description: str) -> str:
    # For now, just return a simple default function using the description.
    code = f"""
def agent_main():
    # This agent was generated from description: {description!r}
    return "Agent says: Hello, this is a placeholder for {description}"
"""
    return code
```  
This creates a trivial function. Later, if integrating with an AI API (like OpenAI), you’d call the API here, passing the description and perhaps expecting Python code in return. Ensure to sanitize and test the returned code.

Document how to use an AI tool in **Agent_Creation_Process.md** (the user of the system might type a description and rely on this, but as the developer, you could also manually use GPT to help write complex agent code and paste it into `agent_config`).

## 8. Final Steps and Testing  
With all endpoints implemented, run the application and test the full flow:  
- **Create Agent**: `POST /agents` with sample data. Check the response is 201 and the data is in the database (via Supabase dashboard or a GET call).  
- **List Agents**: `GET /agents` and see that it returns the newly created agent.  
- **Execute Agent**: `GET /agents/{user_id}/{agent_name}` for the created agent. Verify the logic runs and returns expected output. Try with `?test=true` and see if it affects the result (if you built any differentiation).  
- **Edge Cases**: Try creating a duplicate agent name, missing fields, or executing an agent that doesn’t exist to see error handling.  

Iterate on the implementation if any issues arise (for example, syntax errors in the dynamic exec, missing imports, etc.). Logging within your functions will help debug.

## 9. Repository Structure and File Organization  
After implementation, your project structure might look like:  
```
hello_world_agent/
├─ app/
│   ├─ main.py           # FastAPI app with new endpoints
│   ├─ models.py         # Pydantic models
│   ├─ ... (other app code)
├─ db/
│   ├─ supabase.py       # Supabase client initialization
├─ agents/
│   ├─ __init__.py
│   ├─ (dynamically created .py files for agents, if file-based approach)
├─ config.py             # Contains SUPABASE_URL, SUPABASE_KEY
├─ docs/                 # Documentation files
└─ ...
```  
Make sure to create an `agents/` directory and add an `__init__.py` if using file-based agent modules so it’s recognized as a package for imports.

## 10. Commit and Document  
Update the README.md (provided above) with any additional setup notes. Ensure all new dependencies (like `supabase`) are added to your `requirements.txt` or `Pipfile`. Include the documentation (the files we’re writing now) in the repository under `docs/` for future developers. 

With the above steps, the base `hello_world_agent` repository is now extended to support user-created custom agents. Use **Testing_and_Validation.md** next to verify everything under various scenarios, and refer to **Security_Considerations.md** to review and tighten any security aspects before deploying.
# fastapi-agent
A FastAPI-based dynamic agent system that leverages the ReACT methodology for building autonomous and human-in-the-loop agents.

## Original Gist:
https://gist.github.com/bar181/7fc0286841a38c72848ed037d0e561fd
Author: Bradley Ross (bar181 on gists and github)

**docs/README.md**

# Custom Agent System – Overview and Setup

## Introduction  
This project extends the base **hello_world_agent** FastAPI application into a custom agent system. Users can create personal AI agents, store their configurations in Supabase, and invoke them dynamically via HTTP requests. The system leverages **FastAPI** for building API endpoints and **Supabase** (PostgreSQL) for persistent storage and authentication. By following this documentation, a developer can clone the base repository and integrate new features to support multiple custom agents per user.

## Features  
- **Dynamic Agent Creation** – Create new agents via a FastAPI **POST** endpoint. Agents are defined by a name, description, and configuration (which can include code or settings).  
- **Supabase Integration** – Persist agent definitions (user ID, agent name, config, description) in a Supabase database for durability and queryability.  
- **Agent Query & Execution** – Retrieve agent details or execute an agent’s logic via **GET** requests. The system uses dynamic URL paths to route requests to the correct agent.  
- **In-Memory or File-Based Agents** – Choose between running agent logic from memory (directly from the database) or generating a Python file for each agent. Both approaches are supported and documented.  
- **Test Mode** – Use an optional `?test=true` query parameter on agent execution endpoints to run agents in a test/dry-run mode without side effects.  
- **Security and Auth** – Ensure that only authorized users can create or run their agents. Supabase’s authentication and Row-Level Security (RLS) policies help enforce data isolation.

## Setup Instructions  
1. **Clone the Repository** – Begin by cloning the base repository (e.g., via `git clone <repo_url>`). Navigate into the project directory.  
2. **Python Environment** – Create a virtual environment and install dependencies:  
   ```bash
   pip install fastapi uvicorn supabase
   ```  
   Ensure FastAPI and the Supabase Python client (`supabase-py`) are installed ([Building a CRUD API with FastAPI and Supabase: A Step-by-Step Guide](https://blog.theinfosecguy.xyz/building-a-crud-api-with-fastapi-and-supabase-a-step-by-step-guide#:~:text=mkdir%20fastapi,bcrypt%20supabase)) ([Python: Initializing | Supabase Docs](https://supabase.com/docs/reference/python/initializing#:~:text=import%20os%20from%20supabase%20import,create_client%2C%20Client)).  
3. **Supabase Project** – Create a Supabase project (via the Supabase web console) if you haven’t already. In the project settings under “API”, find your **Supabase URL** and **API (anon) key** ([Building a CRUD API with FastAPI and Supabase: A Step-by-Step Guide](https://blog.theinfosecguy.xyz/building-a-crud-api-with-fastapi-and-supabase-a-step-by-step-guide#:~:text=To%20integrate%20Supabase%20with%20Python%2C,Supabase%20from%20the%20Supabase%20dashboard)). These will be used for database connectivity.  
4. **Environment Variables** – Define environment variables for Supabase credentials. For example, create a `.env` file (or use your OS environment) with:  
   ```env
   SUPABASE_URL=<your-supabase-project-url>
   SUPABASE_KEY=<your-supabase-api-key>
   ```  
   **Note:** Use the **anon** key for client-level access (enforces RLS), or a **service role** key for server-side access (with caution – service role bypasses security policies ([Authorization via Row Level Security | Supabase Features](https://supabase.com/features/row-level-security#:~:text=4,bypassrls%20privilege%20for%20administrative%20tasks))). Never expose the service role key publicly.  
5. **Supabase Database Setup** – Using Supabase’s dashboard or SQL editor, create a table named `agents` with the following structure:  
   - `id`: Primary key (UUID or serial).  
   - `user_id`: UUID or text, references the user (e.g., Supabase Auth user ID).  
   - `agent_name`: text or varchar, the unique name of the agent (unique per user).  
   - `agent_config`: text or json, stores the agent’s configuration or code.  
   - `description`: text, a human-readable description of the agent.  
   Enable Row Level Security on this table and create a policy to ensure users can only access their own rows (for example, using `auth.uid() = user_id` in the policy ([Row Level Security | Supabase Docs](https://supabase.com/docs/guides/database/postgres/row-level-security#:~:text=create%20policy%20,their%20own%20todos))). More details in **docs/Security_Considerations.md**.  
6. **Run the Application** – Start the FastAPI server (e.g., with Uvicorn):  
   ```bash
   uvicorn app.main:app --reload
   ```  
   (Adjust the module path if your main application file is in a different location.) The server should start at `http://127.0.0.1:8000`. Use the `--reload` flag for auto-reloading during development.  
7. **Verify Base Endpoint** – The base repository may have a simple endpoint (e.g., GET `/` returning “Hello World”). Confirm it still works by visiting `http://127.0.0.1:8000/` in your browser or via curl. You should see a JSON greeting or similar.  

## Documentation Guide  
The project documentation is organized in the `docs/` directory as follows:  

- **Architecture.md** – Detailed explanation of the system’s structure and data flow.  
- **Technical_Specifications.md** – Precise specifications of API endpoints, data models, and database schema.  
- **Implementation_Guide.md** – Step-by-step instructions to implement the new features into the base project, with code snippets and pseudocode.  
- **Supabase_Integration.md** – Guidance on setting up Supabase, connecting from FastAPI, and performing database operations.  
- **Agent_Creation_Process.md** – Explanation of how agents are created and managed, including in-memory vs. file-based approaches and how to leverage AI tools to generate agent code.  
- **Testing_and_Validation.md** – Instructions for testing the system’s functionality, including manual testing (with example requests) and writing automated tests.  
- **Security_Considerations.md** – Important security aspects like authentication, authorization, and safe execution of agent code.  

Developers should read **Architecture.md** first to understand the high-level design, then refer to **Technical_Specifications.md** and **Implementation_Guide.md** when integrating the features. Use **Testing_and_Validation.md** to verify everything works as expected. Each document contains clear explanations, example code, and tips (including using AI assistance where helpful) to ease the development process.

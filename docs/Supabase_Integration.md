**docs/Supabase_Integration.md**

# Supabase Integration Guide

Supabase is used in this project as the database and user management backend. This guide explains how to set up Supabase for the custom agent system and how to perform common database operations from the FastAPI app.

## Setting Up Supabase Project  
1. **Create a Supabase Account**: If you don’t have one, sign up at [supabase.com](https://supabase.com) and start a new project. The free tier is sufficient for development.  
2. **Project Configuration**: In your Supabase project dashboard, go to **Settings -> API**. Note down the **API URL** and the **anon public key** (and the service role key if needed). These will be used by your application to connect to the database ([Building a CRUD API with FastAPI and Supabase: A Step-by-Step Guide](https://blog.theinfosecguy.xyz/building-a-crud-api-with-fastapi-and-supabase-a-step-by-step-guide#:~:text=To%20integrate%20Supabase%20with%20Python%2C,Supabase%20from%20the%20Supabase%20dashboard)).  
3. **Database Table - Agents**: Navigate to the **Table Editor** and create a new table called `agents` (in the public schema). Add the columns as described in Technical Specifications:  
   - `id`: UUID (primary key, default `gen_random_uuid()` in Supabase).  
   - `user_id`: UUID (or text) – you can set this as a text if you prefer, but UUID type aligning with Supabase Auth user IDs is ideal. Not null.  
   - `agent_name`: text – not null. You may set a uniqueness constraint on combination of `user_id` and `agent_name`.  
   - `description`: text – not null (or allow null if you want description optional).  
   - `agent_config`: text – not null (this can be very long if storing code; Postgres `text` can handle large sizes).  
   - (Optional timestamps `created_at` and `updated_at` with default now()).  
4. **Enable Row Level Security (RLS)**: In the Table Editor’s Security settings, toggle RLS to **Enabled** for `agents`. Initially, without any policies, this means no one (except service role) can access the data – we will add policies next.  
5. **Add Policies**: Add at least a SELECT and an INSERT policy for the `agents` table:  
   - Select Policy: **Using expression:** `(auth.uid() = user_id)` – This means a Supabase authenticated user can select rows where the `user_id` matches their own UID ([Row Level Security | Supabase Docs](https://supabase.com/docs/guides/database/postgres/row-level-security#:~:text=create%20policy%20,their%20own%20todos)).  
   - Insert Policy: **Check expression:** `(auth.uid() = user_id)` – This ensures that when inserting, the `user_id` field must match the UID of the authenticated user (preventing one from creating an agent for someone else).  
   - You may also add UPDATE/DELETE policies similarly if you plan to allow editing or deleting agents via the API.  
   - In Supabase UI, you can use the simple policy templates or the SQL editor to write these. The result should be something like:  
     ```sql
     create policy "Allow insert own agent" on public.agents
       for insert with check (auth.uid() = user_id);
     create policy "Allow select own agents" on public.agents
       for select using (auth.uid() = user_id);
     ```  
6. **Testing RLS**: Supabase provides a “Test out policies” feature where you can simulate a user’s token to see if they can access the data. Use a user’s ID to test selecting their agent row vs. another’s. With the above, each user should only see their data.

## Connecting FastAPI to Supabase  
Your FastAPI app will interact with Supabase through the `supabase-py` library. The connection requires the URL and an API key.

- **Supabase URL**: Looks like `https://xyzcompany.supabase.co` (unique to your project).  
- **Supabase Key**: There are two primary keys provided: the anon public key (meant for client-side, enforces RLS) and the service role key (full access, bypasses RLS). Decide which to use:  
  - For a backend server, you might use the service role key to allow full DB access, but then implement all security in your code. **Use this carefully**, as it can override RLS ([Authorization via Row Level Security | Supabase Features](https://supabase.com/features/row-level-security#:~:text=4,bypassrls%20privilege%20for%20administrative%20tasks)).  
  - Alternatively, use the anon key and pass the user’s JWT on each request to Supabase so that RLS policies apply. The supabase-py library supports user authentication tokens if you use the `auth` features (not covered fully here).  
- For simplicity, the code examples used the service role key and did manual checks in the API. In a real deployment, a more secure pattern is to use the anon key with RLS or use the service key but restrict operations.

**Initializing the client:** (Recap from Implementation Guide)  
In `db/supabase.py`:  
```python
from supabase import create_client, Client
import os

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
```  
This will create a global `supabase` client object. You can import this in your route handlers to query the DB. Under the hood, `create_client` sets up a REST client pointed at your Supabase instance ([Python: Initializing | Supabase Docs](https://supabase.com/docs/reference/python/initializing#:~:text=import%20os%20from%20supabase%20import,create_client%2C%20Client)).

Make sure `SUPABASE_URL` and `SUPABASE_KEY` are set in your environment or via a config file. Never commit keys to source control. Use environment variable management in your deployment.

## Database Operations with supabase-py  
The supabase-py client provides an ORM-like interface for CRUD operations. Here are common operations used in this project:

- **Insert**: Adding a new record.  
  Example:  
  ```python
  data = {"user_id": uid, "agent_name": name, "description": desc, "agent_config": cfg}
  res = supabase.from_("agents").insert(data).execute()
  ```  
  This returns an object; `res.data` will contain the inserted rows (if successful) and `res.error` any error. You can insert a single dict or a list of dicts.  

- **Select**: Querying data.  
  Example:  
  ```python
  res = supabase.from_("agents").select("*").eq("user_id", uid).execute()
  rows = res.data  # list of records matching the query
  ```  
  The `eq` method adds a filter condition (column equals value). You can chain filters and other query modifiers (like `.single()` if expecting one result, or `.select("id, name")` to specify columns).  
  To get a specific agent:  
  ```python
  res = supabase.from_("agents").select("*").match({"user_id": uid, "agent_name": name}).execute()
  ```  
  `.match` is a shorthand to filter by multiple columns.  

- **Update**: Modifying data (not heavily used in our current scope, but for completeness).  
  Example:  
  ```python
  res = supabase.from_("agents").update({"description": "New desc"}).eq("id", agent_id).execute()
  ```  
  This will update the `description` of the agent with given id. Similar filtering as select.

- **Delete**: Removing records (also not used here unless you add an endpoint to delete an agent).  
  Example:  
  ```python
  res = supabase.from_("agents").delete().eq("id", agent_id).execute()
  ```  

Each of these returns a response with possibly `data` and `count`. Check `res.error` to see if the operation failed. If `res.error` is not None, log or handle it.  

**Important**: When using the service key, the operations will bypass RLS. So if you accidentally query without a `.eq("user_id", ...)` filter, you might get all agents in the database. Always include user scoping in your queries (or use RLS with anon key to enforce it automatically).

## Supabase Auth and JWT integration (Optional Advanced)  
If you want to fully integrate Supabase Auth:  
- The user would log in via Supabase (maybe through a separate front-end or hitting Supabase auth endpoints). They’d receive a JWT.  
- That JWT should be sent with each request to your FastAPI (in `Authorization: Bearer <token>`).  
- In FastAPI, you’d decode that token. Supabase JWTs are signed with your Supabase project’s secret (available in settings). They also embed the `sub` (subject) claim which is the user’s UUID.  
- You can decode JWT using PyJWT or any JWT library, verify the signature with the secret, and extract the user ID. Then that becomes `current_user`.  
- The supabase-py library can also be used to sign in and get a session, but since we’re focusing on custom endpoints, manual decode is fine.

For development/testing, as noted, you might skip actual JWT and use a fake header. But be sure to secure this before production.

## Example: End-to-End Request with Supabase  
Suppose a client wants to create a new agent. Here’s what happens with Supabase involved:

- **Client** (`POST /agents` with JSON) -> **FastAPI** (Python code) -> **Supabase** (HTTP call to DB).  
- The FastAPI handler calls `supabase.from_("agents").insert({...}).execute()`.  
- This triggers an HTTP request from the supabase-py client to the Supabase REST endpoint: `POST https://<PROJECT>.supabase.co/rest/v1/agents` with the JSON body and an `apikey` header (plus `Authorization` header if using a user JWT).  
- Supabase receives it. If using anon key, it treats it as a user request (and expects a JWT for auth; the anon key just identifies the project). If using service key, it goes as admin.  
- Supabase applies RLS policies: in case of anon+JWT, it checks the insert policy `(auth.uid() = user_id)`. Our code provided `user_id` in the data and the JWT has the same UID, so the insert is allowed.  
- The record is created in the database. Supabase returns the inserted record in the response.  
- The supabase-py client populates `res.data` with that record. FastAPI then continues to return a result to the client.

All of this happens seamlessly through the supabase-py library. We as developers just wrote a few lines of Python to make it happen, thanks to the client’s abstraction. The real power is in configuring Supabase correctly (RLS, etc.) so that minimal checks are needed in code.

## Supabase CLI and Local Development (Optional)  
Supabase offers a CLI tool and the ability to run Supabase locally via Docker. If you prefer not to use a cloud instance for dev/testing, you can:  
- Install the Supabase CLI, run `supabase init` in your project, and `supabase start` to launch a local Postgres with the Supabase platform (Auth, Storage, etc.).  
- The URL will be `http://localhost:54321` for API and you’ll have a local anon/service key in the config.  
- The setup steps (creating table, policies) can then be done via the CLI or by connecting to the local database.  
- Your FastAPI would point to the local URL and key for testing.  
- This can speed up development and avoid accidentally messing with production data.

## Troubleshooting  
- **Invalid API Key**: If you get errors connecting, double-check that you used the correct URL and key. The URL should include the unique project ref (the subdomain) and end with `.supabase.co`. The key should correspond to that project (and correct role).  
- **RLS Denies**: If using anon key without JWT or with a wrong JWT, Supabase will return an error or just no data due to RLS. Ensure a valid token is present if required. If using service key but forgot to enable RLS or policies, you might inadvertently allow all data – double-check using the right key.  
- **Supabase downtime or latency**: In rare cases, the Supabase service might be slow or down; your API should handle exceptions from supabase-py gracefully (catch exceptions or check `res.error`). Implement retries or fallback logic if needed for robust production use.  
- **Data encoding issues**: If `agent_config` is large or contains special characters (like quotes, newlines), ensure they are properly escaped in JSON. The supabase client will handle JSON serialization. If you run into issues storing extremely large text, consider Supabase Storage (to store a file) or chunking the data.

By following this guide, you should have Supabase properly wired up with your FastAPI app, providing a secure and scalable persistence layer for the agent system. Continue with **Agent_Creation_Process.md** for details on how agent definitions are handled, or jump to **Testing_and_Validation.md** to verify the integration.

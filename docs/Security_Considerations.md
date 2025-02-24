**docs/Security_Considerations.md**

# Security Considerations

Security is critical for a system that executes user-provided code and manages multi-user data. This document highlights potential risks and how to mitigate them, covering authentication, authorization, and safe code execution.

## Authentication & Authorization  
**Authentication** verifies the identity of the user calling the API, while **authorization** ensures they have access to the resources (agents) they’re requesting.

- **Use JWTs or API Keys**: It’s recommended to use Supabase Auth JWTs for authentication. Each request should include an `Authorization: Bearer <token>` header. The FastAPI app should decode this token (using the project’s JWT secret or JWKS). The token contains the user’s UUID (`sub` claim). By trusting this token, you avoid having to pass `user_id` in the URL at all – the server can infer it. In our design, we included `user_id` in the path for clarity, but you might simplify to `/agents/{agent_name}` and always use the authenticated user’s ID internally.  
- **Current User Dependency**: Ensure the `get_current_user` dependency checks the token properly. If token is missing or invalid, raise `HTTPException(status_code=401)`. If token is valid, extract `user_id`. Use that for DB queries and to compare with any `user_id` path param (if present).  
- **Authorization**: The system should verify that a user can only create, list, or execute their own agents. We did this by checking `if user_id != current_user` in the execution endpoint. Similar checks (or design choices) should be applied to any future endpoints (like delete or update agent). Even on the list endpoint, even though the DB query filters by user_id, it’s wise to require auth so someone can’t just omit auth and get an empty list (which might not be a big issue, but consistency matters).  
- **Supabase RLS**: Rely on Row-Level Security as a safety net. With RLS policies like `(auth.uid() = user_id)` ([Row Level Security | Supabase Docs](https://supabase.com/docs/guides/database/postgres/row-level-security#:~:text=create%20policy%20,their%20own%20todos)), even if someone tried to bypass your API and hit Supabase directly with an anon key and a crafted JWT, they would only see their data. RLS also protects if you accidentally make a query without a filter. For example, if a bug in code did `supabase.from_("agents").select("*").execute()` with an anon key + JWT, RLS would restrict it to the user’s rows. Without RLS (or with service key), that would expose all data. So enabling RLS and using anon key where possible is highly recommended in production.  
- **Service Role Key Security**: If you use the service role key in your backend, treat it like a password. Do not expose it to the client-side. Ensure your repository does not contain it (use environment variables). The service key can bypass RLS ([Authorization via Row Level Security | Supabase Features](https://supabase.com/features/row-level-security#:~:text=4,bypassrls%20privilege%20for%20administrative%20tasks)), so your backend must enforce all checks. Ideally, the backend should never perform an action on behalf of a user without checking their rights. For instance, never blindly return `supabase.from_("agents").select("*")` with service key and trust the client to filter – always filter in the query for user-specific data.

## Secure Code Execution  
The most unique risk here is executing user-defined code. If an attacker can create an agent and put malicious code in `agent_config`, that code will run on your server with potentially full privileges. This is essentially remote code execution as a service – very dangerous if not controlled. Here’s how to mitigate:

- **Sandboxing**: Ideally, run user code in a sandboxed environment. In Python, true sandboxing is non-trivial. Some approaches:  
  - Use OS-level sandboxing: e.g., run the code in a separate process with restricted permissions (maybe inside a container, or as a certain user, or using something like `seccomp` or sandbox libraries). For example, spawn a subprocess that runs the agent code and kill it if it tries to do disallowed things or after a timeout. This could be heavy, but it separates memory and permissions.  
  - Use `exec` with a restricted globals dict: When using `exec`, pass in a minimal dictionary for globals. For example:  
    ```python
    safe_globals = {"__builtins__": {}}  # no builtins
    exec(user_code, safe_globals)
    ```  
    This prevents use of dangerous builtins like `__import__`, `open`, etc. You can selectively allow some safe functions if needed. However, completely removing builtins means even basic things like `len()` or `range()` won’t be available unless you allow them. You could manually inject safe ones. This is a form of soft sandboxing. Be aware that creative attackers might break out (there are known tricks to get access to builtins through other Python loopholes).  
  - Limit libraries and attributes: If you allow imports, someone could import `os` and do harm. In the safe_globals, we set `__builtins__` to an empty dict to disallow all builtins and imports. If the agent needs to import something, consider pre-specifying allowed modules (like math) and provide them in the globals.  
  - Use timeouts: If an agent code goes into an infinite loop, it could hang your server worker. Use asyncio timeout or threading to enforce a max execution time. For example, run the agent function in a thread and join with timeout, or if using asyncio, use `asyncio.wait_for`. Uvicorn worker timeouts might help at request level too.  
- **File System Access**: If using file-based, ensure the directory for agents has proper permissions. Agents should not be able to read or write arbitrary files on the server. If an agent code tries `open('/etc/passwd').read()`, by default Python would allow it. With no sandbox, that’s a serious problem. Removing builtins avoids direct open, but an agent could still call some allowed library that does file operations. Consider chrooting or working in a container. This is complex; for many use cases, it might be acceptable to say “only trusted users can deploy code” – but if this is public-facing, you need a sandbox.  
- **Resource Limits**: An agent could try to use a lot of memory or CPU (e.g., create huge objects or do heavy computation). This could affect your server’s performance. Monitor or limit resources where possible. Python doesn’t have easy memory limits per thread, but running each agent in a separate process might allow using OS limits (ulimit or cgroups).  

Given the complexity, you might at least start with the `exec` in restricted globals approach and document that the system is not secure against malicious code, advising that it’s for trusted scenarios or behind an approval process.

## Input Validation  
While Pydantic covers basic request validation, consider additional checks:  
- **agent_name**: enforce a pattern (regex) to avoid special characters. This prevents odd cases like an agent name with “../” which in a file system context could be exploited. E.g., allow only alphanumeric and underscores.  
- **description**: not so critical, but you might limit length to prevent someone from sending extremely large descriptions (though our system can handle fairly large text).  
- **agent_config**: if you allow users to directly provide code, you might want to scan it for obvious bad patterns. For example, you could disallow the string “import os” or “__” (dunder methods) as a simple heuristic. This is not foolproof, but it raises the bar for an attacker. Conversely, if using AI generation, your AI might inadvertently include such things – so maybe you trust your generator more than arbitrary user code. Decide whether direct user-supplied code is allowed or if only AI/back-end can produce code from descriptions (which you can try to constrain).

## Supabase Security (Additional)  
- **Ensure HTTPS**: When your FastAPI communicates with Supabase, use the HTTPS URL (which it does by default). Keep your Supabase keys secret (already emphasized).  
- **Least Privilege**: If possible, use the anon key in your app for most operations with user JWTs. Only use the service key for administrative tasks (like if you had an admin endpoint to view all agents or to bypass RLS intentionally). By using anon + JWT, you ensure that even if your app had a bug, the exposure is limited by RLS.  
- **Rate Limiting**: Consider rate limiting the endpoints to prevent abuse (especially the execution endpoint, to avoid someone spamming heavy computations). You can use libraries like `slowapi` or a proxy (like API Gateway or Nginx) to rate limit by IP or user. Supabase itself has some rate limiting on API keys, but better to enforce on your side for execution.  
- **Monitoring and Logging**: Log important security-related events: agent creation (with user and name), execution (with user and agent, maybe truncated output or runtime). This can help detect misuse. For example, if you see a user created an agent with suspicious code (you might log the first 100 chars of agent_config), you can investigate. Or if an execution error occurs, log the stack trace securely. Ensure logs themselves don’t leak sensitive info inadvertently (like don’t log full Supabase keys or full user code if not needed).

## Permissions for Supabase Table  
- If using service key, the `agents` table should ideally only be accessible via your backend. Supabase’s default API will allow the anon key to do operations if RLS permits. That’s fine and intended. If you accidentally leaked the service key, someone could do anything to your DB.  
- You could tighten Supabase by restricting the anon key’s access further (like only allow certain RPC functions or something), but generally RLS is enough if configured.  
- Consider using Supabase’s `postgrest` settings to allow only certain columns. For example, you might mark `agent_config` as unavailable to the anon role if you didn’t want it to be queryable from the client directly. Since our design uses a backend, this is less of an issue.

## Testing Security  
Write tests or perform actions to confirm security measures:  
- Try to create an agent with forbidden characters in the name (should be rejected).  
- Try code injection in description to see if any part of your system mistakenly executes it (it shouldn’t).  
- If possible, deliberately create a malicious `agent_config` in a controlled environment to see what damage it could do and if your restrictions stop it. For instance, try `import os` under the restricted `exec` and see if it fails (expected, if no builtins). Try referencing `__builtins__` in the user code, etc. There are known exploit attempts for Python sandboxing – consider researching those if this is a high-stakes application.  
- Confirm that without valid auth, nothing can be done (e.g., using curl without token yields 401 on protected endpoints).  
- Confirm RLS: try using the Supabase REST API directly with anon key and a JWT of user A to get user B’s agent (simulate by crafting JWT or using the testing feature). It should deny access.

## Summary and Recommendations  
- Always authenticate and authorize every request. Never trust client-supplied identifiers for sensitive operations without verification.  
- Treat user-supplied code as hostile. Sandbox as much as possible. If full sandboxing isn’t feasible, you might need to limit this feature to trusted users or specific safe languages (an alternative approach could be to have a domain-specific language for agents rather than raw Python).  
- Keep secrets (keys, tokens) out of the wrong hands. Use HTTPS everywhere.  
- Use Supabase’s security features (Auth and RLS) to complement your application security – defense in depth ([Row Level Security | Supabase Docs](https://supabase.com/docs/guides/database/postgres/row-level-security#:~:text=RLS%20is%20incredibly%20powerful%20and,the%20browser%20to%20the%20database)).  
- If this system evolves (say, adding the ability for agents to call external APIs or access user data), revisit security often to handle new threats (like API key management, data privacy concerns, etc.).  

By implementing the above measures, you can significantly mitigate risks associated with dynamic code execution and multi-user data access, making the custom agent platform safer for deployment. Always err on the side of caution: if unsure about allowing something (like a particular operation in agent code), disallow it or log and monitor it.
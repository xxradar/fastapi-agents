## Summary of Changes

This log summarizes the changes made to fix deprecation warnings and a syntax error in the project, as well as refactoring the agent routes and agent information.

### `starter/agents/math.py`

-   Replaced `ast.Num` with `ast.Constant` and `node.n` with `node.value` to address a deprecation warning related to the `ast` module.

### `starter/agents/time.py`

-   Replaced the original content with the updated code provided by the user, which fixed an `AttributeError` and addressed a deprecation warning related to the `datetime` module. The `datetime.datetime.utcnow()` was replaced with `datetime.now(UTC)`.

### Code Refactoring

-   Created a new file `starter/app/agent_routes.py` to handle all agent-related routes
-   Created a new file `starter/app/agents_info.py` to store agent information
-   Updated `starter/app/main.py` to import and use these new modules
-   Updated `starter/README.md` to reflect the new project structure
-   Updated the test to match the welcome message

This refactoring improves the code organization with a cleaner separation of concerns:
- `main.py` focuses on core application setup and basic routes
- `agent_routes.py` handles all agent-specific routes
- `agents_info.py` stores agent metadata

The modular structure makes the codebase more maintainable and easier to extend in the future.
## Summary of Changes

This log summarizes the changes made to fix deprecation warnings and a syntax error in the project.

### `starter/agents/math.py`

-   Replaced `ast.Num` with `ast.Constant` and `node.n` with `node.value` to address a deprecation warning related to the `ast` module.

### `starter/agents/time.py`

-   Replaced the original content with the updated code provided by the user, which fixed an `AttributeError` and addressed a deprecation warning related to the `datetime` module. The `datetime.datetime.utcnow()` was replaced with `datetime.now(UTC)`.
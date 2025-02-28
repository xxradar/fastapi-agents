import ast
import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, Query, Body

logging.basicConfig(level=logging.DEBUG)

# Global variable expected to be set externally.
# Example: EXPRESSION = "3 + 4 * 2"
try:
    EXPRESSION
except NameError:
    EXPRESSION = None

def safe_arithmetic_eval(expr: str) -> float:
    """
    Safely evaluate an arithmetic expression using Python's AST.
    Disallows attributes, function calls, or unknown operators.
    """
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    valid_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Load,
        ast.Constant,  # For Python 3.8+, numeric literals appear as Constants
        ast.operator  # Include operator type in valid nodes
    )
    valid_ops = (
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
        ast.FloorDiv
    )

    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and not isinstance(node.op, valid_ops):
            raise ValueError(f"Operator not allowed: {type(node.op).__name__}")
        elif not isinstance(node, valid_nodes):
            raise ValueError(f"Node not allowed: {type(node).__name__}")

    compiled = compile(tree, filename="<safe_arithmetic_eval>", mode="eval")
    return eval(compiled, {"__builtins__": {}})

def agent_main():
    """
    Context-Aware Calculator Agent
    --------------------------------
    Purpose: Evaluate arithmetic expressions with context sharing via MCP.
    
    Usage:
      from agents import calculator
      calculator.EXPRESSION = "3 + 4 * 2"
      result = calculator.agent_main()
      # Expected output: {'result': 14, 'context': <MCP_updated_context>}
    """
    logging.debug("Calculator agent started")
    if not EXPRESSION:
        logging.debug("EXPRESSION is not set")
        return {"error": "EXPRESSION is not set."}

    processed_expression = EXPRESSION

    # Build initial context
    context = {
        "expression": processed_expression,
        "previous_result": None
    }

    # Update context via MCP
    try:
        logging.debug("Updating context")
        if 'mcp_adapter' not in globals():
            logging.error("MCP adapter not injected")
            # Continue without MCP functionality
            updated_context = context
        else:
            updated_context = mcp_adapter.send_context(context)
        logging.debug(f"Updated context: {updated_context}")
    except Exception as exc:
        logging.exception("Failed to update context")
        return {"error": f"Failed to update context: {str(exc)}"}

    # Safely evaluate the expression
    try:
        logging.debug("Evaluating expression")
        result = safe_arithmetic_eval(processed_expression)
        logging.debug(f"Result: {result}")
    except Exception as exc:
        logging.exception("Failed to evaluate expression")
        return {"error": f"Failed to evaluate expression: {str(exc)}"}

    return {"result": result, "context": updated_context}

def register_routes(router: APIRouter):
    """Registers the calculator agent's routes with the provided APIRouter."""

    @router.post("/agents/calculator", summary="Evaluates arithmetic expressions with context sharing", response_model=Dict[str, Any], tags=["MCP Agents"])
    async def calculator_route(payload: Dict[str, Any] = Body(..., examples={"Example": {"value": {"expression": "3 + 4 * 2"}}})):
        """
        Evaluates an arithmetic expression with context sharing via MCP.

        **Input:**

        *   **expression (required, string):** The arithmetic expression to evaluate. Example: 3 + 4 * 2

        **Process:** The expression is safely evaluated using Python's AST to prevent code injection.
        Context is shared and updated via MCP, allowing for state management between calls.

        **Example Input (JSON payload):**

        ```json
        {
          "expression": "3 + 4 * 2"
        }
        ```

        **Example Output:**

        ```json
        {
          "agent": "calculator",
          "result": {
            "result": 11,
            "context": {
              "expression": "3 + 4 * 2",
              "previous_result": null
            }
          }
        }
        ```

        **Example Output (if expression is invalid):**

        ```json
        {
          "agent": "calculator",
          "result": {
            "error": "Failed to evaluate expression: Invalid syntax: invalid syntax (line 1)"
          }
        }
        ```
        """
        global EXPRESSION
        EXPRESSION = payload.get("expression")
        
        # Inject the adapter so code references the same place that tests can patch
        global mcp_adapter
        from app.mcp_adapter import MCPAdapter
        mcp_adapter = MCPAdapter()
        
        output = agent_main()
        return {"agent": "calculator", "result": output}

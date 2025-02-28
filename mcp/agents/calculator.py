import ast
import logging

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

# Math Agent: Evaluates arithmetic expressions after token verification
# This agent demonstrates a more complex implementation with authorization and safe evaluation

import ast
import operator
from typing import Dict, Any, Union, Optional
from fastapi import APIRouter, Query

# Expected token for authorization
EXPECTED_TOKEN = "MATH_SECRET"

# Global variables for configuration
TOKEN = None  # User must set this before calling agent_main()
EXPRESSION = None  # User must set this to a valid arithmetic expression (e.g., "2+2")

# Supported operators for safe evaluation
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

class MathAgent:
    """
    Math Agent
    -----------
    Purpose: Evaluates arithmetic expressions after token verification.
    """
    
    def __init__(self):
        self.expected_token = EXPECTED_TOKEN
    
    def safe_eval(self, expr):
        """
        Safely evaluate a mathematical expression.
        Only allows basic arithmetic operations (+, -, *, /, **) and numbers.
        
        Args:
            expr (str): The mathematical expression to evaluate
            
        Returns:
            float: The result of the evaluation
            
        Raises:
            ValueError: If the expression contains unsupported operations
            SyntaxError: If the expression is not valid Python syntax
        """
        try:
            # Parse the expression into an AST
            tree = ast.parse(expr, mode='eval')
            
            def eval_node(node):
                """Recursively evaluate an AST node"""
                if isinstance(node, ast.Expression):
                    return eval_node(node.body)
                elif isinstance(node, ast.Num):
                    return node.n
                elif isinstance(node, ast.BinOp):
                    # Only allow supported arithmetic operations
                    if type(node.op) not in OPERATORS:
                        raise ValueError("Unsupported operator")
                    left = eval_node(node.left)
                    right = eval_node(node.right)
                    return OPERATORS[type(node.op)](left, right)
                else:
                    raise ValueError("Unsupported expression type")
                    
            return eval_node(tree)
        except (ValueError, SyntaxError, TypeError) as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def evaluate(self, token: Optional[str] = None, expression: Optional[str] = None) -> Dict[str, Any]:
        """
        Evaluates a mathematical expression after token verification.
        
        Args:
            token: The authorization token
            expression: The mathematical expression to evaluate
            
        Returns:
            A dictionary containing the result or an error message
        """
        # Use provided parameters or fall back to global variables
        token = token or TOKEN
        expression = expression or EXPRESSION
        
        # Check authorization
        if token != self.expected_token:
            return {"error": "Invalid token. Access denied."}
            
        # Validate expression
        if not isinstance(expression, str):
            return {"error": "Expression must be a string."}
        if not expression.strip():
            return {"error": "Expression cannot be empty."}
            
        # Evaluate expression
        try:
            result = self.safe_eval(expression)
            return {"result": result}
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Unexpected error during evaluation: {str(e)}"}

# Keep the original function for backward compatibility
def agent_main():
    """
    Original agent_main function for backward compatibility.
    """
    agent = MathAgent()
    result = agent.evaluate(TOKEN, EXPRESSION)
    
    # Convert the result to match the original format
    if "error" in result:
        return result["error"]
    else:
        return result["result"]

def register_routes(router: APIRouter):
    """Registers the math agent's routes with the provided APIRouter."""
    
    agent = MathAgent()
    
    @router.get("/math", summary="Evaluates a math expression after verifying a token", tags=["Agents with Validation"])
    async def math_route(
        token: str = Query(..., description="Authorization token (must be 'MATH_SECRET')"),
        expression: str = Query(..., description="Mathematical expression to evaluate")
    ):
        """
        Evaluates a mathematical expression after token verification.
        
        **Security:** This endpoint requires a valid token for authorization.
        
        **Input:**
        
        * **token (required):** Must be set to the correct value for authorization
        * **expression (required):** A valid arithmetic expression (e.g., "3 * (4 + 2)")
        
        **Process:** The expression is safely evaluated using AST parsing to prevent code injection.
        Only basic arithmetic operations (+, -, *, /, **) and numbers are allowed.
        
        **Example Input:**
        
        `?token=MATH_SECRET&expression=3*(4+2)`
        
        **Example Output:**
        
        ```json
        {
          "agent": "math",
          "result": {
            "result": 18
          }
        }
        ```
        
        **Example Error (invalid token):**
        
        ```json
        {
          "agent": "math",
          "result": {
            "error": "Invalid token. Access denied."
          }
        }
        ```
        """
        result = agent.evaluate(token, expression)
        return {"agent": "math", "result": result}
# Math Agent: Evaluates arithmetic expressions after token verification
# This agent demonstrates a more complex implementation with authorization and safe evaluation

import ast
import operator

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

def safe_eval(expr):
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
            elif isinstance(node, ast.Constant):
                return node.value
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

def agent_main():
    """
    Main function for the Math Agent.
    
    This agent requires proper authorization via a token and evaluates 
    mathematical expressions safely.
    
    Instructions for direct invocation:
    1. Set the global variable TOKEN to your token key:
       >>> from agents import math
       >>> math.TOKEN = "MATH_SECRET"
    
    2. Set the global variable EXPRESSION to the arithmetic expression:
       >>> math.EXPRESSION = "3 * (4 + 2)"
    
    3. Call agent_main() to execute:
       >>> result = math.agent_main()
       >>> print(result)  # Should output: 18
    
    Returns:
        Union[float, str]: The result of the evaluated expression if successful,
                          or an error message if authorization fails or evaluation errors occur.
    """
    # Check authorization
    if TOKEN != EXPECTED_TOKEN:
        return "Error: Invalid token. Access denied."
        
    # Validate expression
    if not isinstance(EXPRESSION, str):
        return "Error: Expression must be a string."
    if not EXPRESSION.strip():
        return "Error: Expression cannot be empty."
        
    # Evaluate expression
    try:
        result = safe_eval(EXPRESSION)
        return result
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error during evaluation: {str(e)}"
# agents/echo.py

def agent_main():
    """
    Echo Agent
    -----------
    Purpose: Returns a hard-coded echo message.
    
    Usage:
        # In a Python shell:
        from agents import echo
        result = echo.agent_main()
        print(result)  # Expected output: {'message': 'Echo from agent!'}
    """
    return {"message": "Echo from agent!"}
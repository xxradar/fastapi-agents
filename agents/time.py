# agents/time.py
from datetime import datetime

def agent_main():
    """
    Time Agent
    -----------
    Purpose: Returns the current time in ISO 8601 format.
    
    Usage:
        # In a Python shell:
        from agents import time
        result = time.agent_main()
        print(result)  # Example output: {'time': '2025-02-24T15:44:03Z'}
    """
    current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return {"time": current_time}
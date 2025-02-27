# agents/echo.py

from typing import Dict, Any
from fastapi import APIRouter

class EchoAgent:
    """
    Echo Agent
    -----------
    Purpose: Returns a hard-coded echo message.
    """
    
    def get_echo(self) -> Dict[str, str]:
        """Returns a hard-coded echo message."""
        return {"message": "Echo from agent!"}

# Keep the original function for backward compatibility
def agent_main():
    """
    Original agent_main function for backward compatibility.
    """
    agent = EchoAgent()
    return agent.get_echo()

def register_routes(router: APIRouter):
    """Registers the echo agent's routes with the provided APIRouter."""
    
    agent = EchoAgent()
    
    @router.get("/echo", summary="Returns an echo message", tags=["Simple Agents"])
    async def echo_route():
        """
        Returns a simple echo message.
        
        **Process:** An instance of the `EchoAgent` is used to generate the response.
        
        **Example Output:**
        
        ```json
        {
          "message": "Echo from agent!"
        }
        ```
        """
        return agent.get_echo()
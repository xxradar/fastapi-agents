# agents/joke.py
import random

# Collection of programming jokes
JOKES = [
    "Why did the programmer quit his job? Because he didn't get arrays!",
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the programmer go broke? Because he used up all his cache!",
    "What's a programmer's favorite hangout spot? The Foo Bar!",
    "Why do programmers always mix up Halloween and Christmas? Because Oct 31 equals Dec 25!",
    "Why did the programmer get kicked out of school? Because he kept breaking too many classes!",
    "What do you call a programmer from Finland? Nerdic!",
    "Why do programmers hate nature? It has too many bugs!",
    "What's a programmer's favorite place in New York? Boolean Station!",
    "Why did the programmer get stuck in the shower? The instructions said: Lather, Rinse, Repeat!"
]

from typing import Dict, Any
from fastapi import APIRouter
import random

# Collection of programming jokes
JOKES = [
    "Why did the programmer quit his job? Because he didn't get arrays!",
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the programmer go broke? Because he used up all his cache!",
    "What's a programmer's favorite hangout spot? The Foo Bar!",
    "Why do programmers always mix up Halloween and Christmas? Because Oct 31 equals Dec 25!",
    "Why did the programmer get kicked out of school? Because he kept breaking too many classes!",
    "What do you call a programmer from Finland? Nerdic!",
    "Why do programmers hate nature? It has too many bugs!",
    "What's a programmer's favorite place in New York? Boolean Station!",
    "Why did the programmer get stuck in the shower? The instructions said: Lather, Rinse, Repeat!"
]

class JokeAgent:
    """
    Joke Agent
    -----------
    Purpose: Returns a random programming joke from a collection.
    """
    
    def get_joke(self) -> Dict[str, str]:
        """Returns a random programming joke."""
        return {"joke": random.choice(JOKES)}
    
# Keep the original function for backward compatibility
def agent_main():
    """
    Original agent_main function for backward compatibility.
    """
    agent = JokeAgent()
    return agent.get_joke()

def register_routes(router: APIRouter):
    """Registers the joke agent's routes with the provided APIRouter."""
    
    agent = JokeAgent()
    
    @router.get("/joke", summary="Returns a random joke.", tags=["Simple Agents"])
    async def joke_route():
        """
        Returns a hard-coded joke.
        
        **Process:** An instance of the `JokeAgent` is used to generate the response.
        
        **Example Output:**
        
        ```json
        {
          "agent": "joke",
          "result": {
            "joke": "Why do programmers prefer dark mode? Because light attracts bugs!"
          }
        }
        ```
        """
        return {"agent": "joke", "result": agent.get_joke()}
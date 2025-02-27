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

def agent_main():
    """
    Joke Agent
    -----------
    Purpose: Returns a random programming joke from a collection.
    
    Usage:
        # In a Python shell:
        from agents import joke
        result = joke.agent_main()
        print(result)  # Example output: {'joke': 'Why do programmers prefer dark mode? Because light attracts bugs!'}
    """
    return {"joke": random.choice(JOKES)}
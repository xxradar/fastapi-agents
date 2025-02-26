from typing import List, Dict

AGENTS_INFO: List[Dict[str, str]] = [
    {
        "name": "hello_world",
        "description": "Returns a simple hello world message.",
        "instructions": "Call /agent/hello_world with no additional parameters."
    },
    {
        "name": "goodbye",
        "description": "Returns a goodbye message.",
        "instructions": "Call /agent/goodbye with no additional parameters."
    },
    {
        "name": "echo",
        "description": "Returns an echo message.",
        "instructions": "Call /agent/echo with no additional parameters."
    },
    {
        "name": "time",
        "description": "Returns the current server time.",
        "instructions": "Call /agent/time with no additional parameters."
    },
    {
        "name": "joke",
        "description": "Returns a random joke.",
        "instructions": "Call /agent/joke with no additional parameters."
    },
    {
        "name": "quote",
        "description": "Returns an inspirational quote.",
        "instructions": "Call /agent/quote with no additional parameters."
    },
    {
        "name": "math",
        "description": "Evaluates a math expression after verifying a token.",
        "instructions": "Call /agent/math with token=MATH_SECRET and expression parameters."
    }
    
]
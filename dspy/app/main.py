from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from typing import Optional, List, Dict, Any
import os
from agents.dspy_integration import load_agent, run_agent

app = FastAPI(title="FastAPI Agent System")

# Agent information dictionary
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
    },
    {
        "name": "classifier",
        "description": "Classifies input text using advanced rule-based logic.",
        "instructions": "Call /agent/classifier with INPUT_TEXT parameter."
    },
    {
        "name": "summarizer",
        "description": "Summarizes a block of text.",
        "instructions": "Call /agent/summarizer with TEXT_TO_SUMMARIZE parameter."
    }
]

@app.get("/agents")
async def list_all_agents() -> Dict[str, List[Dict[str, str]]]:
    """
    Returns a list of all available agents with brief descriptions and instructions.
    """
    return {"agents": AGENTS_INFO}

@app.get("/agent/hello_world")
async def hello_world_agent():
    agent_file = os.path.join("agents", "hello_world.py")
    agent_module = load_agent(agent_file)
    output = run_agent(agent_module)
    return {"agent": "hello_world", "result": output}

@app.get("/agent/goodbye")
async def goodbye_agent():
    agent_file = os.path.join("agents", "goodbye.py")
    agent_module = load_agent(agent_file)
    output = run_agent(agent_module)
    return {"agent": "goodbye", "result": output}

@app.get("/agent/echo")
async def echo_agent():
    agent_file = os.path.join("agents", "echo.py")
    agent_module = load_agent(agent_file)
    output = run_agent(agent_module)
    return {"agent": "echo", "result": output}

@app.get("/agent/time")
async def time_agent():
    agent_file = os.path.join("agents", "time.py")
    agent_module = load_agent(agent_file)
    output = run_agent(agent_module)
    return {"agent": "time", "result": output}

@app.get("/agent/joke")
async def joke_agent():
    agent_file = os.path.join("agents", "joke.py")
    agent_module = load_agent(agent_file)
    output = run_agent(agent_module)
    return {"agent": "joke", "result": output}

@app.get("/agent/quote")
async def quote_agent():
    agent_file = os.path.join("agents", "quote.py")
    agent_module = load_agent(agent_file)
    output = run_agent(agent_module)
    return {"agent": "quote", "result": output}

@app.get("/agent/math")
async def math_agent(token: Optional[str] = None, expression: Optional[str] = None):
    agent_file = os.path.join("agents", "math.py")
    agent_module = load_agent(agent_file)
    if hasattr(agent_module, 'TOKEN'):
        agent_module.TOKEN = token
    if hasattr(agent_module, 'EXPRESSION'):
        agent_module.EXPRESSION = expression
    output = run_agent(agent_module)
    return {"agent": "math", "result": output}

@app.get("/agent/classifier")
async def classifier_agent(INPUT_TEXT: Optional[str] = None):
    agent_file = os.path.join("agents", "classifier.py")
    agent_module = load_agent(agent_file)
    if hasattr(agent_module, 'INPUT_TEXT'):
        agent_module.INPUT_TEXT = INPUT_TEXT
    output = run_agent(agent_module)
    return {"agent": "classifier", "result": output}

@app.get("/agent/summarizer")
async def summarizer_agent(TEXT_TO_SUMMARIZE: Optional[str] = None):
    agent_file = os.path.join("agents", "summarizer.py")
    agent_module = load_agent(agent_file)
    if hasattr(agent_module, 'TEXT_TO_SUMMARIZE'):
        agent_module.TEXT_TO_SUMMARIZE = TEXT_TO_SUMMARIZE
    output = run_agent(agent_module)
    return {"agent": "summarizer", "result": output}

@app.get("/favicon.ico")
async def get_favicon():
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
        <rect width="16" height="16" fill="#4a90e2"/>
        <text x="2" y="12" font-size="10" fill="white">A</text>
    </svg>'''
    return Response(content=svg.encode('utf-8'), media_type="image/svg+xml")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Hello World Agent System!"}

@app.get("/health")
async def health_check():
    return JSONResponse({"status": "ok", "message": "Healthy"})

@app.get("/agent/{agent_name}")
async def execute_agent(agent_name: str, request: Request):
    # Construct the path to the agent file
    agent_file = os.path.join("agents", f"{agent_name}.py")
    if not os.path.exists(agent_file):
        raise HTTPException(status_code=404, detail="Agent not found.")
    
    try:
        agent_module = load_agent(agent_file)
        
        # Set global variables if they are provided and the agent supports them
        if hasattr(agent_module, 'TOKEN') and 'token' in request.query_params:
            agent_module.TOKEN = request.query_params['token']
        if hasattr(agent_module, 'EXPRESSION') and 'expression' in request.query_params:
            agent_module.EXPRESSION = request.query_params['expression']
        if hasattr(agent_module, 'INPUT_TEXT') and 'INPUT_TEXT' in request.query_params:
            agent_module.INPUT_TEXT = request.query_params['INPUT_TEXT']
        if hasattr(agent_module, 'TEXT_TO_SUMMARIZE') and 'TEXT_TO_SUMMARIZE' in request.query_params:
            agent_module.TEXT_TO_SUMMARIZE = request.query_params['TEXT_TO_SUMMARIZE']
            
        output = run_agent(agent_module)
        return {"agent": agent_name, "result": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing agent: {str(e)}")
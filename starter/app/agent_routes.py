from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Optional
import os
from agents.dspy_integration import load_agent, run_agent

router = APIRouter()

@router.get("/agent/hello_world")
async def hello_world_agent():
    agent_file = os.path.join("agents", "hello_world.py")
    agent_module = load_agent(agent_file)
    output = run_agent(agent_module)
    return {"agent": "hello_world", "result": output}

@router.get("/agent/goodbye")
async def goodbye_agent():
    agent_file = os.path.join("agents", "goodbye.py")
    agent_module = load_agent(agent_file)
    output = run_agent(agent_module)
    return {"agent": "goodbye", "result": output}

@router.get("/agent/echo")
async def echo_agent():
    agent_file = os.path.join("agents", "echo.py")
    agent_module = load_agent(agent_file)
    output = run_agent(agent_module)
    return {"agent": "echo", "result": output}

@router.get("/agent/time")
async def time_agent():
    agent_file = os.path.join("agents", "time.py")
    agent_module = load_agent(agent_file)
    output = run_agent(agent_module)
    return {"agent": "time", "result": output}

@router.get("/agent/joke")
async def joke_agent():
    agent_file = os.path.join("agents", "joke.py")
    agent_module = load_agent(agent_file)
    output = run_agent(agent_module)
    return {"agent": "joke", "result": output}

@router.get("/agent/quote")
async def quote_agent():
    agent_file = os.path.join("agents", "quote.py")
    agent_module = load_agent(agent_file)
    output = run_agent(agent_module)
    return {"agent": "quote", "result": output}

@router.get("/agent/math")
async def math_agent(token: Optional[str] = None, expression: Optional[str] = None):
    agent_file = os.path.join("agents", "math.py")
    agent_module = load_agent(agent_file)
    if hasattr(agent_module, 'TOKEN'):
        agent_module.TOKEN = token
    if hasattr(agent_module, 'EXPRESSION'):
        agent_module.EXPRESSION = expression
    output = run_agent(agent_module)
    return {"agent": "math", "result": output}

@router.get("/agent/{agent_name}")
async def execute_agent(agent_name: str, request: Request):
    """
    Dynamically loads and executes a specified agent.

    Parameters:
    - agent_name: Name of the agent file (without .py extension).
    - token: Optional authentication token for agents requiring authorization.
    - expression: Optional mathematical expression for matah agent.

    Returns:
    - JSON response with the execution result or an error message.
    """
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
            
        output = run_agent(agent_module)
        return {"agent": agent_name, "result": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing agent: {str(e)}")
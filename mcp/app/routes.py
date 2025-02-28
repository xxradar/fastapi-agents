from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from typing import Optional, List, Dict, Any
import os

# Import from the same location used by your agent files
from app.mcp_adapter import MCPAdapter
from agents.dspy_integration import load_agent, run_agent

router = APIRouter()

# Agent information dictionary
AGENTS_INFO: List[Dict[str, str]] = [
    
    {
        "name": "quote",
        "description": "Returns an inspirational quote.",
        "instructions": "Call /agent/quote with no additional parameters."
    },
    
    {
        "name": "classifier",
        "description": "Classifies input text using advanced rule-based logic.",
        "instructions": "Call /agent/classifier with INPUT_TEXT parameter."
    },
  
    {
        "name": "calculator",
        "description": "Evaluates an arithmetic expression.",
        "instructions": "Post to /agents/calculator with a JSON payload containing the expression."
    },
    {
        "name": "multi_step_reasoning",
        "description": "Iteratively refines a hypothesis by sharing and updating context through MCP. This agent takes an initial hypothesis and iteratively refines it by sharing and updating context through MCP. It continues refining the hypothesis until a final answer is received from MCP or the maximum number of iterations is reached.",
        "instructions": "Post to /agents/multi_step_reasoning with a JSON payload containing an initial hypothesis. Example prompt: {\"hypothesis\": \"The Earth is flat\"}. Expected output: {\"result\": {\"final_answer\": \"The Earth is an oblate spheroid\"}, \"context\": {}}"
    },
    {
        "name": "workflow_coordinator",
        "description": "Coordinates and aggregates responses from multiple sub-agents using MCP for shared context. This agent simulates a workflow where multiple sub-agents contribute to a final decision or report. It aggregates the responses from these sub-agents and updates the context accordingly using MCP.",
        "instructions": "Post to /agents/workflow_coordinator with no additional parameters. Example prompt: {}. Expected output: {\"result\": \"Aggregated results: Result from agent 1, Result from agent 2, Result from agent 3\", \"context\": {}}"
    },
    {
    "name": "workflow_decisioning",
    "description": "Coordinates and aggregates responses from multiple sub-agents using MCP for shared context. This agent examines a task description, selects sub-agents based on keywords, executes them, and updates shared state using MCP. It outputs a detailed, step-by-step decision process.",
    "instructions": "POST to /agents/workflow_decisioning with a JSON payload containing a key 'task_description'. Example prompt: {\"task_description\": \"Please analyze and report the data\"}. Expected output: {\"result\": \"<final aggregated output with detailed steps>\", \"context\": { ... }}."
  }
]

@router.get("/agents")
async def list_all_agents() -> Dict[str, List[Dict[str, str]]]:
    """
    Returns a list of all available agents with brief descriptions and instructions.
    """
    return {"agents": AGENTS_INFO}




@router.get("/agent/quote")
async def quote_agent():
    agent_file = os.path.join("agents", "quote.py")
    agent_module = load_agent(agent_file)
    output = run_agent(agent_module)
    return {"agent": "quote", "result": output}



@router.get("/favicon.ico")
async def get_favicon():
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
        <rect width="16" height="16" fill="#4a90e2"/>
        <text x="2" y="12" font-size="10" fill="white">A</text>
    </svg>'''
    return Response(content=svg.encode('utf-8'), media_type="image/svg+xml")

@router.get("/")
async def read_root():
    return {"message": "Welcome to the Hello World Agent System!"}

@router.get("/health")
async def health_check():
    return JSONResponse({"status": "ok", "message": "Healthy"})



@router.post("/agents/calculator")
async def calculator_agent_route(payload: dict):
    """
    Evaluates an arithmetic expression.
    """
    agent_file = os.path.join("agents", "calculator.py")
    agent_module = load_agent(agent_file)

    # Inject the adapter so code references the same place that tests can patch
    agent_module.mcp_adapter = MCPAdapter()

    agent_module.EXPRESSION = payload.get("expression")
    output = run_agent(agent_module)
    return {"agent": "calculator", "result": output}

@router.post("/agents/multi_step_reasoning")
async def multi_step_reasoning_agent_route(payload: dict):
    """
    Iteratively refines a hypothesis by sharing and updating context through MCP.
    """
    agent_file = os.path.join("agents", "multi_step_reasoning.py")
    agent_module = load_agent(agent_file)

    # Inject the adapter so code references the same place that tests can patch
    agent_module.mcp_adapter = MCPAdapter()

    agent_module.HYPOTHESIS = payload.get("hypothesis")
    output = run_agent(agent_module)
    return {"agent": "multi_step_reasoning", "result": output}

@router.post("/agents/workflow_decisioning")
async def workflow_decisioning_agent_route(payload: dict):
    """
    Coordinates and aggregates responses from multiple sub-agents using decision logic based on task descriptions.
    """
    agent_file = os.path.join("agents", "workflow_decisioning.py")
    agent_module = load_agent(agent_file)

    # Inject the adapter so code references the same place that tests can patch
    agent_module.mcp_adapter = MCPAdapter()

    # Set the task_description as a global variable
    agent_module.TASK_DESCRIPTION = payload.get("task_description", "")
    
    # Run the agent without passing task_description as a parameter
    output = run_agent(agent_module)
    return {"agent": "workflow_decisioning", "result": output}

@router.post("/agents/workflow_coordinator")
async def workflow_coordinator_agent_route(payload: dict):
    """
    Coordinates and aggregates responses from multiple sub-agents using MCP for shared context.
    """
    agent_file = os.path.join("agents", "workflow_coordinator.py")
    agent_module = load_agent(agent_file)

    # Inject the adapter so code references the same place that tests can patch
    agent_module.mcp_adapter = MCPAdapter()

    output = run_agent(agent_module)
    return {"agent": "workflow_coordinator", "result": output}

@router.post("/dynamic-agents/{agent_name}")
async def execute_dynamic_agent(agent_name: str, payload: dict):
    """
    Execute a dynamic agent with additional parameters provided in the request body.
    """
    agent_file = os.path.join("agents", f"{agent_name}.py")
    if not os.path.exists(agent_file):
        raise HTTPException(status_code=404, detail="Agent not found.")
    
    try:
        agent_module = load_agent(agent_file)
        # Update agent globals with payload values if supported
        for key, value in payload.items():
            if hasattr(agent_module, key):
                setattr(agent_module, key, value)
        
        output = run_agent(agent_module)
        return {"agent": agent_name, "result": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing agent: {str(e)}")
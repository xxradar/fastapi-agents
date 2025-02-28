from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from typing import Optional, List, Dict, Any
import os

# Import from the same location used by your agent files
from app.mcp_adapter import MCPAdapter
from agents.dspy_integration import load_agent, run_agent

# Import agent route registrations
from agents.classifier import register_routes as register_classifier_routes
from agents.calculator import register_routes as register_calculator_routes
from agents.multi_step_reasoning import register_routes as register_multi_step_reasoning_routes
from agents.workflow_coordinator import register_routes as register_workflow_coordinator_routes
from agents.workflow_decisioning import register_routes as register_workflow_decisioning_routes

router = APIRouter()

# Agent information dictionary
AGENTS_INFO: List[Dict[str, str]] = [
    # Simple Agents
    {
        "category": "Simple Agents",
        "name": "quote",
        "description": "Returns an inspirational quote.",
        "instructions": "Call /agent/quote with no additional parameters."
    },
    
    {
        "category": "Simple Agents",
        "name": "classifier",
        "description": "Classifies input text using advanced rule-based logic.",
        "instructions": "Call /agent/classifier with INPUT_TEXT parameter."
    },
  
    # MCP Agents
    {
        "category": "MCP Agents",
        "name": "calculator",
        "description": "Evaluates an arithmetic expression with context sharing via MCP.",
        "details": "This agent demonstrates basic MCP functionality by evaluating arithmetic expressions and sharing the result through the Module Context Protocol. It safely evaluates expressions using a secure evaluation method and maintains context between calls.",
        "instructions": "POST to /agents/calculator with a JSON payload containing the expression. Example: {\"expression\": \"3 + 4 * 2\"}",
        "example_output": "{\"agent\": \"calculator\", \"result\": {\"result\": 11, \"context\": {\"expression\": \"3 + 4 * 2\", \"previous_result\": null}}}"
    },
    {
        "category": "MCP Agents",
        "name": "multi_step_reasoning",
        "description": "Iteratively refines a hypothesis through context sharing and updates via MCP.",
        "details": "This agent demonstrates advanced reasoning capabilities using MCP for state management. It takes an initial hypothesis and iteratively refines it by sharing and updating context through MCP. The agent continues refining the hypothesis until a final answer is received from MCP or the maximum number of iterations is reached. This showcases how MCP can be used for complex, multi-step reasoning processes.",
        "instructions": "POST to /agents/multi_step_reasoning with a JSON payload containing an initial hypothesis. Example: {\"hypothesis\": \"The Earth is flat\"}",
        "example_output": "{\"agent\": \"multi_step_reasoning\", \"result\": {\"final_answer\": \"The Earth is an oblate spheroid\", \"context\": {\"iteration\": 1, \"hypothesis\": \"The Earth is flat\"}}}"
    },
    {
        "category": "MCP Agents",
        "name": "workflow_coordinator",
        "description": "Coordinates and aggregates responses from multiple sub-agents using MCP for shared context.",
        "details": "This agent demonstrates workflow coordination using MCP. It simulates a scenario where multiple sub-agents contribute to a final decision or report. The agent aggregates the responses from these sub-agents and updates the shared context accordingly using MCP. This showcases how MCP can be used to coordinate complex workflows involving multiple agents.",
        "instructions": "POST to /agents/workflow_coordinator with no additional parameters. Example: {}",
        "example_output": "{\"agent\": \"workflow_coordinator\", \"result\": {\"result\": \"Aggregated results: Result from agent 1, Result from agent 2, Result from agent 3\", \"context\": {\"sub_agent_results\": {\"agent1\": \"Result from agent 1\", \"agent2\": \"Result from agent 2\", \"agent3\": \"Result from agent 3\"}, \"workflow_status\": \"in_progress\"}}}"
    },
    {
        "category": "MCP Agents",
        "name": "workflow_decisioning",
        "description": "Makes intelligent workflow decisions based on task descriptions using MCP for state management.",
        "details": "This agent demonstrates advanced decision-making capabilities using MCP. It examines a task description, selects appropriate sub-agents based on keywords in the description, executes them, and updates shared state using MCP. The agent outputs a detailed, step-by-step decision process, showcasing how MCP can be used for complex decisioning workflows.",
        "instructions": "POST to /agents/workflow_decisioning with a JSON payload containing a key 'task_description'. Example: {\"task_description\": \"Please analyze and report the data\"}",
        "example_output": "{\"agent\": \"workflow_decisioning\", \"result\": {\"result\": \"Aggregated results: Performed comprehensive data analysis\", \"context\": {\"task_description\": \"Please analyze and report the data\", \"selected_agents\": [\"analysis\"], \"sub_agent_results\": {\"analysis\": \"Performed comprehensive data analysis\"}, \"workflow_status\": \"in_progress\", \"steps\": [\"collect\", \"analyze\"]}}}"
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



# Calculator route is now registered via register_calculator_routes

# Multi-Step Reasoning route is now registered via register_multi_step_reasoning_routes

# Workflow Decisioning route is now registered via register_workflow_decisioning_routes

# Workflow Coordinator route is now registered via register_workflow_coordinator_routes

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

# Register agent routes
register_classifier_routes(router)
register_calculator_routes(router)
register_multi_step_reasoning_routes(router)
register_workflow_coordinator_routes(router)
register_workflow_decisioning_routes(router)
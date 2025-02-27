# main.py
from fastapi import FastAPI, HTTPException, Request, APIRouter
from fastapi.responses import JSONResponse, Response
from typing import Optional, List, Dict, Any
import os
from agents.dspy_integration import load_agent, run_agent
from agents.classifier import register_routes as register_classifier_routes
from agents.summarizer import register_routes as register_summarizer_routes  


app = FastAPI(title="FastAPI Agent System")

# --- Agent Information ---
AGENTS_INFO: List[Dict[str, str]] = [
    {"name": "hello_world", "description": "Returns a simple hello world message.", "instructions": "Call /agent/hello_world with no additional parameters."},
    {"name": "goodbye", "description": "Returns a goodbye message.", "instructions": "Call /agent/goodbye with no additional parameters."},
    {"name": "classifier", "description": "Classifies input text using advanced rule-based logic.", "instructions": "Call /agent/classifier with INPUT_TEXT parameter."},
    {"name": "summarizer", "description": "Summarizes a block of text.", "instructions": "Call /agent/summarizer with TEXT_TO_SUMMARIZE parameter."},
]

@app.get("/agents")
async def list_all_agents() -> Dict[str, List[Dict[str, str]]]:
    """Returns a list of all available agents with brief descriptions and instructions."""
    return {"agents": AGENTS_INFO}

# --- Agent Router ---
agent_router = APIRouter(prefix="/agent")
register_classifier_routes(agent_router)
register_summarizer_routes(agent_router)  # Register summarizer routes
app.include_router(agent_router)


# --- Other Routes ---

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

# NO summarizer route defined here. It's handled by the agent router.

@app.get("/agent/{agent_name}")  # Keep the generic route handler
async def execute_agent(agent_name: str, request: Request):
    agent_file = os.path.join("agents", f"{agent_name}.py")
    if not os.path.exists(agent_file):
        raise HTTPException(status_code=404, detail="Agent not found.")

    try:
        agent_module = load_agent(agent_file)

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
    return {"message": "Welcome to the Agent System!"}

@app.get("/health")
async def health_check():
    return JSONResponse({"status": "ok", "message": "Healthy"})
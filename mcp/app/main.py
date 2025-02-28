import os
from fastapi import FastAPI, Request, HTTPException
from agents.dspy_integration import load_agent, run_agent
from app.mcp_adapter import MCPAdapter
from app.routes import router as agent_router

app = FastAPI(title="Fastapi MCP Agents")
app.include_router(agent_router)

@app.get("/agent/{agent_name}")
async def run_agent_get(agent_name: str, request: Request):
    """Handle GET requests to /agent/{agent_name}"""
    # Construct the path to the agent file
    agent_file = os.path.join("agents", f"{agent_name}.py")
    if not os.path.exists(agent_file):
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        # Load the agent module
        agent_module = load_agent(agent_file)

        # Initialize and inject MCP Adapter
        mcp_adapter = MCPAdapter()
        agent_module.mcp_adapter = mcp_adapter

        # Set global variables from query parameters
        if hasattr(agent_module, 'TOKEN') and 'token' in request.query_params:
            agent_module.TOKEN = request.query_params['token']
        if hasattr(agent_module, 'INPUT_TEXT') and 'INPUT_TEXT' in request.query_params:
            agent_module.INPUT_TEXT = request.query_params['INPUT_TEXT']
        if hasattr(agent_module, 'TEXT_TO_SUMMARIZE') and 'TEXT_TO_SUMMARIZE' in request.query_params:
            agent_module.TEXT_TO_SUMMARIZE = request.query_params['TEXT_TO_SUMMARIZE']

        # Run the agent
        output = run_agent(agent_module)

        # Return result
        return {"agent": agent_name, "result": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing agent: {str(e)}")

@app.post("/agents/{agent_name}")
async def run_agent_post(agent_name: str, request: Request):
    """
    Runs an agent using agent_name.
    Optionally sets EXPRESSION if posted in JSON.
    """
    # Construct the path to the agent file
    agent_file = os.path.join("agents", f"{agent_name}.py")
    if not os.path.exists(agent_file):
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        # Parse request body
        data = await request.json()
        expression = data.get("expression")

        # Load the agent module
        agent_module = load_agent(agent_file)

        # Initialize and inject MCP Adapter
        mcp_adapter = MCPAdapter()
        agent_module.mcp_adapter = mcp_adapter

        # Set global variables from request body
        if expression and hasattr(agent_module, 'EXPRESSION'):
            agent_module.EXPRESSION = expression
        if 'hypothesis' in data and hasattr(agent_module, 'HYPOTHESIS'):
            agent_module.HYPOTHESIS = data['hypothesis']

        # Run the agent
        output = run_agent(agent_module)

        # Return result
        if "error" in output:
            # You may choose to return a 200 with the error object, 
            # or raise an exception:
            return {"agent": agent_name, "result": output}

        return {
            "agent": agent_name,
            "result": output["result"],
            "context": output.get("context", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing agent: {str(e)}")
# agents/workflow_coordinator.py

import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, Body

logging.basicConfig(level=logging.DEBUG)

def agent_main():
    """
    Workflow Coordinator Agent
    ----------------------------
    Purpose: Coordinate and aggregate responses from multiple sub-agents using MCP for shared context.
    
    Usage:
      from agents import workflow_coordinator
      result = workflow_coordinator.agent_main()
      # Expected output: {'result': <aggregated_result>, 'context': <updated_context>}
    """
    logging.debug("Workflow Coordinator agent started")

    # Simulate results from sub-agents
    sub_agent_results = {
        "agent1": "Result from agent 1",
        "agent2": "Result from agent 2",
        "agent3": "Result from agent 3"
    }
    
    # Create workflow context
    context = {
        "sub_agent_results": sub_agent_results,
        "workflow_status": "in_progress"
    }
    
    # Update context via MCP
    try:
        logging.debug("Updating context")
        if 'mcp_adapter' not in globals():
            logging.error("MCP adapter not injected")
            # Continue without MCP functionality
            updated_context = context
        else:
            updated_context = mcp_adapter.send_context(context)
        logging.debug(f"Updated context: {updated_context}")
    except Exception as exc:
        logging.exception("Failed to update context")
        return {"error": f"Failed to update context: {str(exc)}"}
    
    # Process updated context to produce final output
    final_output = updated_context.get(
        "aggregated_result",
        "Aggregated results: " + ", ".join(sub_agent_results.values())
    )
    
    return {"result": final_output, "context": updated_context}

def register_routes(router: APIRouter):
    """Registers the workflow coordinator agent's routes with the provided APIRouter."""

    @router.post("/agents/workflow_coordinator", summary="Coordinates and aggregates responses from multiple sub-agents", response_model=Dict[str, Any], tags=["MCP Agents"])
    async def workflow_coordinator_route(payload: Dict[str, Any] = Body(..., examples={"Example": {"value": {}}})):
        """
        Coordinates and aggregates responses from multiple sub-agents using MCP for shared context.

        **Input:**

        *   No specific input parameters required. The agent simulates responses from multiple sub-agents internally.

        **Process:** The agent simulates a scenario where multiple sub-agents contribute to a final decision or report.
        It aggregates the responses from these sub-agents and updates the shared context accordingly using MCP.
        This showcases how MCP can be used to coordinate complex workflows involving multiple agents.

        **Example Input (JSON payload):**

        ```json
        {}
        ```

        **Example Output:**

        ```json
        {
          "agent": "workflow_coordinator",
          "result": {
            "result": "Aggregated results: Result from agent 1, Result from agent 2, Result from agent 3",
            "context": {
              "sub_agent_results": {
                "agent1": "Result from agent 1",
                "agent2": "Result from agent 2",
                "agent3": "Result from agent 3"
              },
              "workflow_status": "in_progress"
            }
          }
        }
        ```
        """
        # Inject the adapter so code references the same place that tests can patch
        global mcp_adapter
        from app.mcp_adapter import MCPAdapter
        mcp_adapter = MCPAdapter()
        
        output = agent_main()
        return {"agent": "workflow_coordinator", "result": output}
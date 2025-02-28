import logging
import datetime
from typing import Optional, Dict, Any
from fastapi import APIRouter, Body

logging.basicConfig(level=logging.DEBUG)

# Global variable expected to be set externally.
try:
    TASK_DESCRIPTION
except NameError:
    TASK_DESCRIPTION = ""

class DummyMCPAdapter:
    """Dummy adapter to simulate MCP state management."""
    def send_context(self, context):
        logging.debug("DummyMCPAdapter: processing context update.")
        # Simulate a state update with timestamp and log of executed steps.
        # For testing, this adapter may return a controlled context.
        context["mcp_state"] = {
            "last_update": datetime.datetime.now().isoformat(),
            "steps_executed": context.get("steps", []),
            "status": "updated"
        }
        # Add an aggregated result based on sub-agent outputs.
        context["aggregated_result"] = (
            "Aggregated result: " + ", ".join(
                context.get("sub_agent_results", {}).values()
            )
        )
        return context


def agent_main():
    """
    Workflow Decisioning Agent
    ---------------------------
    Purpose:
      Coordinate and aggregate responses from multiple sub-agents.
      Uses decision logic based on keywords in the provided task description.
      Demonstrates MCP state management by logging each step.

    Usage:
      from agents import workflow_decisioning
      workflow_decisioning.TASK_DESCRIPTION = "Please analyze and report the data"
      result = workflow_decisioning.agent_main()
      # Expected output: {
      #    'result': <final aggregated output with detailed steps>,
      #    'context': <updated context including MCP state>
      # }
    """
    logging.debug("Workflow Decisioning agent started.")

    # Step 1: Log and record the task description.
    logging.debug("Received task description: %s", TASK_DESCRIPTION)
    steps = [f"Step 1: Received task '{TASK_DESCRIPTION}'."]
    
    # Step 2: Decide which sub-agents to run based on keywords.
    sub_agent_results = {}
    selected_agents = []
    lower_desc = TASK_DESCRIPTION.lower()

    if "analyze" in lower_desc:
        sub_agent_results["analysis"] = "Performed comprehensive data analysis"
        selected_agents.append("analysis")
    if "report" in lower_desc:
        sub_agent_results["report"] = "Generated detailed summary report"
        selected_agents.append("report")
    if "fetch" in lower_desc or "retrieve" in lower_desc:
        sub_agent_results["fetch"] = "Retrieved external dataset"
        selected_agents.append("fetch")
    if not selected_agents:
        # Run a default sub-agent if no keywords match.
        sub_agent_results["default"] = "Executed default processing"
        selected_agents.append("default")

    steps.append(f"Step 2: Analyzed keywords and selected agents: {', '.join(selected_agents)}.")
    logging.debug("Selected sub-agents: %s", selected_agents)

    # Step 3: Build the initial workflow context.
    context = {
        "task_description": TASK_DESCRIPTION,
        "selected_agents": selected_agents,
        "sub_agent_results": sub_agent_results,
        "workflow_status": "in_progress",
        "steps": steps
    }
    steps.append("Step 3: Executed sub-agents and collected results.")

    # Step 4: Update context via MCP.
    try:
        logging.debug("Updating context via MCP.")
        if "mcp_adapter" not in globals():
            logging.warning("MCP adapter not injected; using dummy adapter for simulation.")
            global mcp_adapter
            mcp_adapter = DummyMCPAdapter()
        # The adapter returns a new context, possibly with modified steps.
        context = mcp_adapter.send_context(context)
        # Note: Do not update local 'steps' here, we'll rely on context["steps"].
        logging.debug("Updated context: %s", context)
    except Exception as exc:
        logging.exception("Failed to update context via MCP.")
        return {"error": f"Failed to update context: {str(exc)}"}

    # Step 5: Generate final output using the steps from the updated context.
    final_output = context.get(
        "aggregated_result",
        "Aggregated results: " + ", ".join(sub_agent_results.values())
    )
    detailed_steps = "\n".join(context.get("steps", []))
    final_detailed_output = f"{final_output}\n\nDetailed Steps:\n{detailed_steps}"
    return {"result": final_detailed_output, "context": context}


def register_routes(router: APIRouter):
    """Registers the workflow decisioning agent's routes with the provided APIRouter."""

    @router.post("/agents/workflow_decisioning", summary="Makes intelligent workflow decisions based on task descriptions", response_model=Dict[str, Any], tags=["MCP Agents"])
    async def workflow_decisioning_route(payload: Dict[str, Any] = Body(..., examples={"Example": {"value": {"task_description": "Please analyze and report the data"}}})):
        """
        Makes intelligent workflow decisions based on task descriptions using MCP for state management.

        **Input:**

        *   **task_description (required, string):** The task description to analyze. Example: Please analyze and report the data

        **Process:** The agent examines the task description, selects appropriate sub-agents based on keywords in the description,
        executes them, and updates shared state using MCP. The agent outputs a detailed, step-by-step decision process,
        showcasing how MCP can be used for complex decisioning workflows.

        **Example Input (JSON payload):**

        ```json
        {
          "task_description": "Please analyze and report the data"
        }
        ```

        **Example Output:**

        ```json
        {
          "agent": "workflow_decisioning",
          "result": {
            "result": "Aggregated results: Performed comprehensive data analysis, Generated detailed summary report\\n\\nDetailed Steps:\\nStep 1: Received task 'Please analyze and report the data'.\\nStep 2: Analyzed keywords and selected agents: analysis, report.\\nStep 3: Executed sub-agents and collected results.",
            "context": {
              "task_description": "Please analyze and report the data",
              "selected_agents": ["analysis", "report"],
              "sub_agent_results": {
                "analysis": "Performed comprehensive data analysis",
                "report": "Generated detailed summary report"
              },
              "workflow_status": "in_progress",
              "steps": [
                "Step 1: Received task 'Please analyze and report the data'.",
                "Step 2: Analyzed keywords and selected agents: analysis, report.",
                "Step 3: Executed sub-agents and collected results."
              ]
            }
          }
        }
        ```
        """
        global TASK_DESCRIPTION
        TASK_DESCRIPTION = payload.get("task_description", "")
        
        # Inject the adapter so code references the same place that tests can patch
        global mcp_adapter
        from app.mcp_adapter import MCPAdapter
        mcp_adapter = MCPAdapter()
        
        output = agent_main()
        return {"agent": "workflow_decisioning", "result": output}


if __name__ == "__main__":
    # Example execution with a sample task description.
    sample_task = "Please analyze and report the data"
    TASK_DESCRIPTION = sample_task
    output = agent_main()
    print(output)

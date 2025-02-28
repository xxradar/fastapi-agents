import logging
import datetime

logging.basicConfig(level=logging.DEBUG)


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


def agent_main(task_description=""):
    """
    Workflow Decisioning Agent
    ---------------------------
    Purpose:
      Coordinate and aggregate responses from multiple sub-agents.
      Uses decision logic based on keywords in the provided task description.
      Demonstrates MCP state management by logging each step.

    Usage:
      from agents import workflow_decisioning
      result = workflow_decisioning.agent_main("Please analyze and report the data")
      # Expected output: {
      #    'result': <final aggregated output with detailed steps>,
      #    'context': <updated context including MCP state>
      # }
    """
    logging.debug("Workflow Decisioning agent started.")

    # Step 1: Log and record the task description.
    logging.debug("Received task description: %s", task_description)
    steps = [f"Step 1: Received task '{task_description}'."]
    
    # Step 2: Decide which sub-agents to run based on keywords.
    sub_agent_results = {}
    selected_agents = []
    lower_desc = task_description.lower()

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
        "task_description": task_description,
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


if __name__ == "__main__":
    # Example execution with a sample task description.
    sample_task = "Please analyze and report the data"
    output = agent_main(sample_task)
    print(output)

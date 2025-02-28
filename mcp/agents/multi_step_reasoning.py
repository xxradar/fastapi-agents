# agents/multi_step_reasoning.py

import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, Body

logging.basicConfig(level=logging.DEBUG)

# Global variable expected to be set externally.
try:
    HYPOTHESIS
except NameError:
    HYPOTHESIS = None

def agent_main():
    """
    Multi-Step Reasoning Agent
    ---------------------------
    Purpose: Iteratively refine a hypothesis by sharing and updating context through MCP.
    """
    logging.debug("Multi-Step Reasoning agent started")
    if not HYPOTHESIS:
        logging.debug("HYPOTHESIS is not set")
        return {"error": "HYPOTHESIS is not set."}

    hypothesis = HYPOTHESIS
    context = {
        "hypothesis": hypothesis,
        "iteration": 0,
        "history": [hypothesis]
    }
    max_iterations = 5

    for i in range(max_iterations):
        context["iteration"] = i
        # Update context via MCP
        try:
            logging.debug("Updating context (iteration %d)", i)
            if 'mcp_adapter' not in globals():
                logging.error("MCP adapter not injected")
                # Continue without MCP functionality
                updated_context = context
            else:
                updated_context = mcp_adapter.send_context(context)
            logging.debug("Updated context: %s", updated_context)
        except Exception as exc:
            logging.exception("Failed to update context")
            return {"error": f"Failed to update context: {str(exc)}"}

        # Check if MCP returned a final answer
        if "final_answer" in updated_context:
            logging.debug("Final answer received from MCP")
            return {
                "final_answer": updated_context["final_answer"],
                "context": updated_context.get("context", {})
            }

        # Otherwise, refine the hypothesis
        hypothesis += " refined"
        context["hypothesis"] = hypothesis
        context["history"].append(hypothesis)
        logging.debug("Refined hypothesis: %s", hypothesis)

    # If we reach max iterations without final answer, return partial
    logging.debug("Maximum iterations reached")
    return {
        "partial_hypothesis": hypothesis,
        "context": updated_context.get("context", {})
    }

def register_routes(router: APIRouter):
    """Registers the multi-step reasoning agent's routes with the provided APIRouter."""

    @router.post("/agents/multi_step_reasoning", summary="Iteratively refines a hypothesis through context updates", response_model=Dict[str, Any], tags=["MCP Agents"])
    async def multi_step_reasoning_route(payload: Dict[str, Any] = Body(..., examples={"Example": {"value": {"hypothesis": "The Earth is flat"}}})):
        """
        Iteratively refines a hypothesis through context sharing and updates via MCP.

        **Input:**

        *   **hypothesis (required, string):** The initial hypothesis to refine. Example: The Earth is flat

        **Process:** The agent takes an initial hypothesis and iteratively refines it by sharing and updating context through MCP.
        The agent continues refining the hypothesis until a final answer is received from MCP or the maximum number of iterations is reached.
        This showcases how MCP can be used for complex, multi-step reasoning processes.

        **Example Input (JSON payload):**

        ```json
        {
          "hypothesis": "The Earth is flat"
        }
        ```

        **Example Output:**

        ```json
        {
          "agent": "multi_step_reasoning",
          "result": {
            "final_answer": "The Earth is an oblate spheroid",
            "context": {
              "iteration": 1,
              "hypothesis": "The Earth is flat"
            }
          }
        }
        ```

        **Example Output (if maximum iterations reached without final answer):**

        ```json
        {
          "agent": "multi_step_reasoning",
          "result": {
            "partial_hypothesis": "The Earth is flat refined refined refined refined refined",
            "context": {
              "iteration": 5,
              "hypothesis": "The Earth is flat refined refined refined refined refined",
              "history": ["The Earth is flat", "The Earth is flat refined", ...]
            }
          }
        }
        ```
        """
        global HYPOTHESIS
        HYPOTHESIS = payload.get("hypothesis")
        
        # Inject the adapter so code references the same place that tests can patch
        global mcp_adapter
        from app.mcp_adapter import MCPAdapter
        mcp_adapter = MCPAdapter()
        
        output = agent_main()
        return {"agent": "multi_step_reasoning", "result": output}

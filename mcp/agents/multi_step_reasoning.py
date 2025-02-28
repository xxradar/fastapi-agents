# agents/multi_step_reasoning.py

import logging

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
                "result": {
                    "final_answer": updated_context["final_answer"],
                    "context": updated_context["context"]
                }
            }

        # Otherwise, refine the hypothesis
        hypothesis += " refined"
        context["hypothesis"] = hypothesis
        context["history"].append(hypothesis)
        logging.debug("Refined hypothesis: %s", hypothesis)

    # If we reach max iterations without final answer, return partial
    logging.debug("Maximum iterations reached")
    return {
        "result": {
            "partial_hypothesis": hypothesis,
            "context": updated_context.get("context", {})
        }
    }

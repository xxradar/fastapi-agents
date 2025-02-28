file: 3-mcp-agents.md

# Plan for MCP Showcase Agents

## Step 3: Implement MCP Showcase Agents

**Objective:**  
Develop a set of advanced agents that leverage MCP features for context sharing and improved decision-making. These agents will demonstrate how inter-module communication can enhance agent performance. For this phase, we plan to implement a series of single-file agents that use MCP for updating and retrieving context. Use a mix of GET and POST endpoints where appropriate.

**Examples of MCP Agents:**
- Context-Aware Calculator Agent
- Multi-Step Reasoning Agent
- Workflow Coordinator Agent

> **Note:** After completing each step, update the logs file (e.g., `/logs/3-logs.md`) and add corresponding tests in the `/tests` folder.

---

## Agent 1: Context-Aware Calculator Agent

**Purpose:**  
Evaluate arithmetic expressions while sharing context with the MCP system. The agent sends its expression and any prior calculation results as context and receives updated context before performing the calculation.

**Use Case:**  
Used when previous results or preferences need to be considered in calculations, enabling context-aware computations.

**Pseudocode:**

```python
# agents/calculator.py

# Global variable expected to be set externally
# Example: EXPRESSION = "3 + 4 * 2"
try:
    EXPRESSION
except NameError:
    EXPRESSION = None

def agent_main():
    """
    Context-Aware Calculator Agent
    --------------------------------
    Purpose: Evaluate arithmetic expressions with context sharing via MCP.
    
    Usage:
      from agents import calculator
      calculator.EXPRESSION = "3 + 4 * 2"
      result = calculator.agent_main()
      # Expected output: {'result': 11, 'context': <updated_context_from_MCP>}
    """
    if not EXPRESSION:
        return {"error": "EXPRESSION is not set."}
    
    # Pre-process the expression if necessary
    processed_expression = EXPRESSION
    
    # Create initial context
    context = {
        "expression": processed_expression,
        "previous_result": None
    }
    
    # Update context using MCP (update_context is injected into the agent module)
    updated_context = update_context(context)
    
    # Safely evaluate the arithmetic expression
    try:
        result = eval(processed_expression, {"__builtins__": {}})
    except Exception as e:
        return {"error": f"Failed to evaluate expression: {str(e)}"}
    
    return {"result": result, "context": updated_context}
```

---

## Agent 2: Multi-Step Reasoning Agent

**Purpose:**  
Perform iterative reasoning by continuously updating context via MCP until a final answer is reached.

**Use Case:**  
Ideal for tasks that require iterative refinement or multi-step decision-making, such as solving complex puzzles or planning tasks.

**Pseudocode:**

```python
# agents/multi_step_reasoning.py

def agent_main():
    """
    Multi-Step Reasoning Agent
    ---------------------------
    Purpose: Iteratively refine a hypothesis by sharing and updating context through MCP.
    
    Usage:
      from agents import multi_step_reasoning
      result = multi_step_reasoning.agent_main()
      # Expected output: {'final_answer': <final_answer>, 'context': <updated_context>}
    """
    # Initialize hypothesis and context
    hypothesis = "Initial hypothesis based on input data."
    context = {"hypothesis": hypothesis, "iteration": 0}
    max_iterations = 5
    
    for i in range(max_iterations):
        context["iteration"] = i
        # Update context via MCP
        updated_context = update_context(context)
        
        # Check if MCP returned a final answer
        if "final_answer" in updated_context:
            return {"final_answer": updated_context["final_answer"], "context": updated_context}
        
        # Refine the hypothesis (placeholder logic)
        hypothesis += " refined"
        context["hypothesis"] = hypothesis
    
    return {"result": hypothesis, "context": updated_context}
```

---

## Agent 3: Workflow Coordinator Agent

**Purpose:**  
Coordinate outputs from multiple sub-agents by aggregating their results using MCP to share context.

**Use Case:**  
Useful in workflows where several specialized agents contribute to a final decision or report. This agent aggregates sub-agent responses and updates context accordingly.

**Pseudocode:**

```python
# agents/workflow_coordinator.py

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
    updated_context = update_context(context)
    
    # Process updated context to produce final output
    final_output = updated_context.get(
        "aggregated_result",
        "Aggregated results: " + ", ".join(sub_agent_results.values())
    )
    
    return {"result": final_output, "context": updated_context}
```

---

## Testing and Logging

- **Testing:**  
  - Write tests in `/tests` to ensure that each MCP agent:
    - Correctly updates and retrieves context.
    - Handles missing parameters or errors gracefully.
- **Logging:**  
  - Create and Update `/logs/3-logs.md` after each agent is implemented and tested, detailing tasks completed, test outcomes, and any issues encountered.

---

## Summary

This plan outlines the development of MCP showcase agents that leverage advanced context sharing to improve decision-making:
- **Context-Aware Calculator Agent:** Evaluates arithmetic expressions using context.
- **Multi-Step Reasoning Agent:** Iteratively refines hypotheses using context updates.
- **Workflow Coordinator Agent:** Aggregates sub-agent outputs through shared context.

These examples demonstrate how to integrate MCP functionality into agents, setting the stage for further development of context-aware, multi-step reasoning workflows.

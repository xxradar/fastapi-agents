Below is the **/plans/2-Single_File_Agent.md** document outlining the implementation of a new, more complex math agent. This agent will be a single file that requires a hard-coded token key and evaluates a math expression. Comments within the agent will guide users on how to call it directly.

---

# Plan for Single File Math Agent Implementation

## Objective

- **Develop a single file math agent** that demonstrates more complex functionality than a simple "hello world" agent.
- **Incorporate a hard-coded token key** for authorization (e.g., `"MATH_SECRET"`).
- **Evaluate a math expression safely** if the token is valid.
- **Provide in-code comments** explaining how a user can call this agent directly.
- *Note:* This plan covers only one single file agent. Additional agents can be added in future phases (see plans/3).

---

## Overview

The math agent will be implemented in a new file (`agents/math.py`) and follow the same structure as the hello_world agent, but with added complexity:
- **Authorization:** It checks for a hard-coded token key before evaluating any math expression.
- **Math Evaluation:** It safely evaluates a user-provided arithmetic expression.
- **User Guidance:** Inline comments will explain how to set the token and input the expression, and then call `agent_main()` directly.

The FastAPI endpoint (`/agent/{agent_name}`) from Repo 1 will be used to load and execute this agent dynamically.

---

## Implementation Steps

### Step 1: Design the Math Agent

- **Functionality:**
  - The agent will expect a valid token (e.g., `"MATH_SECRET"`) to authorize execution.
  - It will evaluate a math expression provided via a global variable (e.g., `EXPRESSION`).
  - If the token does not match, it returns an error message.
- **User Instructions (to be included as comments in the file):**
  - How to set the token and expression.
  - How to invoke the `agent_main()` function directly.
- **Log Instruction:**  
  Record the design and expected behavior in `/logs/2-logs.md`.

---

### Step 2: Create the Math Agent File

- **File Name:**  
  Create a new file `agents/math.py`.
- **Implementation Requirements:**
  - Define a hard-coded token (e.g., `EXPECTED_TOKEN = "MATH_SECRET"`).
  - Use a function `agent_main()` that:
    - Checks if a global variable `TOKEN` matches `EXPECTED_TOKEN`.
    - If valid, safely evaluates a global variable `EXPRESSION` (e.g., using a limited eval or arithmetic parser).
    - Returns the computed result or an error message.
- **In-Code Comments:**
  - Include comments explaining how a user can set `TOKEN` and `EXPRESSION` and call `agent_main()` directly.
- **Example Code Snippet (for context, not final code in the plan):**
  ```python
  # agents/math.py
  
  # Expected token for authorization
  EXPECTED_TOKEN = "MATH_SECRET"
  
  # Global variables for demonstration purposes
  TOKEN = None  # User must set this before calling agent_main()
  EXPRESSION = None  # User must set this to a valid arithmetic expression (e.g., "2+2")
  
  def agent_main():
      """
      Main function for the Math Agent.
      
      Instructions for direct invocation:
      1. Set the global variable TOKEN to your token key (e.g., "MATH_SECRET").
      2. Set the global variable EXPRESSION to the arithmetic expression you want evaluated.
      3. Call agent_main() to execute the agent.
      
      Example:
          >>> from agents import math
          >>> math.TOKEN = "MATH_SECRET"
          >>> math.EXPRESSION = "3 * (4 + 2)"
          >>> result = math.agent_main()
          >>> print(result)  # Should output: 18
      
      Returns:
          The result of the evaluated expression if the token is valid; otherwise, an error message.
      """
      if TOKEN != EXPECTED_TOKEN:
          return "Error: Invalid token. Access denied."
      try:
          # For safety, restrict evaluation to numbers and basic math operators
          if not isinstance(EXPRESSION, str) or not EXPRESSION.replace(" ", "").isalnum():
              # Note: This is a simplistic check. In production, use a proper arithmetic parser.
              return "Error: Invalid expression format."
          # Evaluate the expression (this example uses eval; replace with a safer method as needed)
          result = eval(EXPRESSION, {"__builtins__": {}})
          return result
      except Exception as e:
          return f"Error during evaluation: {str(e)}"
  ```
- **Log Instruction:**  
  Update `/logs/2-logs.md` with details of the file creation and code implementation.

---

### Step 3: Integrate with FastAPI Endpoint

- **Dynamic Loading:**
  - The existing dynamic endpoint (`/agent/{agent_name}`) in `app/main.py` should load `agents/math.py` when `/agent/math` is requested.
- **Testing:**
  - Manually set `TOKEN` and `EXPRESSION` via the code or through test cases.
  - Verify that a valid token and expression produce the correct result.
  - Verify that an invalid token returns an appropriate error.
- **Log Instruction:**  
  Document endpoint testing results in `/logs/2-logs.md`.

---

### Step 4: Testing and Validation

- **Local Testing:**
  - Use the FastAPI Swagger UI or curl to test the `/agent/math` endpoint.
  - Confirm that the math agent returns the evaluated result when the correct token is set.
- **Automated Tests:**
  - Add tests in `/tests/test_agents.py` to verify:
    - Correct execution with a valid token.
    - Rejection with an invalid token.
    - Handling of malformed expressions.
- **Log Instruction:**  
  Record testing outcomes and any encountered issues in `/logs/2-logs.md`.

---

### Step 5: Documentation and Final Review

- **Update Documentation:**
  - Update `/docs/Implementation_Guide.md` to include the new math agent details.
  - Include inline instructions (from the agent file) for calling the agent directly.
- **Final Code Review:**
  - Ensure the code is clean, comments are clear, and the agent follows best practices.
- **Log Instruction:**  
  Summarize all completed tasks, test results, and any technical debt in `/logs/2-logs.md`.

---

## Summary

This plan outlines the creation of a single file math agent that performs arithmetic evaluation upon verifying a hard-coded token. The agent is integrated into the existing FastAPI system via the dynamic agent loader. Every step—from design to testing—is documented, and progress should be logged in `/logs/2-logs.md` after each phase. This implementation serves as a template for adding further single file agents in future phases.

---
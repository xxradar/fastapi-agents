# Plan for Simple Agents Implementation

## Objective

- Develop four simple agents as individual single-file agents in the `agents/` directory:
  - **Echo Agent (`echo.py`)** – Returns a hard-coded echo message.
  - **Time Agent (`time.py`)** – Returns a hard-coded time value.
  - **Joke Agent (`joke.py`)** – Returns a hard-coded joke.
  - **Quote Agent (`quote.py`)** – Returns a hard-coded inspirational quote.
- Each agent returns a JSON object with its respective content.
- All agents will be dynamically loaded via the `/agent/{agent_name}` endpoint.
- **Hard-coded content** for each agent is included directly within the file as a JSON structure.
- Use a simple, consistent naming convention (all lowercase names) for easy integration and future expansion.

> **Log Instruction:**  
> At the completion of each step, update `/logs/3-logs.md` with a summary of tasks, test results, and any issues encountered.

---

## Overview

This plan outlines the implementation of four simple agents that return static JSON responses. Each agent is a standalone Python module containing an `agent_main()` function that returns its hard-coded output. These agents serve as examples for how to build additional single-file agents and will be accessible using the dynamic loader in `app/main.py`.

---

## Implementation Steps

### Step 1: Design the Simple Agents

Define the behavior and expected JSON output for each agent:

- **Echo Agent (`echo.py`):**
  - **Purpose:** Returns an echo message.
  - **Output:** `{ "message": "Echo from agent!" }`

- **Time Agent (`time.py`):**
  - **Purpose:** Returns a hard-coded current time string.
  - **Output:** `{ "time": "2025-02-23T20:00:00Z" }`
  
- **Joke Agent (`joke.py`):**
  - **Purpose:** Returns a hard-coded joke.
  - **Output:** `{ "joke": "Why did the chicken cross the road? To get to the other side!" }`

- **Quote Agent (`quote.py`):**
  - **Purpose:** Returns a hard-coded inspirational quote.
  - **Output:** `{ "quote": "Believe in yourself and all that you are." }`

*Log Instruction:* Document the design decisions in `/logs/3-logs.md` before proceeding.

---

### Step 2: Create the Agent Files

For each agent, create a file in the `agents/` directory with the following content.

#### A. Echo Agent (`agents/echo.py`)

```python
# agents/echo.py

def agent_main():
    """
    Echo Agent
    -----------
    Purpose: Returns a hard-coded echo message.
    
    Usage:
        # In a Python shell:
        from agents import echo
        result = echo.agent_main()
        print(result)  # Expected output: {'message': 'Echo from agent!'}
    """
    return {"message": "Echo from agent!"}
```

#### B. Time Agent (`agents/time.py`)

```python
# agents/time.py

def agent_main():
    """
    Time Agent
    -----------
    Purpose: Returns a hard-coded representation of the current time.
    
    Usage:
        # In a Python shell:
        from agents import time
        result = time.agent_main()
        print(result)  # Expected output: {'time': '2025-02-23T20:00:00Z'}
    
    Note: This is a static example. In a real implementation, consider using dynamic time.
    """
    return {"time": "2025-02-23T20:00:00Z"}
```

#### C. Joke Agent (`agents/joke.py`)

```python
# agents/joke.py

def agent_main():
    """
    Joke Agent
    -----------
    Purpose: Returns a hard-coded joke.
    
    Usage:
        # In a Python shell:
        from agents import joke
        result = joke.agent_main()
        print(result)  # Expected output: {'joke': 'Why did the chicken cross the road? To get to the other side!'}
    """
    return {"joke": "Why did the chicken cross the road? To get to the other side!"}
```

#### D. Quote Agent (`agents/quote.py`)

```python
# agents/quote.py

def agent_main():
    """
    Quote Agent
    -----------
    Purpose: Returns a hard-coded inspirational quote.
    
    Usage:
        # In a Python shell:
        from agents import quote
        result = quote.agent_main()
        print(result)  # Expected output: {'quote': 'Believe in yourself and all that you are.'}
    """
    return {"quote": "Believe in yourself and all that you are."}
```

*Log Instruction:* After creating each file, update `/logs/3-logs.md` with details about file creation and content.

---

### Step 3: Validate Integration

- **Dynamic Loading:**  
  The FastAPI endpoint `/agent/{agent_name}` in `app/main.py` will dynamically load these agent files. For example, accessing `/agent/echo` will load `agents/echo.py`.

- **Manual Testing:**  
  1. Start the FastAPI server:
     ```bash
     uvicorn app.main:app --reload
     ```
  2. Test each endpoint using a browser, curl, or the Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs):
     - [http://127.0.0.1:8000/agent/echo](http://127.0.0.1:8000/agent/echo)
     - [http://127.0.0.1:8000/agent/time](http://127.0.0.1:8000/agent/time)
     - [http://127.0.0.1:8000/agent/joke](http://127.0.0.1:8000/agent/joke)
     - [http://127.0.0.1:8000/agent/quote](http://127.0.0.1:8000/agent/quote)
  
- **Automated Testing:**  
  Add tests in `/tests/` (e.g., `tests/test_agents.py`) to verify that each endpoint returns the expected JSON response.

*Log Instruction:* Record all testing results and any issues encountered in `/logs/3-logs.md`.

---

### Step 4: Final Documentation and Commit

- **Documentation:**  
  Update the repository’s README and related documentation in `/docs/` to include instructions on these simple agents.
  
- **Review:**  
  Verify that the code adheres to the naming conventions (all lowercase names) and that the hard-coded JSON responses match the design.
  
- **Commit:**  
  Commit all changes with clear commit messages referencing the completion of the simple agents phase.

*Log Instruction:* Finalize `/logs/3-logs.md` with a summary of all completed tasks, including file creation, integration tests, and documentation updates.

---

## Summary

This plan outlines the steps to implement four simple single-file agents—echo, time, joke, and quote—each returning a hard-coded JSON response. These agents demonstrate the core dynamic loading functionality of the system, adhering to a clear and consistent naming convention. Each agent is self-contained, making it easy to expand the system in future phases. All progress should be logged in `/logs/3-logs.md`.

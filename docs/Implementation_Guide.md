
# Implementation Guide

This guide provides step-by-step instructions for setting up and using the FastAPI Agent System. This repository is designed as a starter project for agent development. It demonstrates how to build a modular, single file agent system using FastAPI and dspy-inspired dynamic loading. In this version, agents are stored as individual Python files and are dynamically loaded and executed via a common endpoint.

> **Note:** This repository does not include Supabase integration. Future versions will add persistent storage and advanced agent creation features.

---

## Prerequisites

- **Python 3.9+** (recommended)
- **FastAPI** and **Uvicorn** for running the web server
- **python-dotenv** for environment variable management
- Basic familiarity with Python and RESTful APIs

Install the required dependencies (if not already installed):

```bash
pip install fastapi uvicorn python-dotenv
```

> **Codespaces Tip:** If using GitHub Codespaces, simply connect to the Codespace in VS Code; the repository will be cloned automatically.

---

## Project Structure

The repository is organized as follows:

```
fastapi-agent-system/
├─ app/
│   ├─ main.py          # FastAPI application entrypoint
│   └─ models.py        # (Reserved for future use, e.g., data models)
├─ agents/
│   ├─ __init__.py      # Package initializer for agent modules
│   ├─ hello_world.py   # Simple "Hello World" agent
│   ├─ math.py          # Math Agent (complex example with token check)
│   ├─ classifier.py    # dspy showcase: Classifier Agent
│   ├─ summarizer.py    # dspy showcase: Summarizer Agent
│   ├─ echo.py          # Simple Echo Agent
│   ├─ time.py          # Simple Time Agent
│   ├─ joke.py          # Simple Joke Agent
│   └─ quote.py         # Simple Quote Agent
├─ docs/
│   └─ (Documentation files)
├─ plans/
│   └─ (Plan documents for implementation phases)
├─ tests/
│   └─ (Test files for various endpoints and agents)
├─ requirements.txt     # List of dependencies
└─ .env                 # Environment variables (for future use)
```

---

## 1. Base FastAPI Application

The main application is located in `app/main.py`. It includes endpoints for:

- Root ("/") – A welcome message.
- Health Check ("/health") – Returns the system status.
- Dynamic Agent Execution ("/agent/{agent_name}") – Loads and executes an agent by its name.

**Example `app/main.py`:**

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
import os
from agents.dspy_integration import load_agent, run_agent

app = FastAPI(title="Hello World Agent System")

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
    return {"message": "Welcome to the Hello World Agent System!"}

@app.get("/health")
async def health_check():
    return JSONResponse({"status": "ok", "message": "Healthy"})

@app.get("/agent/{agent_name}")
async def execute_agent(agent_name: str):
    # Construct the path to the agent file
    agent_file = os.path.join("agents", f"{agent_name}.py")
    if not os.path.exists(agent_file):
        raise HTTPException(status_code=404, detail="Agent not found.")
    
    try:
        agent_module = load_agent(agent_file)
        output = run_agent(agent_module)
        return {"agent": agent_name, "result": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing agent: {str(e)}")
```

---

## 2. dspy-Inspired Dynamic Agent Loading

The file `agents/dspy_integration.py` provides helper functions to load and run agents dynamically.

**Example `agents/dspy_integration.py`:**

```python
import importlib.util
import os

def load_agent(agent_filename: str):
    """
    Dynamically load an agent module from the given filename.
    """
    module_name = os.path.splitext(os.path.basename(agent_filename))[0]
    spec = importlib.util.spec_from_file_location(module_name, agent_filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_agent(agent_module):
    """
    Execute the agent's main function (agent_main) and return its output.
    """
    if hasattr(agent_module, "agent_main"):
        return agent_module.agent_main()
    else:
        raise AttributeError("The agent does not define 'agent_main'.")
```

---

## 3. Included Agents

This repository includes several agents to demonstrate different functionalities.

### A. Advanced dspy Showcase Agents

1. **Math Agent (`agents/math.py`):**

   - **Purpose:**
     Evaluates arithmetic expressions after verifying a hard-coded token.
     
   - **Functionality:**
     - Checks if a global variable `TOKEN` matches the expected token (`"MATH_SECRET"`).
     - Safely evaluates the expression provided in a global variable `EXPRESSION`.
     - Uses AST parsing for secure expression evaluation.
     - Provides comprehensive error handling.
     
   - **Usage via API:**
     ```bash
     # Example API call:
     curl "http://localhost:8000/agent/math?token=MATH_SECRET&expression=3*(4%2B2)"
     # Expected response:
     # {"agent": "math", "result": 18}
     ```
     
   - **Usage in Code:**
     ```python
     # Direct usage in Python:
     from agents import math
     math.TOKEN = "MATH_SECRET"
     math.EXPRESSION = "3 * (4 + 2)"
     result = math.agent_main()  # Expected output: 18
     
     # Error handling examples:
     math.TOKEN = "WRONG_TOKEN"  # Returns: "Error: Invalid token. Access denied."
     math.TOKEN = "MATH_SECRET"
     math.EXPRESSION = "import os"  # Returns: "Error: Invalid expression..."
     ```
     
   - **Security Features:**
     - Token-based authorization required for execution
     - Safe expression evaluation using AST parsing
     - Protection against code injection
     - Comprehensive input validation
   
2. **Classifier Agent (`agents/classifier.py`):**

   - **Purpose:**  
     Classifies an input text based on simple keyword analysis.
     
   - **Usage:**  
     Set a global variable (e.g., `INPUT_TEXT`) and call `agent_main()` to receive a classification such as "Greeting", "Question", or "Statement".

3. **Summarizer Agent (`agents/summarizer.py`):**

   - **Purpose:**  
     Summarizes a block of text by truncating it to a fixed length (e.g., first 50 characters) and appending ellipsis if necessary.
     
   - **Usage:**  
     Set a global variable (e.g., `TEXT_TO_SUMMARIZE`) and call `agent_main()` to obtain the summary.

### B. Other Simple Agents

1. **Echo Agent (`agents/echo.py`):**

   - **Purpose:**
     Returns a simple echo message in JSON format.
     
   - **Usage:**
     ```bash
     curl http://localhost:8000/agent/echo
     # Returns: {"agent": "echo", "result": {"message": "Echo from agent!"}}
     ```

2. **Time Agent (`agents/time.py`):**

   - **Purpose:**
     Returns the current UTC time in ISO 8601 format.
     
   - **Usage:**
     ```bash
     curl http://localhost:8000/agent/time
     # Returns: {"agent": "time", "result": {"time": "2025-02-24T15:45:56Z"}}
     ```

3. **Joke Agent (`agents/joke.py`):**

   - **Purpose:**
     Returns a random programming joke from a collection.
     
   - **Usage:**
     ```bash
     curl http://localhost:8000/agent/joke
     # Returns: {"agent": "joke", "result": {"joke": "<random programming joke>"}}
     ```
     
   - **Features:**
     - Collection of 10 programming-related jokes
     - Random selection on each request
     - Family-friendly content

4. **Quote Agent (`agents/quote.py`):**

   - **Purpose:**
     Returns a random inspirational quote from a collection.
     
   - **Usage:**
     ```bash
     curl http://localhost:8000/agent/quote
     # Returns: {"agent": "quote", "result": {"quote": "<random inspirational quote>"}}
     ```
     
   - **Features:**
     - Collection of 10 inspirational quotes
     - Includes quotes from notable figures
     - Random selection on each request

> **Naming Convention:**  
> Each agent file should be named in all lowercase (e.g., `math.py`, `classifier.py`, etc.) so that it is automatically accessible via the `/agent/{agent_name}` endpoint.

---

## 4. Running and Testing the System

- **Start the FastAPI Server:**

  ```bash
  uvicorn app.main:app --reload
  ```

- **Access Endpoints:**

  - **Health Check:**  
    Visit [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) to verify the server is running.
  
  - **Execute an Agent:**  
    For example, to run the math agent:
    1. Ensure you set the required global variables in your agent file (or via testing):
       ```python
       # In a Python shell:
       from agents import math
       math.TOKEN = "MATH_SECRET"
       math.EXPRESSION = "3 * (4 + 2)"
       print(math.agent_main())  # Expected output: 18
       ```
    2. Alternatively, access via the browser or curl:
       ```bash
       curl http://127.0.0.1:8000/agent/math
       ```
  
  - **List and Execute Other Agents:**  
    Simply use the corresponding agent name in the URL (e.g., `/agent/echo`, `/agent/time`, etc.).

- **Testing with Swagger UI:**  
  Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to interact with the API endpoints.

---

## 5. Adding New Agents

- **File Placement:**  
  Create new agent files in the `agents/` directory following the naming convention (all lowercase, descriptive names).
  
- **Agent Interface:**  
  Each agent should define a function `agent_main()` that encapsulates its functionality.
  
- **Dynamic Loading:**  
  The system will automatically load any new agent file via the `/agent/{agent_name}` endpoint.

---

## Conclusion

This implementation guide provides a streamlined approach to setting up a FastAPI-based agent system with multiple single file agents. The repository currently includes a math agent (with token verification), two dspy showcase agents (classifier and summarizer), and several simple agents (echo, time, joke, quote). The system is designed to be modular and extensible, allowing new agents to be added easily by following the established conventions.


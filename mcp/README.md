# mcp-llm-agents
Advanced FastAPI agent system integrating Module Context Protocol (MCP) and LLM calls (Gemini/OpenAI) on a base agent framework. Features intelligent agents with enhanced dspy functionality for dynamic, context-aware responses

```markdown
# MCP-LLM Agents

A FastAPI-based agent system that extends the base dynamic agent framework with advanced MCP (Module Context Protocol) and LLM (Google/OpenAI) integrations. This project builds on the Repo 1 foundation by adding context-aware, multi-agent workflows and LLM-powered agents.

---

## Features

- Dynamic agent loading and execution
- Multiple agent support with dedicated endpoints
- MCP integration for enhanced context sharing
- LLM-based agents using Google and OpenAI APIs
- Agent listing and discovery endpoint
- Health check endpoint
- Comprehensive test suite and error handling
- Token-based authorization (for math agent) and advanced text processing (classifier and summarizer agents)

---

## Project Structure

```
mcp-llm-agents/
├─ app/
│   ├─ main.py           # FastAPI application entrypoint (refactored to use a separate routes file)
│   └─ routes.py         # Dedicated routes for agent endpoints (direct calls and dynamic loading)
├─ agents/
│   ├─ __init__.py       # Package initializer
│   ├─ hello_world.py    # Basic Hello World agent (from Repo 1)
│   ├─ math.py           # Math agent with token verification
│   ├─ classifier.py     # Advanced dspy showcase: Classifier agent
│   ├─ summarizer.py     # Advanced dspy showcase: Summarizer agent
│   ├─ mcp_agent1.py     # Example MCP agent 1
│   ├─ mcp_agent2.py     # Example MCP agent 2
│   ├─ llm_agent1.py     # Example LLM agent 1 (supports GET/POST)
│   ├─ llm_agent2.py     # Example LLM agent 2 (supports GET/POST)
│   ├─ echo.py           # Simple Echo agent
│   ├─ time.py           # Simple Time agent
│   ├─ joke.py           # Simple Joke agent
│   └─ quote.py          # Simple Quote agent
├─ docs/                # Documentation files
├─ plans/               # Detailed plans for each development phase
├─ tests/               # Test suite
├─ requirements.txt     # Dependencies
└─ LICENSE              # MIT License
```

---

## Getting Started

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the project root with your API keys and configuration (for MCP and LLM integrations):

```env
MCP_API_KEY=your_mcp_api_key

```

### Run the Server

```bash
uvicorn app.main:app --reload
```
2. Choose a module and navigate to its directory:
```bash
cd dspy  # or starter or base-framework
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
# Using the Python -m flag for proper module resolution
python -m uvicorn app.main:app --reload
```
## Running Tests

Navigate to the specific module directory and run:
```bash
# Using the Python -m flag for proper module resolution
python -m pytest tests
```
5. Test the endpoints:

Core Endpoints:
- Welcome message: GET /
- Health check: GET /health
- List all agents: GET /agents
---

## API Endpoints

### Core Endpoints

- **Welcome Message:** GET `/`
- **Health Check:** GET `/health`
- **List All Agents:** GET `/agents`

### Dedicated Agent Endpoints

- **Dynamic Agent Execution:** GET `/agent/{agent_name}`  
  Loads and executes an agent by its file name.

- **Quote Agent:** GET `/agent/quote`  
  Returns an inspirational quote.

- **Classifier Agent:** GET `/agent/classifier?INPUT_TEXT=Hello,%20how%20are%20you?`  
  Classifies input text into categories with a confidence score.


### MCP and LLM Endpoints

- **MCP Showcase Agents:**  
  `agents/multi_step_reasoning.py` with iterative reasoning capabilities
  `agents/workflow_coordinator.py` with sub-agent coordination capabilities
`agents/workflow_decisioning.py` with decision-making capabilities based on task 
`agents/calculator.py` with MCP context sharing capabilities

---

## Running Tests

Execute the test suite with:

```bash
pytest tests/
```

---

## Documentation

- **Implementation Guide:** Detailed setup and usage instructions are in `/docs/Implementation_Guide.md`.
- **Technical Specifications:** See `/docs/Technical_Specifications.md` for endpoint and data model details.
- **Testing Documentation:** Refer to `/docs/Testing_and_Validation.md`.
- **Additional Plans:** See the `/plans` folder for phase-specific implementation guides.

---

## Documentation First Coding

This repository was created using Documentation First Coding methodologies:

1. **Brainstorm and Design:**  
   All ideas and designs were thoroughly documented.
2. **Required Documentation:**  
   Technical and implementation documents are maintained in the `/docs` directory.
3. **Phase Plans:**  
   Detailed plans for each development phase are available in the `/plans` folder.
4. **Step-by-Step Execution:**  
   Development followed outlined steps with comprehensive testing.
5. **Tracking and Logging:**  
   Progress was tracked in the `/logs` directory.
6. **Testing and Updates:**  
   The project includes a complete test suite and regularly updated documentation.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Original Gist:**  
[https://gist.github.com/bar181/7fc0286841a38c72848ed037d0e561fd](https://gist.github.com/bar181/7fc0286841a38c72848ed037d0e561fd)

**Author:** Bradley Ross (bar181 on GitHub and Gists)
```
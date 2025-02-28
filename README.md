# FastAPI Agent System

A FastAPI-based dynamic agent system that leverages the ReACT methodology for building autonomous and human-in-the-loop agents. This mono repo contains multiple standalone modules, each focusing on different aspects of agent implementation.

## Features
- Dynamic agent loading and execution
- Multiple agent support with dedicated endpoints
- Agent listing and discovery endpoint
- Health check endpoint
- Error handling
- Comprehensive test suite
- Token-based authorization (for math agent)
- Advanced text processing (classifier and summarizer agents)

## Project Structure

This project is structured as a mono repo with multiple standalone modules:

### `/base-framework`
The recommended starting point for creating your own agents. This module provides the core framework for FastAPI Agents with minimal configuration required. It includes:
- Core agent execution framework
- Pre-built agents (Quote and Classifier)
- Dynamic agent execution
- Organized Swagger UI
- Comprehensive test suite (8 tests)
- No `.env` file required for setup

### `/starter`
A collection of simple agents that demonstrate basic functionality. This module includes:
- Hello World agent
- Goodbye agent
- Echo agent
- Time agent
- Joke agent
- Quote agent
- Math agent with token verification
- Organized routes and agent information
- No `.env` file required for setup

### `/dspy`
Advanced agents leveraging DSPy for complex text processing tasks. This module includes:
- DSPy integration for advanced AI capabilities
- Classifier agent for text classification
- Summarizer agent for text summarization
- TextRank summarizer agent
- All simple agents from the starter module
- Comprehensive test suite (30 tests)
- No `.env` file required for setup

### Planned Future Modules
This repository is actively expanding and in development with the following planned modules:

- **LLM Agents**: Will provide integration with various Large Language Models for more sophisticated reasoning and natural language understanding capabilities.
- **MIPROv2 Agents**: Will implement the MIPROv2 framework for multi-step reasoning and planning in complex environments.
- **Additional Advanced Agents**: More specialized agents for various domains and use cases.

## Mono Repo Structure

This project follows a mono repo style architecture:
- You can clone the entire repository to access all modules
- Each folder is designed to be modular and standalone
- Modules can be run independently with their own dependencies

```
fastapi-agents/
├─ base-framework/   # Core framework with minimal agents
├─ starter/          # Simple agents with basic functionality
├─ dspy/             # Advanced agents with DSPy integration
├─ (future) llm/     # Agents leveraging various LLMs
├─ (future) miprov2/ # Agents using MIPROv2 framework
└─ README.md         # Main documentation
```

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/bar181/fastapi-agents.git
cd fastapi-agents
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

5. Test the endpoints:

Core Endpoints:
- Welcome message: GET /
- Health check: GET /health
- List all agents: GET /agents

Agent endpoints vary by module. Check each module's README.md for specific details.

Example Usage:
```bash
# Test an endpoint (replace SERVER_URL with your server address)
curl SERVER_URL/agent/hello_world

# Test with parameters
curl "SERVER_URL/agent/math?token=MATH_SECRET&expression=3*(4%2B2)"
```

## Running Tests

Navigate to the specific module directory and run:
```bash
# Using the Python -m flag for proper module resolution
python -m pytest tests
```

## Documentation
- Each module contains its own `/docs` directory with detailed documentation
- `/plans` directories contain step-by-step instructions for development
- `/logs` directories track development progress

## This repository was created using Documentation First Coding Methodologies

Our development process followed a rigorous Documentation First approach:

1. **Brainstorm and Design:**  
   Initial ideas and designs were discussed and documented to establish project goals.

2. **Required Documentation:**  
   All technical and implementation documents were created and saved in the `/docs` directory.

3. **Phase Plans:**  
   Detailed plans for each development phase were created and are available in the `/plans` folder.

4. **Step-by-Step Execution:**  
   Development followed the step-by-step outlines provided in each phase, including comprehensive tests.

5. **Tracking and Logging:**  
   Every step of the process was tracked and logged in the `/logs` directory for transparency.

6. **Testing and Updates:**  
   Appropriate tests were implemented and documentation was continuously updated to reflect the current state of the project.

## Original Gist
https://gist.github.com/bar181/7fc0286841a38c72848ed037d0e561fd
### Author: Bradley Ross (bar181 on gists and github)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# DSPy Agents

This module contains agents that leverage **DSPy** for advanced text processing tasks, including classification and summarization. It also includes foundational agents (`hello_world` and `goodbye`) for demonstration purposes.

---

## Features

✅ **Advanced Text Processing with DSPy**
   - **Classifier Agent**: Uses advanced rule-based logic for text classification.
   - **Summarizer Agent**: Processes and summarizes long-form text.

✅ **Dynamic Agent Execution**
   - **Agents are loaded dynamically** via FastAPI and executed on demand.

✅ **Prebuilt Starter Agents**
   - **Hello World**: Returns a simple greeting.
   - **Goodbye**: Returns a farewell message.

✅ **API Integration**
   - Each agent is accessible via a dedicated API endpoint.

---

## Project Structure

```
fastapi-agent-system/
├─ app/
│   ├─ main.py          # FastAPI application entrypoint
│   └─ models.py        # (For future use: data models)
├─ agents/
│   ├─ __init__.py      # Package initializer
│   ├─ hello_world.py   # Hello World agent
│   ├─ goodbye.py       # Goodbye agent
│   ├─ classifier.py    # Text classification agent
│   ├─ summarizer.py    # Text summarization agent
├─ docs/                # Documentation for this module
├─ plans/               # Step by step instructions for AI code writing
├─ logs/                # Logging steps
├─ tests/               # Test suite
├─ requirements.txt     # Dependencies
└─ LICENSE             # MIT License
```

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:

For standalone modules:
```bash
uvicorn app.main:app --reload
```

For running within the mono repo:
```bash
# First, navigate to the specific module directory
cd dspy

# Then run the server using the Python -m flag
python -m uvicorn app.main:app --reload
```

3. Test the endpoints:

Core Endpoints:
- Welcome message: GET /
- Health check: GET /health
- List all agents: GET /agents

Simple Agents (No Parameters):
- Hello World: GET /agent/hello_world
- Goodbye: GET /agent/goodbye

Advanced Agents (With Parameters):
- Classifier: GET /agent/classifier?INPUT_TEXT=Hello,%20how%20are%20you?
- Summarizer: GET /agent/summarizer?TEXT_TO_SUMMARIZE=FastAPI%20is%20efficient&max_length=10

Example Usage:
```bash
# Test an endpoint (replace SERVER_URL with your server address)
curl SERVER_URL/agent/hello_world

# Test with parameters
curl "SERVER_URL/agent/summarizer?TEXT_TO_SUMMARIZE=FastAPI%20is%20efficient&max_length=10"
```

## Running Tests

For standalone modules:
```bash
pytest tests/
```

For running within the mono repo:
```bash
# First, navigate to the specific module directory
cd dspy

# Then run the tests using the Python -m flag
python -m pytest tests
```

## Documentation
- /docs main documentation for this module
- /plans step by step instructions
- /logs updates

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

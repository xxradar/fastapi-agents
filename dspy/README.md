# Base Framework - FastAPI Agents
source: https://github.com/bar181/fastapi-agents

This module serves as the core framework for **FastAPI Agents** within the `fastapi-agents` mono repo. It provides the foundation for integrating and running AI-driven agents, including **Quote** (a simple starting agent) and **Classifier** (which leverages DSPy for classification tasks).

---

## Features

✅ **Core Agent Execution Framework**
   - Provides a structured environment for running AI-based agents.
   - Supports **FastAPI** as the primary API framework.

✅ **Pre-Built Agents**
   - **Quote Agent**: Returns an inspirational quote.
   - **Classifier Agent**: Uses DSPy for advanced text classification.

✅ **Dynamic Agent Execution**
   - Supports the dynamic loading and execution of new agents.

✅ **Organized Swagger UI**
   - All available agents and their endpoints are listed in the Swagger UI.
   - Easily test and interact with the API.

✅ **API Integration**
   - Provides structured API endpoints for agent execution.

✅ **Comprehensive Test Suite**
   - Includes **8 tests** to validate core functionality.
   - Uses `pytest` for testing.

✅ **Minimal Configuration Required**
   - **No `.env` file required** for setup.
   - All necessary configurations are included within the module.

---

## Project Structure

```
base-framework/
├─ app/
│   ├─ main.py          # FastAPI application entrypoint
│   └─ models.py        # Placeholder for future data models
├─ agents/
│   ├─ __init__.py      # Package initializer
│   ├─ quote.py         # Quote agent
│   ├─ classifier.py    # DSPy-based classifier agent
├─ docs/                # Documentation for this module
├─ plans/               # Phase-based execution plans
├─ logs/                # Development logs
├─ tests/               # Test suite
├─ requirements.txt     # Dependencies
└─ LICENSE             # MIT License
```

---

## Getting Started

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run the Server**
```bash
uvicorn app.main:app --reload
```

For running within the mono repo:
```bash
# First, navigate to the specific module directory
cd base-framework

# Then run the server using the Python -m flag
python -m uvicorn app.main:app --reload
```

### **3. Test Endpoints**

Core Endpoints:
- **Welcome message**: `GET /`
- **Health check**: `GET /health`
- **List all agents**: `GET /agents`

Agent-Specific Endpoints:
- **Quote Agent**: `GET /agent/quote`
- **Classifier Agent**: `GET /agent/classifier?input_text=YourTextHere`

Example Usage:
```bash
curl http://127.0.0.1:8000/agent/quote
```

---

## Running Tests

Run all tests using:
```bash
pytest tests/
```

For running within the mono repo (base-framework is a folder)
```bash
# First, navigate to the specific module directory
cd base-framework

# Then run the tests using the Python -m flag
python -m pytest tests
```

The test suite includes **8 tests** to validate core functionality.

---

## Documentation
- `/docs/` - Technical documentation for this module.
- `/plans/` - Step-by-step execution plans.
- `/logs/` - Development logs tracking progress.

## Development Process

This repository follows a **Documentation First** approach:

1. **Brainstorm and Design**: Initial concepts and requirements are documented.
2. **Technical Documentation**: All implementation details are written before development.
3. **Phase Plans**: Development is guided by structured `/plans/` documents.
4. **Execution and Testing**: Code is written, executed, and tested step by step.
5. **Tracking and Logging**: Every step is logged in `/logs/` for transparency.
6. **Continuous Updates**: Documentation is kept up-to-date alongside the code.

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
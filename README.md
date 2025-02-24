# FastAPI Agent System

A FastAPI-based dynamic agent system that leverages the ReACT methodology for building autonomous and human-in-the-loop agents.

## Features
- Dynamic agent loading and execution
- Multiple agent support
- Health check endpoint
- Error handling
- Comprehensive test suite

## Project Structure
```
fastapi-agent-system/
├─ app/
│   ├─ main.py         # FastAPI application entrypoint
│   ├─ models.py       # (For future use: data models)
├─ agents/
│   ├─ __init__.py     # Package initializer
│   ├─ hello_world.py  # Hello World agent
│   ├─ goodbye.py      # Goodbye agent
├─ docs/               # Documentation
├─ tests/              # Test suite
├─ requirements.txt    # Dependencies
```

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn app.main:app --reload
```

3. Test the endpoints:
- Welcome message: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Hello World agent: http://127.0.0.1:8000/agent/hello_world
- Goodbye agent: http://127.0.0.1:8000/agent/goodbye

## Running Tests
```bash
pytest tests/
```

## Documentation
- [Implementation Guide](docs/Implementation_Guide.md)
- [Testing Documentation](docs/tests.md)
- [Technical Specifications](docs/Technical_Specifications.md)

## Future Enhancements
1. **Supabase Integration**
   - Store and retrieve agent definitions from database
   - User authentication and authorization
   - Row-level security for agent access

2. **Enhanced dspy Features**
   - AI-based agent self-improvement
   - Dynamic code generation
   - Agent learning capabilities

3. **Security Features**
   - Authentication system
   - Rate limiting
   - Input validation
   - Secure agent execution

## Original Gist
https://gist.github.com/bar181/7fc0286841a38c72848ed037d0e561fd
Author: Bradley Ross (bar181 on gists and github)

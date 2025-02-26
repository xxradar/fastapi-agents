from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from typing import List, Dict
import os
from app import agent_routes
from agents.dspy_integration import load_agent, run_agent

app = FastAPI(title="FastAPI Agent System")

# Agent information dictionary
AGENTS_INFO: List[Dict[str, str]] = [
    {
        "name": "hello_world",
        "description": "Returns a simple hello world message.",
        "instructions": "Call /agent/hello_world with no additional parameters."
    },
    {
        "name": "goodbye",
        "description": "Returns a goodbye message.",
        "instructions": "Call /agent/goodbye with no additional parameters."
    },
    {
        "name": "echo",
        "description": "Returns an echo message.",
        "instructions": "Call /agent/echo with no additional parameters."
    },
    {
        "name": "time",
        "description": "Returns the current server time.",
        "instructions": "Call /agent/time with no additional parameters."
    },
    {
        "name": "joke",
        "description": "Returns a random joke.",
        "instructions": "Call /agent/joke with no additional parameters."
    },
    {
        "name": "quote",
        "description": "Returns an inspirational quote.",
        "instructions": "Call /agent/quote with no additional parameters."
    },
    {
        "name": "math",
        "description": "Evaluates a math expression after verifying a token.",
        "instructions": "Call /agent/math with token=MATH_SECRET and expression parameters."
    }
    
]

@app.get("/agents")
async def list_all_agents() -> Dict[str, List[Dict[str, str]]]:
    """
    Returns a list of all available agents with brief descriptions and instructions.
    """
    return {"agents": AGENTS_INFO}

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

app.include_router(agent_routes.router)
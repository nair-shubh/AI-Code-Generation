#!/usr/bin/env python3
"""
Web Interface for Intelligent Code Automation Engine
Provides a modern web UI for the code automation system
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
import uvicorn

from src.core.engine import CodeTransformationPlatform, ExecutionStatus

# Pydantic models
class GitHubTokenRequest(BaseModel):
    github_token: str
    openai_token: str

class RepositoryRequest(BaseModel):
    github_token: str
    openai_token: str

class CodeGenerationRequest(BaseModel):
    github_token: str
    openai_token: str
    repo_url: str
    prompt: str
    branch_name: str = "ai-generated-changes"
    commit_message: str = "AI-generated improvements"

class ErrorResponse(BaseModel):
    error: str
    details: str = None

# Initialize FastAPI app
app = FastAPI(
    title="Intelligent Code Automation Engine",
    description="Advanced AI-powered code generation and deployment system",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global platform instance
platform = None
active_sessions = {}

@app.on_event("startup")
async def startup_event():
    """Initialize the code transformation platform"""
    global platform
    try:
        platform = CodeTransformationPlatform()
        print("✅ Code transformation platform initialized")
    except Exception as e:
        print(f"❌ Failed to initialize platform: {e}")

@app.get("/")
async def root():
    """Root endpoint with application info"""
    return {
        "application": "Intelligent Code Automation Engine",
        "version": "2.0.0",
        "features": [
            "AI-powered code generation",
            "E2B cloud execution",
            "GitHub integration",
            "Real-time progress tracking",
            "Automated testing and deployment"
        ],
        "endpoints": {
            "web_interface": "/ui",
            "api_docs": "/docs",
            "health": "/health",
            "repositories": "/api/repositories",
            "generate": "/api/generate",
            "stream": "/api/stream/{session_id}"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "platform_available": platform is not None,
        "e2b_available": hasattr(platform, 'e2b_session') if platform else False
    }

@app.get("/ui")
async def web_interface():
    """Serve the web interface"""
    return FileResponse("src/web/static/index.html")

@app.post("/api/repositories")
async def get_user_repositories(request: RepositoryRequest):
    """Get user's repositories using their GitHub token"""
    try:
        if not platform:
            raise HTTPException(status_code=500, detail="Platform not available")
        
        # Configure platform with user tokens
        platform.setup_github_connection(request.github_token)
        
        # Retrieve repositories
        repos = await platform.retrieve_user_repositories()
        
        # Convert to JSON-serializable format
        repos_data = []
        for repo in repos:
            repos_data.append({
                "name": repo.name,
                "owner": repo.owner,
                "url": repo.url,
                "description": repo.description,
                "language": repo.language
            })
        
        return repos_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate")
async def start_generation(request: CodeGenerationRequest):
    """Start the code generation process"""
    try:
        # Create session
        session_id = f"session_{datetime.now().timestamp()}"
        active_sessions[session_id] = {
            "github_token": request.github_token,
            "openai_token": request.openai_token,
            "repo_url": request.repo_url,
            "prompt": request.prompt,
            "branch_name": request.branch_name,
            "commit_message": request.commit_message,
            "status": "pending"
        }
        
        return {"session_id": session_id, "status": "started"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stream/{session_id}")
async def stream_generation_events(session_id: str) -> EventSourceResponse:
    """Stream generation events using SSE"""
    
    async def event_generator():
        try:
            if session_id not in active_sessions:
                yield {
                    "event": "error",
                    "data": {
                        "status": "error",
                        "message": "Session not found"
                    }
                }
                return
            
            session_data = active_sessions[session_id]
            
            # Create new platform instance for this session
            session_platform = CodeTransformationPlatform(
                openai_api_key=session_data["openai_token"],
                e2b_api_key=os.getenv("E2B_API_KEY")
            )
            
            session_platform.setup_github_connection(session_data["github_token"])
            
            # Update session status
            session_data["status"] = "running"
            
            # Step 1: Create execution environment
            yield {
                "event": "status_update",
                "data": {
                    "message": "Creating E2B cloud execution environment...",
                    "step": 1,
                    "total_steps": 6,
                    "status": "initializing"
                }
            }
            
            await session_platform.create_execution_environment()
            
            yield {
                "event": "status_update",
                "data": {
                    "message": "Execution environment created successfully",
                    "step": 1,
                    "total_steps": 6,
                    "status": "initializing"
                }
            }
            
            # Step 2: Download repository
            yield {
                "event": "status_update",
                "data": {
                    "message": "Downloading repository to execution environment...",
                    "step": 2,
                    "total_steps": 6,
                    "status": "analyzing"
                }
            }
            
            repo_path = await session_platform.download_repository(session_data["repo_url"])
            
            yield {
                "event": "status_update",
                "data": {
                    "message": "Repository downloaded successfully",
                    "step": 2,
                    "total_steps": 6,
                    "status": "analyzing"
                }
            }
            
            # Step 3: Examine codebase
            yield {
                "event": "status_update",
                "data": {
                    "message": "Examining codebase structure...",
                    "step": 3,
                    "total_steps": 6,
                    "status": "analyzing"
                }
            }
            
            analysis = await session_platform.examine_codebase(repo_path)
            
            yield {
                "event": "analysis_complete",
                "data": {
                    "message": f"Examination complete: {analysis['total_files']} files found",
                    "analysis": analysis,
                    "step": 3,
                    "total_steps": 6,
                    "status": "analyzing"
                }
            }
            
            # Step 4: Create transformations
            yield {
                "event": "status_update",
                "data": {
                    "message": "Creating code transformations with AI...",
                    "step": 4,
                    "total_steps": 6,
                    "status": "generating"
                }
            }
            
            transformations = await session_platform.create_code_transformations(
                session_data["prompt"], analysis
            )
            
            yield {
                "event": "modifications_generated",
                "data": {
                    "message": f"Created {len(transformations)} transformations",
                    "modifications_count": len(transformations),
                    "step": 4,
                    "total_steps": 6,
                    "status": "generating"
                }
            }
            
            # Step 5: Implement transformations
            yield {
                "event": "status_update",
                "data": {
                    "message": "Implementing transformations in codebase...",
                    "step": 5,
                    "total_steps": 6,
                    "status": "executing"
                }
            }
            
            implemented_files = await session_platform.implement_transformations(repo_path, transformations)
            
            yield {
                "event": "modifications_applied",
                "data": {
                    "message": f"Implemented {len(implemented_files)} transformations",
                    "applied_files": implemented_files,
                    "step": 5,
                    "total_steps": 6,
                    "status": "executing"
                }
            }
            
            # Step 6: Publish to GitHub
            yield {
                "event": "status_update",
                "data": {
                    "message": "Publishing changes to GitHub...",
                    "step": 6,
                    "total_steps": 6,
                    "status": "deploying"
                }
            }
            
            publish_result = await session_platform.commit_and_publish(
                repo_path,
                session_data["branch_name"],
                session_data["commit_message"],
                session_data["github_token"]
            )
            
            yield {
                "event": "deployment_complete",
                "data": {
                    "message": "Publication completed successfully!",
                    "result": publish_result,
                    "step": 6,
                    "total_steps": 6,
                    "status": "completed"
                }
            }
            
            # Update session status
            session_data["status"] = "completed"
            
        except Exception as e:
            if session_id in active_sessions:
                active_sessions[session_id]["status"] = "failed"
            
            yield {
                "event": "error",
                "data": {
                    "status": "error",
                    "message": f"Generation failed: {str(e)}"
                }
            }
    
    return EventSourceResponse(event_generator())

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            details=str(exc)
        ).dict()
    )

if __name__ == "__main__":
    print("🚀 Starting Intelligent Code Automation Engine Web Interface...")
    print("📱 Open your browser to: http://localhost:8000/ui")
    print("🔧 API docs available at: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 
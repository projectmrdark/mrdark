"""
Sandbox Executor Service
Executes code and commands in isolated environment
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import subprocess
import os
import tempfile
import json

app = FastAPI(
    title="Mr.Dark Sandbox Executor",
    version="1.0.0",
    description="Code execution service for Mr.Dark platform"
)


class CodeExecutionRequest(BaseModel):
    """Code execution request model"""
    code: str
    language: str
    timeout: Optional[int] = 30
    working_dir: Optional[str] = None


class CommandExecutionRequest(BaseModel):
    """Command execution request model"""
    command: str
    timeout: Optional[int] = 30
    working_dir: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Mr.Dark Sandbox Executor",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Sandbox Executor"
    }


@app.post("/execute/code")
async def execute_code(request: CodeExecutionRequest):
    """
    Execute code in the sandbox
    
    Supported languages: python, javascript, bash
    """
    try:
        # Determine executor based on language
        if request.language == "python":
            executor = ["python3"]
            file_ext = ".py"
        elif request.language == "javascript":
            executor = ["node"]
            file_ext = ".js"
        elif request.language == "bash":
            executor = ["bash"]
            file_ext = ".sh"
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language: {request.language}"
            )
        
        # Create temporary file for code
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix=file_ext,
            delete=False
        ) as f:
            f.write(request.code)
            temp_file = f.name
        
        try:
            # Set working directory
            working_dir = request.working_dir or "/workspace/temp"
            os.makedirs(working_dir, exist_ok=True)
            
            # Execute code
            result = subprocess.run(
                executor + [temp_file],
                capture_output=True,
                text=True,
                timeout=request.timeout,
                cwd=working_dir
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "language": request.language
            }
        
        finally:
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=408,
            detail=f"Execution timeout after {request.timeout} seconds"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Execution error: {str(e)}"
        )


@app.post("/execute/command")
async def execute_command(request: CommandExecutionRequest):
    """
    Execute shell command in the sandbox
    """
    try:
        # Set working directory
        working_dir = request.working_dir or "/workspace/temp"
        os.makedirs(working_dir, exist_ok=True)
        
        # Execute command
        result = subprocess.run(
            request.command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=request.timeout,
            cwd=working_dir
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "command": request.command
        }
    
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=408,
            detail=f"Command timeout after {request.timeout} seconds"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Command execution error: {str(e)}"
        )


@app.get("/workspace/info")
async def get_workspace_info():
    """Get workspace information"""
    try:
        workspace_dirs = [
            "/workspace/uploads",
            "/workspace/generated",
            "/workspace/downloads",
            "/workspace/temp"
        ]
        
        info = {}
        for dir_path in workspace_dirs:
            if os.path.exists(dir_path):
                files = os.listdir(dir_path)
                info[dir_path] = {
                    "exists": True,
                    "file_count": len(files),
                    "files": files[:10]  # First 10 files
                }
            else:
                info[dir_path] = {"exists": False}
        
        return {
            "workspace": info,
            "total_dirs": len(workspace_dirs)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting workspace info: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

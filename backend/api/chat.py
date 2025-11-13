"""
Chat API Routes
Handles AI chat interactions using VanChin API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_service import ai_service

router = APIRouter(prefix="/api/chat", tags=["chat"])


class Message(BaseModel):
    """Message model"""
    role: str
    content: str


class ChatRequest(BaseModel):
    """Chat request model"""
    messages: List[Message]
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False


class SimpleChatRequest(BaseModel):
    """Simple chat request model"""
    message: str
    system_prompt: Optional[str] = None


@router.post("/completions")
async def create_chat_completion(request: ChatRequest):
    """
    Create a chat completion
    
    This endpoint uses the VanChin AI API with OpenAI-compatible format
    """
    try:
        # Convert Pydantic models to dicts
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Call AI service
        response = await ai_service.chat_completion(
            messages=messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=request.stream
        )
        
        return {
            "success": True,
            "data": response
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")


@router.post("/simple")
async def simple_chat(request: SimpleChatRequest):
    """
    Simple chat endpoint for quick interactions
    """
    try:
        response = await ai_service.simple_chat(
            user_message=request.message,
            system_prompt=request.system_prompt
        )
        
        return {
            "success": True,
            "response": response
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")


@router.get("/models")
async def get_available_models():
    """
    Get list of available AI models/endpoints
    """
    try:
        models = ai_service.get_available_models()
        return {
            "success": True,
            "models": models,
            "count": len(models)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test")
async def test_ai_connection():
    """
    Test AI service connection
    """
    try:
        response = await ai_service.simple_chat(
            user_message="Hello! Please respond with 'AI service is working correctly.'",
            system_prompt="You are a helpful assistant. Respond exactly as requested."
        )
        
        return {
            "success": True,
            "message": "AI service connection successful",
            "response": response
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service test failed: {str(e)}")

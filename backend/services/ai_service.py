"""
AI Service Module
Integrates with VanChin AI API using OpenAI-compatible format
"""

import os
from typing import List, Dict, Any, Optional
from openai import OpenAI


class AIService:
    """
    AI Service for interacting with VanChin AI API
    Uses OpenAI-compatible API format as specified in requirements
    """
    
    def __init__(self):
        """Initialize AI Service with VanChin API configuration"""
        # Get API key from environment variable VC_API_KEY
        self.api_key = os.environ.get("VC_API_KEY")
        if not self.api_key:
            raise ValueError("VC_API_KEY environment variable is not set")
        
        # Initialize OpenAI client with VanChin base URL
        # IMPORTANT: Do not modify this configuration as per requirements
        self.client = OpenAI(
            base_url="https://vanchin.streamlake.ai/api/gateway/v1/endpoints",
            api_key=self.api_key
        )
        
        # Default model endpoint (ep-xxx format)
        self.default_model = os.environ.get("VC_DEFAULT_MODEL", "ep-lpvcnv-1761467347624133479")
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Create a chat completion using VanChin AI API
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model endpoint ID (ep-xxx format). If None, uses default
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            
        Returns:
            Chat completion response
        """
        # Use provided model or default
        model_id = model or self.default_model
        
        # Ensure model is in ep-xxx format as required
        if not model_id.startswith("ep-"):
            raise ValueError(f"Model must be in ep-xxx format, got: {model_id}")
        
        # Create completion using OpenAI client
        # This follows the exact format specified in requirements
        completion = self.client.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream
        )
        
        if stream:
            return completion
        else:
            return {
                "content": completion.choices[0].message.content,
                "model": model_id,
                "usage": {
                    "prompt_tokens": completion.usage.prompt_tokens if completion.usage else 0,
                    "completion_tokens": completion.usage.completion_tokens if completion.usage else 0,
                    "total_tokens": completion.usage.total_tokens if completion.usage else 0
                },
                "finish_reason": completion.choices[0].finish_reason
            }
    
    async def simple_chat(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        """
        Simple chat interface for quick interactions
        
        Args:
            user_message: User's message
            system_prompt: Optional system prompt
            
        Returns:
            AI response content
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": user_message})
        
        response = await self.chat_completion(messages)
        return response["content"]
    
    def get_available_models(self) -> List[Dict[str, str]]:
        """
        Get list of available API key/model pairs
        Returns the list from the configuration document
        """
        # These are the API key/endpoint pairs from the user's document
        return [
            {"api_key": "WW8GMBSTec_uPhRJQFe5y9OCsYrUKzslQx-LXWKLT9g", "model": "ep-lpvcnv-1761467347624133479"},
            {"api_key": "3gZ9oCeG3sgxUTcfesqhfVnkAOO3JAEJTZWeQKwqzrk", "model": "ep-j9pysc-1761467653839114083"},
            {"api_key": "npthpUsOWQ68u2VibXDmN3IWTM2IGDJeAxQQL1HVQ50", "model": "ep-2uyob4-1761467835762653881"},
            {"api_key": "l1BsR_0ttZ9edaMf9NGBhFzuAfAS64KUmDGAkaz4VBU", "model": "ep-nqjal5-1762460264139958733"},
            {"api_key": "Bt5nUT0GnP20fjZLDKsIvQKW5KOOoU4OsmQrK8SuUE8", "model": "ep-mhsvw6-1762460362477023705"},
            {"api_key": "vsgJFTYUao7OVR7_hfvrbKX2AMykOAEwuwEPomro-zg", "model": "ep-h614n9-1762460436283699679"},
            {"api_key": "pgBW4ALnqV-RtjlC4EICPbOcH_mY4jpQKAu3VXX6Y9k", "model": "ep-ohxawl-1762460514611065743"},
            {"api_key": "cOkB4mwHHjs95szkuOLGyoSRtzTwP2u6-0YBdcQKszI", "model": "ep-bng3os-1762460592040033785"},
            {"api_key": "6quSWJIN9tLotXUQNQypn_U2u6BwvvVLAOk7pgl7ybI", "model": "ep-kazx9x-1761818165668826967"},
            {"api_key": "Co8IQ684LePQeq4t2bCB567d4zFa92N_7zaZLhJqkTo", "model": "ep-6bl8j9-1761818251624808527"},
        ]


# Global AI service instance
ai_service = AIService()

# Mr.Dark AI Agent Platform - AI Agent System & Tool Integration

## 1. AI Agent Architecture Overview

### 1.1 Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI Agent Orchestrator                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           Message Handler & Router                      │    │
│  │  - Receive user message                                │    │
│  │  - Load session context                                │    │
│  │  - Route to appropriate model                          │    │
│  └────────────────────────────────────────────────────────┘    │
│                            ↕                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           Context Manager                               │    │
│  │  - Conversation history                                │    │
│  │  - File attachments                                    │    │
│  │  - Tool execution results                              │    │
│  │  - System prompts                                      │    │
│  │  - Token counting & truncation                         │    │
│  └────────────────────────────────────────────────────────┘    │
│                            ↕                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           Model Interface Layer                         │    │
│  │  - OpenAI API wrapper                                  │    │
│  │  - Anthropic API wrapper                               │    │
│  │  - Google AI API wrapper                               │    │
│  │  - Unified function calling interface                  │    │
│  └────────────────────────────────────────────────────────┘    │
│                            ↕                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           Function Calling Handler                      │    │
│  │  - Parse function calls from model                     │    │
│  │  - Validate parameters                                 │    │
│  │  - Route to tool executor                              │    │
│  │  - Collect results                                     │    │
│  │  - Feed back to model                                  │    │
│  └────────────────────────────────────────────────────────┘    │
│                            ↕                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           Tool Executor                                 │    │
│  │  - Execute tools in sandbox or local                   │    │
│  │  - Handle timeouts & errors                            │    │
│  │  - Collect artifacts                                   │    │
│  │  - Return structured results                           │    │
│  └────────────────────────────────────────────────────────┘    │
│                            ↕                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           Response Streamer                             │    │
│  │  - Stream tokens to client                             │    │
│  │  - Handle tool execution updates                       │    │
│  │  - Send completion signal                              │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Agent Loop Flow

```python
# Pseudocode for agent loop

async def agent_loop(user_message, session_id):
    # 1. Load context
    context = await load_session_context(session_id)
    
    # 2. Add user message to context
    context.add_message(role="user", content=user_message)
    
    # 3. Start streaming response
    stream = await start_stream(session_id)
    
    # 4. Main loop
    max_iterations = 10  # Prevent infinite loops
    for iteration in range(max_iterations):
        # 5. Call AI model
        response = await call_model(
            model=session.model,
            messages=context.to_messages(),
            tools=get_available_tools(),
            stream=True
        )
        
        # 6. Process response
        if response.has_function_calls():
            # 7. Execute tools
            for function_call in response.function_calls:
                # Validate
                validate_function_call(function_call)
                
                # Execute
                result = await execute_tool(
                    tool_name=function_call.name,
                    params=function_call.arguments,
                    mode=session.mode
                )
                
                # Stream tool execution to client
                await stream.send_tool_execution(result)
                
                # Add to context
                context.add_tool_result(function_call, result)
            
            # 8. Continue loop (feed results back to model)
            continue
        
        else:
            # 9. Final response (no more tool calls)
            await stream.send_content(response.content)
            await stream.complete()
            
            # 10. Save to database
            await save_message(
                session_id=session_id,
                role="assistant",
                content=response.content,
                function_calls=context.get_all_function_calls(),
                tool_results=context.get_all_tool_results()
            )
            
            # 11. Update quota
            await update_user_quota(
                user_id=session.user_id,
                tokens=response.usage.total_tokens
            )
            
            break
    
    return response
```

## 2. Model Integration

### 2.1 Supported Models

**OpenAI:**
- `gpt-4` - Most capable, best for complex tasks
- `gpt-4-turbo` - Faster, cheaper, 128K context
- `gpt-3.5-turbo` - Fast, cheap, good for simple tasks

**Anthropic:**
- `claude-3-opus` - Most capable, best reasoning
- `claude-3-sonnet` - Balanced performance/cost
- `claude-3-haiku` - Fastest, cheapest

**Google:**
- `gemini-pro` - Balanced, good multimodal
- `gemini-ultra` - Most capable (when available)

### 2.2 Model Selection Logic

```python
def select_model(user_preference, task_complexity, context_size):
    """
    Auto-select best model based on task requirements
    """
    # User has preference → use it
    if user_preference:
        return user_preference
    
    # Large context → use models with large context window
    if context_size > 100000:
        return "gpt-4-turbo"  # 128K context
    
    # Complex task → use most capable model
    if task_complexity == "high":
        return "gpt-4"  # or claude-3-opus
    
    # Simple task → use fast/cheap model
    if task_complexity == "low":
        return "gpt-3.5-turbo"  # or claude-3-haiku
    
    # Default
    return "gpt-4-turbo"
```

### 2.3 Unified Model Interface

```python
# models/base.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any, AsyncIterator

class BaseModelProvider(ABC):
    """Base class for all model providers"""
    
    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] = None,
        temperature: float = 0.7,
        max_tokens: int = None,
        stream: bool = False
    ) -> AsyncIterator[Dict[str, Any]]:
        """Generate chat completion"""
        pass
    
    @abstractmethod
    def count_tokens(self, messages: List[Dict[str, str]]) -> int:
        """Count tokens in messages"""
        pass
    
    @abstractmethod
    def get_context_window(self) -> int:
        """Get max context window size"""
        pass

# models/openai_provider.py

from openai import AsyncOpenAI

class OpenAIProvider(BaseModelProvider):
    def __init__(self, api_key: str, model: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
    
    async def chat_completion(self, messages, tools=None, **kwargs):
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            **kwargs
        )
        
        if kwargs.get('stream'):
            async for chunk in response:
                yield self._parse_chunk(chunk)
        else:
            yield self._parse_response(response)
    
    def count_tokens(self, messages):
        # Use tiktoken
        import tiktoken
        encoding = tiktoken.encoding_for_model(self.model)
        return sum(len(encoding.encode(msg['content'])) for msg in messages)
    
    def get_context_window(self):
        context_windows = {
            'gpt-4': 8192,
            'gpt-4-turbo': 128000,
            'gpt-3.5-turbo': 16385
        }
        return context_windows.get(self.model, 8192)

# models/anthropic_provider.py

from anthropic import AsyncAnthropic

class AnthropicProvider(BaseModelProvider):
    def __init__(self, api_key: str, model: str):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model
    
    async def chat_completion(self, messages, tools=None, **kwargs):
        # Convert messages format (OpenAI → Anthropic)
        anthropic_messages = self._convert_messages(messages)
        
        response = await self.client.messages.create(
            model=self.model,
            messages=anthropic_messages,
            tools=tools,
            **kwargs
        )
        
        if kwargs.get('stream'):
            async for chunk in response:
                yield self._parse_chunk(chunk)
        else:
            yield self._parse_response(response)
    
    def count_tokens(self, messages):
        # Anthropic's token counting
        return self.client.count_tokens(str(messages))
    
    def get_context_window(self):
        return 200000  # Claude 3 has 200K context

# models/google_provider.py

import google.generativeai as genai

class GoogleProvider(BaseModelProvider):
    def __init__(self, api_key: str, model: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
    
    async def chat_completion(self, messages, tools=None, **kwargs):
        # Convert to Gemini format
        gemini_messages = self._convert_messages(messages)
        
        response = await self.model.generate_content_async(
            gemini_messages,
            tools=tools,
            **kwargs
        )
        
        yield self._parse_response(response)
    
    def count_tokens(self, messages):
        return self.model.count_tokens(str(messages)).total_tokens
    
    def get_context_window(self):
        return 1000000  # Gemini has 1M context
```

### 2.4 Function Calling Schema

```python
# All tools follow this schema for function calling

TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "tool_name",
        "description": "What this tool does",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Description of param1"
                },
                "param2": {
                    "type": "integer",
                    "description": "Description of param2"
                }
            },
            "required": ["param1"]
        }
    }
}
```

## 3. Tool Registry

### 3.1 Tool Categories

**Browser Tools** (from Manus):
- `browser_navigate` - Navigate to URL
- `browser_click` - Click element
- `browser_type` - Type text
- `browser_screenshot` - Take screenshot
- `browser_extract` - Extract data from page
- `browser_wait` - Wait for element
- `browser_scroll` - Scroll page

**Code Execution Tools** (from Manus):
- `execute_python` - Run Python code
- `execute_javascript` - Run JavaScript/Node.js code
- `execute_shell` - Run shell commands
- `execute_bash` - Run bash scripts

**File Tools** (from Manus):
- `file_read` - Read file content
- `file_write` - Write file content
- `file_edit` - Edit file (find & replace)
- `file_delete` - Delete file
- `file_list` - List files in directory
- `file_create_directory` - Create directory
- `file_move` - Move/rename file
- `file_copy` - Copy file

**Search Tools** (from ChatGPT + Manus):
- `web_search` - Search the web
- `image_search` - Search for images
- `news_search` - Search news articles
- `video_search` - Search videos
- `academic_search` - Search academic papers

**Image Generation Tools** (from ChatGPT):
- `generate_image` - Generate image with DALL-E
- `edit_image` - Edit existing image
- `create_variation` - Create image variation

**Data Analysis Tools** (from ChatGPT):
- `analyze_data` - Analyze CSV/Excel data
- `create_chart` - Create visualization
- `statistical_analysis` - Run statistical tests
- `export_data` - Export processed data

**Document Tools**:
- `read_pdf` - Extract text from PDF
- `create_pdf` - Create PDF from content
- `read_docx` - Read Word document
- `create_docx` - Create Word document
- `read_excel` - Read Excel file
- `create_excel` - Create Excel file

**System Tools**:
- `get_current_time` - Get current date/time
- `calculate` - Perform calculation
- `convert_units` - Convert units
- `generate_uuid` - Generate UUID
- `encode_decode` - Encode/decode text

**API Integration Tools**:
- `http_request` - Make HTTP request
- `graphql_query` - Execute GraphQL query
- `rest_api_call` - Call REST API

### 3.2 Tool Implementation Structure

```python
# tools/base.py

from abc import ABC, abstractmethod
from typing import Dict, Any
from pydantic import BaseModel

class ToolParameter(BaseModel):
    """Tool parameter definition"""
    name: str
    type: str
    description: str
    required: bool = False
    default: Any = None

class ToolResult(BaseModel):
    """Tool execution result"""
    success: bool
    result: Any = None
    error: str = None
    artifacts: list = []  # File IDs, URLs, etc.
    metadata: Dict[str, Any] = {}

class BaseTool(ABC):
    """Base class for all tools"""
    
    name: str
    description: str
    parameters: list[ToolParameter]
    category: str
    
    @abstractmethod
    async def execute(
        self,
        params: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ToolResult:
        """Execute the tool"""
        pass
    
    def to_function_schema(self) -> Dict[str, Any]:
        """Convert to OpenAI function calling schema"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        param.name: {
                            "type": param.type,
                            "description": param.description
                        }
                        for param in self.parameters
                    },
                    "required": [
                        param.name 
                        for param in self.parameters 
                        if param.required
                    ]
                }
            }
        }
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate parameters"""
        # Check required params
        for param in self.parameters:
            if param.required and param.name not in params:
                raise ValueError(f"Missing required parameter: {param.name}")
        
        return True

# tools/browser/navigate.py

class BrowserNavigateTool(BaseTool):
    name = "browser_navigate"
    description = "Navigate to a URL in the browser"
    category = "browser"
    parameters = [
        ToolParameter(
            name="url",
            type="string",
            description="The URL to navigate to",
            required=True
        ),
        ToolParameter(
            name="wait_until",
            type="string",
            description="Wait until: load, domcontentloaded, networkidle",
            required=False,
            default="load"
        )
    ]
    
    async def execute(self, params, context):
        try:
            # Get browser instance from context
            browser = context['browser']
            
            # Navigate
            await browser.goto(
                params['url'],
                wait_until=params.get('wait_until', 'load')
            )
            
            # Take screenshot
            screenshot = await browser.screenshot()
            
            # Save screenshot
            screenshot_url = await save_artifact(screenshot, context)
            
            return ToolResult(
                success=True,
                result=f"Navigated to {params['url']}",
                artifacts=[screenshot_url],
                metadata={
                    "url": params['url'],
                    "title": await browser.title()
                }
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e)
            )

# tools/code/execute_python.py

class ExecutePythonTool(BaseTool):
    name = "execute_python"
    description = "Execute Python code in a sandboxed environment"
    category = "code"
    parameters = [
        ToolParameter(
            name="code",
            type="string",
            description="Python code to execute",
            required=True
        ),
        ToolParameter(
            name="timeout",
            type="integer",
            description="Execution timeout in seconds",
            required=False,
            default=30
        )
    ]
    
    async def execute(self, params, context):
        try:
            # Get executor from context (sandbox or local)
            executor = context['executor']
            
            # Execute code
            result = await executor.execute_python(
                code=params['code'],
                timeout=params.get('timeout', 30)
            )
            
            return ToolResult(
                success=result['success'],
                result=result['output'],
                error=result.get('error'),
                artifacts=result.get('files', []),
                metadata={
                    "execution_time": result['duration'],
                    "exit_code": result['exit_code']
                }
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e)
            )

# tools/file/read.py

class FileReadTool(BaseTool):
    name = "file_read"
    description = "Read content of a file"
    category = "file"
    parameters = [
        ToolParameter(
            name="path",
            type="string",
            description="Path to the file to read",
            required=True
        ),
        ToolParameter(
            name="encoding",
            type="string",
            description="File encoding (default: utf-8)",
            required=False,
            default="utf-8"
        )
    ]
    
    async def execute(self, params, context):
        try:
            # Get file system from context
            fs = context['filesystem']
            
            # Read file
            content = await fs.read_file(
                path=params['path'],
                encoding=params.get('encoding', 'utf-8')
            )
            
            return ToolResult(
                success=True,
                result=content,
                metadata={
                    "path": params['path'],
                    "size": len(content)
                }
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e)
            )
```

### 3.3 Tool Registry System

```python
# tools/registry.py

class ToolRegistry:
    """Central registry for all tools"""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._categories: Dict[str, List[str]] = {}
    
    def register(self, tool: BaseTool):
        """Register a tool"""
        self._tools[tool.name] = tool
        
        if tool.category not in self._categories:
            self._categories[tool.category] = []
        self._categories[tool.category].append(tool.name)
    
    def get_tool(self, name: str) -> BaseTool:
        """Get tool by name"""
        if name not in self._tools:
            raise ValueError(f"Tool not found: {name}")
        return self._tools[name]
    
    def get_all_tools(self) -> List[BaseTool]:
        """Get all registered tools"""
        return list(self._tools.values())
    
    def get_tools_by_category(self, category: str) -> List[BaseTool]:
        """Get tools by category"""
        if category not in self._categories:
            return []
        return [self._tools[name] for name in self._categories[category]]
    
    def get_function_schemas(self) -> List[Dict[str, Any]]:
        """Get all tools as function calling schemas"""
        return [tool.to_function_schema() for tool in self._tools.values()]
    
    def get_filtered_schemas(
        self,
        categories: List[str] = None,
        exclude: List[str] = None
    ) -> List[Dict[str, Any]]:
        """Get filtered function schemas"""
        tools = self.get_all_tools()
        
        if categories:
            tools = [t for t in tools if t.category in categories]
        
        if exclude:
            tools = [t for t in tools if t.name not in exclude]
        
        return [tool.to_function_schema() for tool in tools]

# Initialize global registry
tool_registry = ToolRegistry()

# Register all tools
from tools.browser import *
from tools.code import *
from tools.file import *
from tools.search import *
# ... etc

tool_registry.register(BrowserNavigateTool())
tool_registry.register(ExecutePythonTool())
tool_registry.register(FileReadTool())
# ... etc
```

## 4. Context Management

### 4.1 Context Structure

```python
# agent/context.py

from typing import List, Dict, Any
from pydantic import BaseModel

class Message(BaseModel):
    role: str  # user, assistant, system, tool
    content: str
    name: str = None  # For tool messages
    function_call: Dict[str, Any] = None
    tool_calls: List[Dict[str, Any]] = None

class Context:
    """Manages conversation context"""
    
    def __init__(
        self,
        session_id: str,
        model: str,
        max_tokens: int = None
    ):
        self.session_id = session_id
        self.model = model
        self.max_tokens = max_tokens or self._get_default_max_tokens()
        
        self.messages: List[Message] = []
        self.system_prompt: str = self._get_system_prompt()
        self.total_tokens: int = 0
    
    def add_message(self, role: str, content: str, **kwargs):
        """Add message to context"""
        message = Message(role=role, content=content, **kwargs)
        self.messages.append(message)
        self._update_token_count()
    
    def add_tool_result(self, function_call: Dict, result: ToolResult):
        """Add tool execution result"""
        self.messages.append(Message(
            role="tool",
            name=function_call['name'],
            content=str(result.result) if result.success else result.error
        ))
        self._update_token_count()
    
    def to_messages(self) -> List[Dict[str, Any]]:
        """Convert to API format"""
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        for msg in self.messages:
            messages.append(msg.dict(exclude_none=True))
        
        # Truncate if needed
        if self.total_tokens > self.max_tokens:
            messages = self._truncate_messages(messages)
        
        return messages
    
    def _truncate_messages(self, messages: List[Dict]) -> List[Dict]:
        """Truncate old messages to fit context window"""
        # Keep system prompt and last N messages
        system = messages[0]
        recent = messages[-10:]  # Keep last 10 messages
        
        # Add summary of truncated messages
        summary = {
            "role": "system",
            "content": "[Previous messages summarized for context length]"
        }
        
        return [system, summary] + recent
    
    def _update_token_count(self):
        """Update token count"""
        # Use model-specific tokenizer
        from models import get_provider
        provider = get_provider(self.model)
        self.total_tokens = provider.count_tokens(self.to_messages())
    
    def _get_system_prompt(self) -> str:
        """Get system prompt"""
        return """You are Mr.Dark, an advanced AI agent with access to powerful tools.

You can:
- Browse the web and extract information
- Execute code in Python, JavaScript, and other languages
- Read, write, and edit files
- Search for information, images, and news
- Generate and edit images
- Analyze data and create visualizations
- And much more

When a user asks you to do something:
1. Think about which tools you need
2. Use the tools to accomplish the task
3. Provide a clear, helpful response

Always be professional, accurate, and helpful. If you're unsure about something, say so.
If a task requires multiple steps, break it down and execute them one by one.
"""
    
    def _get_default_max_tokens(self) -> int:
        """Get default max tokens for model"""
        # Reserve some tokens for response
        context_windows = {
            'gpt-4': 6000,  # 8K - 2K for response
            'gpt-4-turbo': 120000,  # 128K - 8K for response
            'gpt-3.5-turbo': 14000,  # 16K - 2K for response
            'claude-3-opus': 180000,  # 200K - 20K for response
            'gemini-pro': 900000  # 1M - 100K for response
        }
        return context_windows.get(self.model, 6000)
```

### 4.2 Context Optimization Strategies

**Token Management:**
- Count tokens accurately using model-specific tokenizers
- Truncate old messages when approaching limit
- Summarize truncated messages with AI
- Prioritize recent messages and tool results

**Message Compression:**
- Remove redundant information
- Compress tool results (keep only essential data)
- Use references instead of full content for large files

**Smart Truncation:**
- Keep system prompt always
- Keep last N user/assistant exchanges
- Keep recent tool calls and results
- Summarize middle messages

## 5. Streaming Implementation

### 5.1 Server-Sent Events (SSE)

```python
# api/streaming.py

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import json

router = APIRouter()

@router.post("/sessions/{session_id}/stream")
async def stream_message(session_id: str, message: str):
    """Stream AI response"""
    
    async def event_generator():
        try:
            # Send start event
            yield f"data: {json.dumps({'type': 'start'})}\n\n"
            
            # Run agent loop
            async for event in agent_loop_stream(session_id, message):
                # Send event to client
                yield f"data: {json.dumps(event)}\n\n"
                
                # Small delay to prevent overwhelming client
                await asyncio.sleep(0.01)
            
            # Send end event
            yield f"data: {json.dumps({'type': 'end'})}\n\n"
        
        except Exception as e:
            # Send error event
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

async def agent_loop_stream(session_id: str, message: str):
    """Agent loop with streaming"""
    
    # Load context
    context = await load_context(session_id)
    context.add_message("user", message)
    
    # Stream response
    async for chunk in call_model_stream(context):
        if chunk['type'] == 'content':
            # Text chunk
            yield {
                'type': 'content',
                'delta': chunk['delta']
            }
        
        elif chunk['type'] == 'function_call':
            # Tool execution
            yield {
                'type': 'tool_start',
                'tool': chunk['name'],
                'params': chunk['arguments']
            }
            
            # Execute tool
            result = await execute_tool(chunk['name'], chunk['arguments'])
            
            yield {
                'type': 'tool_end',
                'tool': chunk['name'],
                'result': result.dict()
            }
            
            # Feed back to model
            context.add_tool_result(chunk, result)
```

### 5.2 WebSocket Implementation

```python
# api/websocket.py

from fastapi import WebSocket, WebSocketDisconnect
import json

class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
    
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
    
    async def send_message(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            # Process message
            if data['type'] == 'message':
                # Run agent loop
                async for event in agent_loop_stream(session_id, data['content']):
                    await manager.send_message(session_id, event)
            
            elif data['type'] == 'cancel':
                # Cancel current execution
                await cancel_execution(session_id)
    
    except WebSocketDisconnect:
        manager.disconnect(session_id)
```

## 6. Error Handling & Retry Logic

### 6.1 Error Types

```python
# errors.py

class AgentError(Exception):
    """Base exception for agent errors"""
    pass

class ModelError(AgentError):
    """Error from AI model"""
    pass

class ToolExecutionError(AgentError):
    """Error during tool execution"""
    pass

class QuotaExceededError(AgentError):
    """User quota exceeded"""
    pass

class RateLimitError(AgentError):
    """API rate limit exceeded"""
    pass

class ValidationError(AgentError):
    """Parameter validation error"""
    pass
```

### 6.2 Retry Strategy

```python
# utils/retry.py

import asyncio
from functools import wraps

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0
):
    """Retry decorator with exponential backoff"""
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                
                except RateLimitError as e:
                    if attempt == max_retries - 1:
                        raise
                    
                    # Exponential backoff
                    delay = min(
                        base_delay * (exponential_base ** attempt),
                        max_delay
                    )
                    
                    await asyncio.sleep(delay)
                
                except ModelError as e:
                    # Don't retry model errors (usually permanent)
                    raise
                
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    
                    # Linear backoff for other errors
                    await asyncio.sleep(base_delay)
        
        return wrapper
    return decorator

# Usage
@retry_with_backoff(max_retries=3)
async def call_model_with_retry(context):
    return await call_model(context)
```

### 6.3 Graceful Degradation

```python
# agent/fallback.py

async def call_model_with_fallback(context):
    """Call model with fallback to alternative models"""
    
    # Try primary model
    try:
        return await call_model(context.model, context)
    
    except RateLimitError:
        # Try fallback model
        fallback_models = {
            'gpt-4': 'gpt-4-turbo',
            'gpt-4-turbo': 'gpt-3.5-turbo',
            'claude-3-opus': 'claude-3-sonnet',
            'claude-3-sonnet': 'claude-3-haiku'
        }
        
        fallback = fallback_models.get(context.model)
        if fallback:
            return await call_model(fallback, context)
        
        raise
    
    except ModelError as e:
        # Log error and try alternative provider
        if 'openai' in context.model:
            # Try Anthropic
            return await call_model('claude-3-sonnet', context)
        
        raise
```

## 7. Performance Optimization

### 7.1 Caching

```python
# cache/response_cache.py

import hashlib
import json
from redis import Redis

redis_client = Redis()

def cache_key(messages: List[Dict]) -> str:
    """Generate cache key from messages"""
    content = json.dumps(messages, sort_keys=True)
    return f"response:{hashlib.sha256(content.encode()).hexdigest()}"

async def get_cached_response(messages: List[Dict]) -> Optional[str]:
    """Get cached response"""
    key = cache_key(messages)
    cached = redis_client.get(key)
    
    if cached:
        return json.loads(cached)
    
    return None

async def cache_response(messages: List[Dict], response: str):
    """Cache response"""
    key = cache_key(messages)
    redis_client.setex(
        key,
        3600,  # 1 hour TTL
        json.dumps(response)
    )
```

### 7.2 Parallel Tool Execution

```python
# agent/parallel_execution.py

async def execute_tools_parallel(function_calls: List[Dict], context):
    """Execute multiple tools in parallel"""
    
    # Create tasks
    tasks = [
        execute_tool(call['name'], call['arguments'], context)
        for call in function_calls
    ]
    
    # Run in parallel
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle results
    tool_results = []
    for call, result in zip(function_calls, results):
        if isinstance(result, Exception):
            tool_results.append(ToolResult(
                success=False,
                error=str(result)
            ))
        else:
            tool_results.append(result)
    
    return tool_results
```

### 7.3 Request Batching

```python
# agent/batching.py

class RequestBatcher:
    """Batch multiple requests to reduce API calls"""
    
    def __init__(self, batch_size: int = 5, wait_time: float = 0.1):
        self.batch_size = batch_size
        self.wait_time = wait_time
        self.queue = []
        self.processing = False
    
    async def add_request(self, request):
        """Add request to batch"""
        self.queue.append(request)
        
        if len(self.queue) >= self.batch_size:
            await self.process_batch()
        
        elif not self.processing:
            # Wait for more requests
            self.processing = True
            await asyncio.sleep(self.wait_time)
            await self.process_batch()
    
    async def process_batch(self):
        """Process batched requests"""
        if not self.queue:
            return
        
        batch = self.queue[:self.batch_size]
        self.queue = self.queue[self.batch_size:]
        
        # Process batch
        results = await process_requests_batch(batch)
        
        # Return results to requesters
        for request, result in zip(batch, results):
            request.set_result(result)
        
        self.processing = False
```

## 8. Monitoring & Logging

### 8.1 Structured Logging

```python
# utils/logging.py

import logging
import json
from datetime import datetime

class StructuredLogger:
    """Structured JSON logging"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def log(self, level: str, message: str, **kwargs):
        """Log structured message"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            **kwargs
        }
        
        self.logger.log(
            getattr(logging, level.upper()),
            json.dumps(log_entry)
        )
    
    def info(self, message: str, **kwargs):
        self.log("info", message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self.log("error", message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self.log("warning", message, **kwargs)

# Usage
logger = StructuredLogger("agent")

logger.info(
    "Tool executed",
    tool="browser_navigate",
    session_id="123",
    duration_ms=1234,
    success=True
)
```

### 8.2 Performance Metrics

```python
# monitoring/metrics.py

from prometheus_client import Counter, Histogram, Gauge

# Counters
requests_total = Counter(
    'agent_requests_total',
    'Total agent requests',
    ['model', 'status']
)

tool_executions_total = Counter(
    'tool_executions_total',
    'Total tool executions',
    ['tool', 'status']
)

# Histograms
request_duration = Histogram(
    'agent_request_duration_seconds',
    'Agent request duration',
    ['model']
)

tool_execution_duration = Histogram(
    'tool_execution_duration_seconds',
    'Tool execution duration',
    ['tool']
)

# Gauges
active_sessions = Gauge(
    'agent_active_sessions',
    'Number of active sessions'
)

# Usage
with request_duration.labels(model='gpt-4').time():
    response = await call_model(context)
    requests_total.labels(model='gpt-4', status='success').inc()
```

---

**Document Version**: 1.0  
**Last Updated**: 2024-01-XX  
**Status**: Draft - Pending Review

# Mr.Dark AI Agent Platform - Sandbox & Local Connection System

## 1. Execution Modes Overview

### 1.1 Mode Comparison

| Feature | Sandbox Mode | Local Connection Mode |
|---------|--------------|----------------------|
| **Execution Location** | Server (Docker containers) | User's local machine |
| **Setup Required** | None (instant) | Download & install client |
| **Resource Limits** | Platform-defined (CPU, RAM, disk) | User's machine limits |
| **File Access** | Session workspace only | User-selected directory |
| **Network Access** | Restricted | User's network |
| **Privacy** | Code runs on our servers | Code runs locally |
| **Cost** | Platform bears cost | User bears compute cost |
| **Persistence** | Hibernation support | Always available |
| **Best For** | Quick tasks, new users | Heavy workloads, privacy-sensitive |

### 1.2 Mode Selection Logic

```python
def recommend_execution_mode(task_type, user_preference, has_local_client):
    """Recommend execution mode based on task and user"""
    
    # User preference takes priority
    if user_preference:
        return user_preference
    
    # Heavy computation → recommend local
    if task_type in ['data_analysis', 'video_processing', 'ml_training']:
        return 'local' if has_local_client else 'sandbox'
    
    # Privacy-sensitive → recommend local
    if task_type in ['personal_data', 'credentials', 'private_files']:
        return 'local' if has_local_client else 'sandbox'
    
    # Quick tasks → sandbox
    if task_type in ['web_search', 'simple_code', 'text_processing']:
        return 'sandbox'
    
    # Default to sandbox (easier for users)
    return 'sandbox'
```

## 2. Sandbox System Architecture

### 2.1 Container Design

```
┌─────────────────────────────────────────────────────────────────┐
│                    Sandbox Container                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Base Image: ubuntu:22.04                                        │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Runtime Environments                                   │    │
│  │  - Python 3.11 + pip                                   │    │
│  │  - Node.js 20 + pnpm                                   │    │
│  │  - Bash/Shell                                          │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Browser Automation                                     │    │
│  │  - Playwright                                          │    │
│  │  - Chromium browser                                    │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Common Tools                                           │    │
│  │  - git, curl, wget                                     │    │
│  │  - ffmpeg (video/audio)                                │    │
│  │  - imagemagick (image processing)                      │    │
│  │  - pandoc (document conversion)                        │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Python Packages (pre-installed)                       │    │
│  │  - pandas, numpy, matplotlib                           │    │
│  │  - requests, beautifulsoup4                            │    │
│  │  - pillow, opencv-python                               │    │
│  │  - scikit-learn, tensorflow                            │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  File System                                            │    │
│  │  /workspace (mounted volume)                           │    │
│  │    ├── uploads/      (user uploaded files)            │    │
│  │    ├── generated/    (AI generated files)             │    │
│  │    ├── downloads/    (browser downloads)              │    │
│  │    └── temp/         (temporary files)                │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Agent Executor Service (FastAPI)                      │    │
│  │  - Listens on port 8000                                │    │
│  │  - Receives tool execution requests                    │    │
│  │  - Executes commands                                   │    │
│  │  - Returns results + artifacts                         │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  Resource Limits:                                                │
│  - CPU: 2 cores                                                  │
│  - Memory: 4GB                                                   │
│  - Disk: 10GB                                                    │
│  - Network: 100Mbps                                              │
│  - Execution timeout: 5 minutes per command                      │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Dockerfile

```dockerfile
# Dockerfile for sandbox container

FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    nodejs \
    npm \
    git \
    curl \
    wget \
    ffmpeg \
    imagemagick \
    pandoc \
    chromium-browser \
    chromium-chromedriver \
    && rm -rf /var/lib/apt/lists/*

# Install pnpm
RUN npm install -g pnpm

# Install Python packages
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Install Playwright
RUN pip3 install playwright && \
    playwright install chromium && \
    playwright install-deps

# Create workspace directory
RUN mkdir -p /workspace/{uploads,generated,downloads,temp}

# Copy executor service
COPY executor/ /app/executor/
WORKDIR /app

# Install executor dependencies
RUN pip3 install -r executor/requirements.txt

# Expose executor port
EXPOSE 8000

# Run executor service
CMD ["uvicorn", "executor.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2.3 Container Orchestration

```python
# sandbox/orchestrator.py

import docker
import asyncio
from typing import Dict, Optional
from datetime import datetime, timedelta

class SandboxOrchestrator:
    """Manages sandbox containers"""
    
    def __init__(self):
        self.docker_client = docker.from_env()
        self.active_containers: Dict[str, Container] = {}
        self.hibernation_timeout = timedelta(minutes=5)
    
    async def create_container(self, session_id: str) -> str:
        """Create new sandbox container"""
        
        # Generate container name
        container_name = f"sandbox-{session_id}"
        
        # Create volume for workspace
        volume_name = f"workspace-{session_id}"
        volume = self.docker_client.volumes.create(name=volume_name)
        
        # Create container
        container = self.docker_client.containers.run(
            image="mrdark-sandbox:latest",
            name=container_name,
            detach=True,
            remove=False,  # Don't auto-remove
            volumes={
                volume_name: {
                    'bind': '/workspace',
                    'mode': 'rw'
                }
            },
            mem_limit="4g",
            cpu_count=2,
            network_mode="bridge",
            environment={
                "SESSION_ID": session_id
            }
        )
        
        # Wait for container to be ready
        await self._wait_for_ready(container)
        
        # Store in active containers
        self.active_containers[session_id] = Container(
            id=container.id,
            name=container_name,
            session_id=session_id,
            created_at=datetime.utcnow(),
            last_activity=datetime.utcnow()
        )
        
        # Save to database
        await self._save_container_to_db(session_id, container)
        
        return container.id
    
    async def get_container(self, session_id: str) -> Optional[str]:
        """Get container for session (create if not exists)"""
        
        # Check if already running
        if session_id in self.active_containers:
            container = self.active_containers[session_id]
            container.last_activity = datetime.utcnow()
            return container.id
        
        # Check if hibernated
        db_container = await self._get_container_from_db(session_id)
        if db_container and db_container.status == 'hibernated':
            # Resume from hibernation
            return await self.resume_container(session_id)
        
        # Create new container
        return await self.create_container(session_id)
    
    async def hibernate_container(self, session_id: str):
        """Hibernate container to save resources"""
        
        if session_id not in self.active_containers:
            return
        
        container_info = self.active_containers[session_id]
        container = self.docker_client.containers.get(container_info.id)
        
        # Save workspace to S3
        workspace_snapshot = await self._snapshot_workspace(session_id)
        
        # Stop container
        container.stop()
        
        # Update database
        await self._update_container_status(
            session_id,
            status='hibernated',
            snapshot_url=workspace_snapshot
        )
        
        # Remove from active containers
        del self.active_containers[session_id]
    
    async def resume_container(self, session_id: str) -> str:
        """Resume hibernated container"""
        
        # Get container info from DB
        db_container = await self._get_container_from_db(session_id)
        
        # Restore workspace from S3
        await self._restore_workspace(session_id, db_container.snapshot_url)
        
        # Start container
        container = self.docker_client.containers.get(db_container.container_id)
        container.start()
        
        # Wait for ready
        await self._wait_for_ready(container)
        
        # Add to active containers
        self.active_containers[session_id] = Container(
            id=container.id,
            name=db_container.container_name,
            session_id=session_id,
            created_at=db_container.created_at,
            last_activity=datetime.utcnow()
        )
        
        # Update database
        await self._update_container_status(session_id, status='running')
        
        return container.id
    
    async def destroy_container(self, session_id: str):
        """Destroy container and cleanup"""
        
        if session_id in self.active_containers:
            container_info = self.active_containers[session_id]
            container = self.docker_client.containers.get(container_info.id)
            
            # Stop and remove container
            container.stop()
            container.remove()
            
            # Remove volume
            volume_name = f"workspace-{session_id}"
            try:
                volume = self.docker_client.volumes.get(volume_name)
                volume.remove()
            except:
                pass
            
            # Remove from active containers
            del self.active_containers[session_id]
        
        # Update database
        await self._update_container_status(session_id, status='destroyed')
    
    async def cleanup_idle_containers(self):
        """Cleanup idle containers (background task)"""
        
        while True:
            now = datetime.utcnow()
            
            for session_id, container in list(self.active_containers.items()):
                # Check if idle
                idle_time = now - container.last_activity
                
                if idle_time > self.hibernation_timeout:
                    # Hibernate idle container
                    await self.hibernate_container(session_id)
            
            # Run every minute
            await asyncio.sleep(60)
    
    async def _wait_for_ready(self, container, timeout: int = 30):
        """Wait for container to be ready"""
        
        start_time = datetime.utcnow()
        
        while True:
            # Check if container is running
            container.reload()
            if container.status == 'running':
                # Try to connect to executor service
                try:
                    # Get container IP
                    ip = container.attrs['NetworkSettings']['IPAddress']
                    
                    # Try health check
                    import httpx
                    async with httpx.AsyncClient() as client:
                        response = await client.get(f"http://{ip}:8000/health")
                        if response.status_code == 200:
                            return True
                except:
                    pass
            
            # Check timeout
            if (datetime.utcnow() - start_time).seconds > timeout:
                raise TimeoutError("Container failed to start")
            
            await asyncio.sleep(1)
    
    async def _snapshot_workspace(self, session_id: str) -> str:
        """Snapshot workspace to S3"""
        
        # Create tar archive of workspace
        volume_name = f"workspace-{session_id}"
        archive_path = f"/tmp/workspace-{session_id}.tar.gz"
        
        # Use docker cp to extract volume
        container = self.docker_client.containers.get(
            self.active_containers[session_id].id
        )
        
        # Create archive
        import tarfile
        with tarfile.open(archive_path, 'w:gz') as tar:
            # ... tar workspace files
            pass
        
        # Upload to S3
        from storage import upload_to_s3
        s3_url = await upload_to_s3(archive_path, f"snapshots/{session_id}.tar.gz")
        
        return s3_url
    
    async def _restore_workspace(self, session_id: str, snapshot_url: str):
        """Restore workspace from S3"""
        
        # Download from S3
        from storage import download_from_s3
        archive_path = f"/tmp/workspace-{session_id}.tar.gz"
        await download_from_s3(snapshot_url, archive_path)
        
        # Extract to volume
        # ... extract tar archive
        pass
```

### 2.4 Executor Service

```python
# executor/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import subprocess
from typing import Dict, Any, List

app = FastAPI()

class ExecuteRequest(BaseModel):
    command: str
    language: str  # python, javascript, bash
    timeout: int = 30
    cwd: str = "/workspace"

class ExecuteResponse(BaseModel):
    success: bool
    output: str
    error: str = None
    exit_code: int
    duration: float
    files: List[str] = []

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/execute", response_model=ExecuteResponse)
async def execute_code(request: ExecuteRequest):
    """Execute code in sandbox"""
    
    try:
        # Prepare command
        if request.language == "python":
            cmd = ["python3", "-c", request.command]
        elif request.language == "javascript":
            cmd = ["node", "-e", request.command]
        elif request.language == "bash":
            cmd = ["bash", "-c", request.command]
        else:
            raise ValueError(f"Unsupported language: {request.language}")
        
        # Execute with timeout
        start_time = asyncio.get_event_loop().time()
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=request.cwd
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=request.timeout
            )
        except asyncio.TimeoutError:
            process.kill()
            raise HTTPException(
                status_code=408,
                detail="Execution timeout"
            )
        
        duration = asyncio.get_event_loop().time() - start_time
        
        # Collect generated files
        files = await list_new_files(request.cwd, start_time)
        
        return ExecuteResponse(
            success=process.returncode == 0,
            output=stdout.decode('utf-8'),
            error=stderr.decode('utf-8') if stderr else None,
            exit_code=process.returncode,
            duration=duration,
            files=files
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/browser/navigate")
async def browser_navigate(url: str):
    """Navigate browser to URL"""
    
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto(url)
        
        # Take screenshot
        screenshot_path = f"/workspace/screenshots/{int(time.time())}.png"
        await page.screenshot(path=screenshot_path)
        
        # Get page info
        title = await page.title()
        html = await page.content()
        
        await browser.close()
        
        return {
            "url": url,
            "title": title,
            "screenshot": screenshot_path,
            "html_length": len(html)
        }

@app.post("/file/read")
async def read_file(path: str):
    """Read file from workspace"""
    
    import os
    
    # Security: ensure path is within workspace
    abs_path = os.path.abspath(os.path.join("/workspace", path))
    if not abs_path.startswith("/workspace"):
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        with open(abs_path, 'r') as f:
            content = f.read()
        
        return {
            "path": path,
            "content": content,
            "size": len(content)
        }
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/file/write")
async def write_file(path: str, content: str):
    """Write file to workspace"""
    
    import os
    
    # Security check
    abs_path = os.path.abspath(os.path.join("/workspace", path))
    if not abs_path.startswith("/workspace"):
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        # Create directory if needed
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        
        with open(abs_path, 'w') as f:
            f.write(content)
        
        return {
            "path": path,
            "size": len(content)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def list_new_files(directory: str, since: float) -> List[str]:
    """List files created since timestamp"""
    
    import os
    
    new_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.getctime(filepath) > since:
                new_files.append(filepath)
    
    return new_files
```

## 3. Local Connection System

### 3.1 Local Client Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  Mr.Dark Local Client                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Platform: Electron (cross-platform desktop app)                 │
│  OR: Python CLI (for advanced users)                             │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  UI Layer (Electron only)                              │    │
│  │  - System tray icon                                    │    │
│  │  - Settings window                                     │    │
│  │  - Status dashboard                                    │    │
│  │  - Logs viewer                                         │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  WebSocket Client                                       │    │
│  │  - Connect to platform                                 │    │
│  │  - Authenticate with token                             │    │
│  │  - Receive commands                                    │    │
│  │  - Send results                                        │    │
│  │  - Auto-reconnect on disconnect                        │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Command Executor                                       │    │
│  │  - Execute Python code                                 │    │
│  │  - Execute JavaScript/Node.js code                     │    │
│  │  - Execute shell commands                              │    │
│  │  - Browser automation (Playwright)                     │    │
│  │  - File operations                                     │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Security Sandbox                                       │    │
│  │  - Restricted file access (workspace only)             │    │
│  │  - Command whitelist/blacklist                         │    │
│  │  - Resource limits                                     │    │
│  │  - User confirmation for sensitive ops                 │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  File Sync                                              │    │
│  │  - Watch workspace directory                           │    │
│  │  - Upload new/modified files                           │    │
│  │  - Download artifacts from platform                    │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Configuration                                          │    │
│  │  - Auth token                                          │    │
│  │  - Workspace path                                      │    │
│  │  - Allowed commands                                    │    │
│  │  - Resource limits                                     │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Local Client Implementation (Python)

```python
# local_client/main.py

import asyncio
import websockets
import json
import subprocess
import os
from pathlib import Path
from typing import Dict, Any

class MrDarkLocalClient:
    """Local client for Mr.Dark platform"""
    
    def __init__(self, config_path: str = "~/.mrdark/config.json"):
        self.config_path = Path(config_path).expanduser()
        self.config = self.load_config()
        self.ws = None
        self.running = False
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration"""
        
        if not self.config_path.exists():
            # First-time setup
            return self.setup_wizard()
        
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def setup_wizard(self) -> Dict[str, Any]:
        """Interactive setup wizard"""
        
        print("=== Mr.Dark Local Client Setup ===\n")
        
        # Get auth token
        print("1. Go to https://mrdark.app/settings/local-client")
        print("2. Generate a new connection token")
        print("3. Copy the token and paste it here:\n")
        
        auth_token = input("Auth Token: ").strip()
        
        # Get workspace path
        default_workspace = str(Path.home() / "MrDark")
        workspace = input(f"Workspace directory [{default_workspace}]: ").strip()
        workspace = workspace or default_workspace
        
        # Create workspace
        Path(workspace).mkdir(parents=True, exist_ok=True)
        
        # Save config
        config = {
            "auth_token": auth_token,
            "workspace_path": workspace,
            "server_url": "wss://api.mrdark.app/ws/local",
            "allowed_commands": ["python", "node", "npm", "git"],
            "max_execution_time": 300,  # 5 minutes
            "auto_reconnect": True
        }
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n✓ Configuration saved to {self.config_path}")
        print(f"✓ Workspace: {workspace}\n")
        
        return config
    
    async def connect(self):
        """Connect to platform"""
        
        print(f"Connecting to {self.config['server_url']}...")
        
        headers = {
            "Authorization": f"Bearer {self.config['auth_token']}"
        }
        
        try:
            self.ws = await websockets.connect(
                self.config['server_url'],
                extra_headers=headers
            )
            
            print("✓ Connected to Mr.Dark platform")
            self.running = True
            
            # Start message loop
            await self.message_loop()
        
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            
            if self.config.get('auto_reconnect'):
                print("Retrying in 5 seconds...")
                await asyncio.sleep(5)
                await self.connect()
    
    async def message_loop(self):
        """Main message loop"""
        
        try:
            async for message in self.ws:
                data = json.loads(message)
                
                # Handle different message types
                if data['type'] == 'execute':
                    await self.handle_execute(data)
                
                elif data['type'] == 'file_read':
                    await self.handle_file_read(data)
                
                elif data['type'] == 'file_write':
                    await self.handle_file_write(data)
                
                elif data['type'] == 'ping':
                    await self.send_message({'type': 'pong'})
        
        except websockets.exceptions.ConnectionClosed:
            print("✗ Connection closed")
            self.running = False
            
            if self.config.get('auto_reconnect'):
                print("Reconnecting...")
                await self.connect()
    
    async def handle_execute(self, data: Dict[str, Any]):
        """Handle code execution request"""
        
        command = data['command']
        language = data['language']
        request_id = data['request_id']
        
        print(f"\n→ Executing {language} code...")
        
        # Check if command is allowed
        if not self.is_command_allowed(command):
            await self.send_result(request_id, {
                'success': False,
                'error': 'Command not allowed'
            })
            return
        
        # Execute
        try:
            result = await self.execute_code(command, language)
            await self.send_result(request_id, result)
            print(f"✓ Execution completed")
        
        except Exception as e:
            await self.send_result(request_id, {
                'success': False,
                'error': str(e)
            })
            print(f"✗ Execution failed: {e}")
    
    async def execute_code(
        self,
        code: str,
        language: str
    ) -> Dict[str, Any]:
        """Execute code locally"""
        
        # Prepare command
        if language == "python":
            cmd = ["python3", "-c", code]
        elif language == "javascript":
            cmd = ["node", "-e", code]
        elif language == "bash":
            cmd = ["bash", "-c", code]
        else:
            raise ValueError(f"Unsupported language: {language}")
        
        # Execute
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.config['workspace_path']
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.config['max_execution_time']
            )
        except asyncio.TimeoutError:
            process.kill()
            raise TimeoutError("Execution timeout")
        
        return {
            'success': process.returncode == 0,
            'output': stdout.decode('utf-8'),
            'error': stderr.decode('utf-8') if stderr else None,
            'exit_code': process.returncode
        }
    
    async def handle_file_read(self, data: Dict[str, Any]):
        """Handle file read request"""
        
        path = data['path']
        request_id = data['request_id']
        
        # Security: ensure path is within workspace
        abs_path = Path(self.config['workspace_path']) / path
        if not abs_path.resolve().is_relative_to(
            Path(self.config['workspace_path']).resolve()
        ):
            await self.send_result(request_id, {
                'success': False,
                'error': 'Access denied'
            })
            return
        
        try:
            with open(abs_path, 'r') as f:
                content = f.read()
            
            await self.send_result(request_id, {
                'success': True,
                'content': content
            })
        
        except Exception as e:
            await self.send_result(request_id, {
                'success': False,
                'error': str(e)
            })
    
    async def handle_file_write(self, data: Dict[str, Any]):
        """Handle file write request"""
        
        path = data['path']
        content = data['content']
        request_id = data['request_id']
        
        # Security check
        abs_path = Path(self.config['workspace_path']) / path
        if not abs_path.resolve().is_relative_to(
            Path(self.config['workspace_path']).resolve()
        ):
            await self.send_result(request_id, {
                'success': False,
                'error': 'Access denied'
            })
            return
        
        try:
            abs_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(abs_path, 'w') as f:
                f.write(content)
            
            await self.send_result(request_id, {
                'success': True
            })
        
        except Exception as e:
            await self.send_result(request_id, {
                'success': False,
                'error': str(e)
            })
    
    def is_command_allowed(self, command: str) -> bool:
        """Check if command is allowed"""
        
        # Extract base command
        base_cmd = command.split()[0] if command else ""
        
        # Check whitelist
        allowed = self.config.get('allowed_commands', [])
        
        if not allowed:  # Empty whitelist = allow all
            return True
        
        return base_cmd in allowed
    
    async def send_message(self, data: Dict[str, Any]):
        """Send message to platform"""
        await self.ws.send(json.dumps(data))
    
    async def send_result(self, request_id: str, result: Dict[str, Any]):
        """Send execution result"""
        await self.send_message({
            'type': 'result',
            'request_id': request_id,
            'result': result
        })
    
    def run(self):
        """Run client"""
        asyncio.run(self.connect())

if __name__ == "__main__":
    client = MrDarkLocalClient()
    client.run()
```

### 3.3 Platform-Side Local Connection Handler

```python
# api/local_connection.py

from fastapi import WebSocket, WebSocketDisconnect, Depends
from typing import Dict
import asyncio
import uuid

class LocalConnectionManager:
    """Manage local client connections"""
    
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}
        self.pending_requests: Dict[str, asyncio.Future] = {}
    
    async def connect(
        self,
        websocket: WebSocket,
        user_id: str,
        client_id: str
    ):
        """Accept local client connection"""
        
        await websocket.accept()
        self.connections[client_id] = websocket
        
        # Update database
        await update_local_client_status(client_id, connected=True)
        
        print(f"Local client {client_id} connected")
    
    def disconnect(self, client_id: str):
        """Handle client disconnect"""
        
        if client_id in self.connections:
            del self.connections[client_id]
        
        # Update database
        asyncio.create_task(
            update_local_client_status(client_id, connected=False)
        )
        
        print(f"Local client {client_id} disconnected")
    
    async def execute_command(
        self,
        client_id: str,
        command: str,
        language: str,
        timeout: int = 30
    ) -> Dict:
        """Execute command on local client"""
        
        if client_id not in self.connections:
            raise ValueError("Client not connected")
        
        # Generate request ID
        request_id = str(uuid.uuid4())
        
        # Create future for result
        future = asyncio.Future()
        self.pending_requests[request_id] = future
        
        # Send command to client
        await self.connections[client_id].send_json({
            'type': 'execute',
            'request_id': request_id,
            'command': command,
            'language': language
        })
        
        # Wait for result with timeout
        try:
            result = await asyncio.wait_for(future, timeout=timeout)
            return result
        except asyncio.TimeoutError:
            raise TimeoutError("Command execution timeout")
        finally:
            del self.pending_requests[request_id]
    
    async def handle_result(self, data: Dict):
        """Handle result from client"""
        
        request_id = data['request_id']
        result = data['result']
        
        if request_id in self.pending_requests:
            self.pending_requests[request_id].set_result(result)

local_connection_manager = LocalConnectionManager()

@router.websocket("/ws/local")
async def local_client_websocket(
    websocket: WebSocket,
    user: User = Depends(get_current_user_ws)
):
    """WebSocket endpoint for local clients"""
    
    # Get or create client ID
    client_id = await get_or_create_local_client(user.id)
    
    await local_connection_manager.connect(websocket, user.id, client_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data['type'] == 'result':
                await local_connection_manager.handle_result(data)
            
            elif data['type'] == 'pong':
                # Heartbeat response
                pass
    
    except WebSocketDisconnect:
        local_connection_manager.disconnect(client_id)
```

## 4. Security Considerations

### 4.1 Sandbox Security

**Container Isolation:**
- Each session in separate container
- No inter-container communication
- Network isolation (no access to internal services)
- Read-only system files

**Resource Limits:**
- CPU: 2 cores max
- Memory: 4GB max
- Disk: 10GB max
- Network: 100Mbps
- Execution timeout: 5 minutes per command

**Command Restrictions:**
- No `sudo` or privilege escalation
- No access to host filesystem
- No raw network sockets
- Blacklist dangerous commands (`rm -rf /`, `:(){ :|:& };:`, etc.)

**Secrets Protection:**
- No access to platform secrets
- User API keys encrypted
- Environment variables isolated

### 4.2 Local Client Security

**File Access:**
- Restricted to workspace directory only
- No access to system files
- Path traversal prevention

**Command Execution:**
- Whitelist of allowed commands
- User confirmation for sensitive operations
- Execution timeout

**Network:**
- TLS encryption for all communication
- Token-based authentication
- Token rotation support

**Data Privacy:**
- Code executes locally (not sent to server)
- Only results sent back
- User can audit all operations

## 5. Performance Optimization

### 5.1 Container Pooling

```python
class ContainerPool:
    """Pool of pre-warmed containers"""
    
    def __init__(self, pool_size: int = 5):
        self.pool_size = pool_size
        self.available = []
        self.in_use = {}
    
    async def initialize(self):
        """Pre-create containers"""
        for i in range(self.pool_size):
            container = await create_container(f"pool-{i}")
            self.available.append(container)
    
    async def acquire(self, session_id: str) -> str:
        """Acquire container from pool"""
        if self.available:
            container = self.available.pop()
            self.in_use[session_id] = container
            return container.id
        else:
            # Pool exhausted, create new
            container = await create_container(session_id)
            self.in_use[session_id] = container
            return container.id
    
    async def release(self, session_id: str):
        """Release container back to pool"""
        if session_id in self.in_use:
            container = self.in_use[session_id]
            del self.in_use[session_id]
            
            # Clean and return to pool
            await clean_container(container)
            self.available.append(container)
```

### 5.2 Caching

- Cache Docker images locally
- Cache Python packages in volume
- Cache npm packages in volume
- Reuse containers when possible

### 5.3 Resource Management

- Auto-scale container hosts based on demand
- Hibernate idle containers
- Destroy old containers
- Compress hibernated workspaces

---

**Document Version**: 1.0  
**Last Updated**: 2024-01-XX  
**Status**: Draft - Pending Review

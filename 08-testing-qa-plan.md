# Mr.Dark AI Agent Platform - Testing & Quality Assurance Plan

## 1. Testing Philosophy

### 1.1 Core Principles

**Zero Tolerance for Bugs:**
- Every feature MUST be tested before commit
- All bugs MUST be fixed immediately
- No "known issues" in production
- No "will fix later"

**Test Coverage Requirements:**
- Backend: Minimum 80% code coverage
- Frontend: Minimum 70% code coverage
- Critical paths: 100% coverage
- All API endpoints: 100% coverage

**Testing Pyramid:**
```
        /\
       /  \
      / E2E \
     /--------\
    /          \
   / Integration \
  /--------------\
 /                \
/   Unit Tests     \
--------------------
```

## 2. Unit Testing

### 2.1 Backend Unit Tests (Python/FastAPI)

**Framework:** pytest + pytest-asyncio

**File Structure:**
```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_sessions.py
│   ├── test_messages.py
│   ├── test_ai_agent.py
│   ├── test_tools.py
│   ├── test_sandbox.py
│   ├── test_api_keys.py
│   ├── test_quota.py
│   └── test_database.py
```

**Example: test_auth.py**
```python
import pytest
from fastapi.testclient import TestClient
from main import app
from services.auth import AuthService

client = TestClient(app)

@pytest.fixture
def test_user():
    """Create test user"""
    return {
        'email': 'test@example.com',
        'password': 'TestPass123!',
        'full_name': 'Test User'
    }

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_signup_success(self, test_user):
        """Test successful signup"""
        response = client.post('/api/auth/signup', json=test_user)
        
        assert response.status_code == 201
        data = response.json()
        assert 'access_token' in data
        assert 'user' in data
        assert data['user']['email'] == test_user['email']
    
    def test_signup_duplicate_email(self, test_user):
        """Test signup with duplicate email"""
        # Create user first
        client.post('/api/auth/signup', json=test_user)
        
        # Try to create again
        response = client.post('/api/auth/signup', json=test_user)
        
        assert response.status_code == 400
        assert 'already exists' in response.json()['detail'].lower()
    
    def test_signup_invalid_email(self):
        """Test signup with invalid email"""
        response = client.post('/api/auth/signup', json={
            'email': 'invalid-email',
            'password': 'TestPass123!'
        })
        
        assert response.status_code == 422
    
    def test_signup_weak_password(self, test_user):
        """Test signup with weak password"""
        test_user['password'] = '123'
        response = client.post('/api/auth/signup', json=test_user)
        
        assert response.status_code == 400
        assert 'password' in response.json()['detail'].lower()
    
    def test_login_success(self, test_user):
        """Test successful login"""
        # Create user
        client.post('/api/auth/signup', json=test_user)
        
        # Login
        response = client.post('/api/auth/login', json={
            'email': test_user['email'],
            'password': test_user['password']
        })
        
        assert response.status_code == 200
        data = response.json()
        assert 'access_token' in data
        assert 'refresh_token' in data
    
    def test_login_wrong_password(self, test_user):
        """Test login with wrong password"""
        # Create user
        client.post('/api/auth/signup', json=test_user)
        
        # Try wrong password
        response = client.post('/api/auth/login', json={
            'email': test_user['email'],
            'password': 'WrongPassword123!'
        })
        
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self):
        """Test login with nonexistent user"""
        response = client.post('/api/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'Password123!'
        })
        
        assert response.status_code == 401
    
    def test_refresh_token(self, test_user):
        """Test token refresh"""
        # Create and login
        client.post('/api/auth/signup', json=test_user)
        login_response = client.post('/api/auth/login', json={
            'email': test_user['email'],
            'password': test_user['password']
        })
        
        refresh_token = login_response.json()['refresh_token']
        
        # Refresh
        response = client.post('/api/auth/refresh', json={
            'refresh_token': refresh_token
        })
        
        assert response.status_code == 200
        assert 'access_token' in response.json()
    
    def test_protected_endpoint_without_token(self):
        """Test accessing protected endpoint without token"""
        response = client.get('/api/users/me')
        
        assert response.status_code == 401
    
    def test_protected_endpoint_with_token(self, test_user):
        """Test accessing protected endpoint with valid token"""
        # Create and login
        client.post('/api/auth/signup', json=test_user)
        login_response = client.post('/api/auth/login', json={
            'email': test_user['email'],
            'password': test_user['password']
        })
        
        token = login_response.json()['access_token']
        
        # Access protected endpoint
        response = client.get(
            '/api/users/me',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        assert response.json()['email'] == test_user['email']

# AI MUST CREATE SIMILAR COMPREHENSIVE TESTS FOR:
# - Sessions (create, list, get, update, delete, archive)
# - Messages (create, list, stream, edit, delete)
# - AI Agent (model selection, function calling, streaming)
# - Tools (all tool executions)
# - Sandbox (container lifecycle, hibernation)
# - API Keys (add, list, delete, validate)
# - Quota (check, deduct, reset, warnings)
```

**Example: test_ai_agent.py**
```python
import pytest
from services.ai_agent import AIAgent
from unittest.mock import Mock, patch

class TestAIAgent:
    """Test AI Agent functionality"""
    
    @pytest.fixture
    def agent(self):
        return AIAgent()
    
    @pytest.mark.asyncio
    async def test_simple_chat(self, agent):
        """Test simple chat without tools"""
        response = await agent.chat(
            messages=[
                {'role': 'user', 'content': 'Hello'}
            ],
            model='gpt-3.5-turbo'
        )
        
        assert response['role'] == 'assistant'
        assert len(response['content']) > 0
        assert 'tokens_used' in response
    
    @pytest.mark.asyncio
    async def test_function_calling(self, agent):
        """Test function calling"""
        with patch('services.tools.execute_tool') as mock_execute:
            mock_execute.return_value = {'result': 'Tool executed'}
            
            response = await agent.chat(
                messages=[
                    {'role': 'user', 'content': 'Search for Python tutorials'}
                ],
                model='gpt-4',
                tools_enabled=True
            )
            
            # Should have called search tool
            assert mock_execute.called
            assert 'tool_calls' in response
    
    @pytest.mark.asyncio
    async def test_streaming(self, agent):
        """Test streaming response"""
        chunks = []
        
        async for chunk in agent.chat_stream(
            messages=[
                {'role': 'user', 'content': 'Count to 5'}
            ],
            model='gpt-3.5-turbo'
        ):
            chunks.append(chunk)
        
        assert len(chunks) > 0
        full_response = ''.join(c['content'] for c in chunks if 'content' in c)
        assert len(full_response) > 0
    
    @pytest.mark.asyncio
    async def test_context_management(self, agent):
        """Test context window management"""
        # Create long conversation
        messages = [
            {'role': 'user', 'content': f'Message {i}'}
            for i in range(100)
        ]
        
        # Should truncate to fit context window
        truncated = await agent.truncate_messages(messages, model='gpt-3.5-turbo')
        
        assert len(truncated) < len(messages)
        assert truncated[0]['role'] == 'user'  # Keep recent messages
    
    @pytest.mark.asyncio
    async def test_error_handling(self, agent):
        """Test error handling"""
        with patch('openai.ChatCompletion.create') as mock_create:
            mock_create.side_effect = Exception('API Error')
            
            with pytest.raises(Exception):
                await agent.chat(
                    messages=[{'role': 'user', 'content': 'Test'}],
                    model='gpt-4'
                )
```

**Running Tests:**
```bash
# AI MUST RUN THESE COMMANDS

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::TestAuthentication::test_login_success

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

### 2.2 Frontend Unit Tests (React/Next.js)

**Framework:** Jest + React Testing Library

**File Structure:**
```
frontend/
├── __tests__/
│   ├── components/
│   │   ├── ChatInterface.test.tsx
│   │   ├── MessageList.test.tsx
│   │   ├── MessageInput.test.tsx
│   │   ├── Sidebar.test.tsx
│   │   └── ToolExecution.test.tsx
│   ├── hooks/
│   │   ├── useChat.test.ts
│   │   ├── useSession.test.ts
│   │   └── useAuth.test.ts
│   ├── services/
│   │   ├── api.test.ts
│   │   └── websocket.test.ts
│   └── utils/
│       ├── markdown.test.ts
│       └── formatting.test.ts
```

**Example: ChatInterface.test.tsx**
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { ChatInterface } from '@/components/ChatInterface'
import { useChat } from '@/hooks/useChat'

// Mock useChat hook
jest.mock('@/hooks/useChat')

describe('ChatInterface', () => {
  const mockSendMessage = jest.fn()
  const mockMessages = [
    {
      id: '1',
      role: 'user',
      content: 'Hello',
      created_at: new Date().toISOString()
    },
    {
      id: '2',
      role: 'assistant',
      content: 'Hi there!',
      created_at: new Date().toISOString()
    }
  ]
  
  beforeEach(() => {
    (useChat as jest.Mock).mockReturnValue({
      messages: mockMessages,
      sendMessage: mockSendMessage,
      isLoading: false,
      error: null
    })
  })
  
  it('renders messages correctly', () => {
    render(<ChatInterface sessionId="test-session" />)
    
    expect(screen.getByText('Hello')).toBeInTheDocument()
    expect(screen.getByText('Hi there!')).toBeInTheDocument()
  })
  
  it('sends message on submit', async () => {
    render(<ChatInterface sessionId="test-session" />)
    
    const input = screen.getByPlaceholderText('Type a message...')
    const sendButton = screen.getByRole('button', { name: /send/i })
    
    fireEvent.change(input, { target: { value: 'Test message' } })
    fireEvent.click(sendButton)
    
    await waitFor(() => {
      expect(mockSendMessage).toHaveBeenCalledWith('Test message')
    })
  })
  
  it('shows loading state', () => {
    (useChat as jest.Mock).mockReturnValue({
      messages: mockMessages,
      sendMessage: mockSendMessage,
      isLoading: true,
      error: null
    })
    
    render(<ChatInterface sessionId="test-session" />)
    
    expect(screen.getByTestId('loading-indicator')).toBeInTheDocument()
  })
  
  it('shows error message', () => {
    (useChat as jest.Mock).mockReturnValue({
      messages: mockMessages,
      sendMessage: mockSendMessage,
      isLoading: false,
      error: 'Failed to send message'
    })
    
    render(<ChatInterface sessionId="test-session" />)
    
    expect(screen.getByText(/failed to send message/i)).toBeInTheDocument()
  })
  
  it('clears input after sending', async () => {
    render(<ChatInterface sessionId="test-session" />)
    
    const input = screen.getByPlaceholderText('Type a message...') as HTMLInputElement
    const sendButton = screen.getByRole('button', { name: /send/i })
    
    fireEvent.change(input, { target: { value: 'Test' } })
    fireEvent.click(sendButton)
    
    await waitFor(() => {
      expect(input.value).toBe('')
    })
  })
})

// AI MUST CREATE TESTS FOR ALL COMPONENTS
```

**Running Tests:**
```bash
# AI MUST RUN THESE

# Run all tests
pnpm test

# Run with coverage
pnpm test:coverage

# Run in watch mode
pnpm test:watch

# Update snapshots
pnpm test -u
```

## 3. Integration Testing

### 3.1 API Integration Tests

**Test complete API flows:**

```python
# tests/integration/test_chat_flow.py

import pytest
from fastapi.testclient import TestClient

class TestChatFlow:
    """Test complete chat flow"""
    
    @pytest.fixture
    def authenticated_client(self):
        """Get authenticated client"""
        client = TestClient(app)
        
        # Signup
        response = client.post('/api/auth/signup', json={
            'email': 'test@example.com',
            'password': 'TestPass123!'
        })
        
        token = response.json()['access_token']
        client.headers = {'Authorization': f'Bearer {token}'}
        
        return client
    
    def test_complete_chat_flow(self, authenticated_client):
        """Test: Create session → Send message → Get response → List messages"""
        
        # 1. Create session
        response = authenticated_client.post('/api/sessions', json={
            'model': 'gpt-3.5-turbo',
            'mode': 'sandbox'
        })
        assert response.status_code == 201
        session_id = response.json()['id']
        
        # 2. Send message
        response = authenticated_client.post(
            f'/api/sessions/{session_id}/messages',
            json={'content': 'Hello, AI!'}
        )
        assert response.status_code == 201
        message = response.json()
        assert message['role'] == 'assistant'
        assert len(message['content']) > 0
        
        # 3. List messages
        response = authenticated_client.get(f'/api/sessions/{session_id}/messages')
        assert response.status_code == 200
        messages = response.json()
        assert len(messages) == 2  # User + Assistant
        
        # 4. Get session
        response = authenticated_client.get(f'/api/sessions/{session_id}')
        assert response.status_code == 200
        session = response.json()
        assert session['total_messages'] == 2
        assert session['total_tokens_used'] > 0
    
    def test_tool_execution_flow(self, authenticated_client):
        """Test: Message with tool → Tool execution → Tool result → Final response"""
        
        # Create session
        response = authenticated_client.post('/api/sessions', json={
            'model': 'gpt-4',
            'mode': 'sandbox'
        })
        session_id = response.json()['id']
        
        # Send message that requires tool
        response = authenticated_client.post(
            f'/api/sessions/{session_id}/messages',
            json={'content': 'Search for "Python tutorials"'}
        )
        
        assert response.status_code == 201
        message = response.json()
        
        # Should have tool calls
        assert 'tool_calls' in message or 'tool_executions' in message
        
        # Check tool execution was logged
        response = authenticated_client.get(
            f'/api/sessions/{session_id}/tool-executions'
        )
        assert response.status_code == 200
        executions = response.json()
        assert len(executions) > 0
        assert executions[0]['tool_name'] == 'search'
        assert executions[0]['status'] == 'success'

# AI MUST CREATE INTEGRATION TESTS FOR:
# - Sandbox lifecycle
# - File upload/download
# - API key management
# - Quota system
# - Local client connection
```

### 3.2 Database Integration Tests

```python
# tests/integration/test_database_integrity.py

class TestDatabaseIntegrity:
    """Test database constraints and relationships"""
    
    @pytest.mark.asyncio
    async def test_cascade_delete_user(self):
        """Test that deleting user cascades to sessions and messages"""
        
        # Create user
        user = await db.create_user({
            'email': 'test@example.com',
            'auth_id': str(uuid.uuid4())
        })
        
        # Create session
        session = await db.create_session({
            'user_id': user['id'],
            'model': 'gpt-4',
            'mode': 'sandbox'
        })
        
        # Create message
        message = await db.create_message({
            'session_id': session['id'],
            'role': 'user',
            'content': 'Test'
        })
        
        # Delete user
        await db.delete_user(user['id'])
        
        # Verify cascading delete
        assert await db.get_session(session['id']) is None
        assert await db.get_message(message['id']) is None
    
    @pytest.mark.asyncio
    async def test_quota_constraints(self):
        """Test quota constraints"""
        
        user = await db.create_user({
            'email': 'test@example.com',
            'auth_id': str(uuid.uuid4()),
            'quota_tokens_monthly': 1000
        })
        
        # Try to use more than quota
        with pytest.raises(Exception):
            await db.update_user(user['id'], {
                'quota_used_current_month': 1001
            })
```

## 4. End-to-End (E2E) Testing

### 4.1 Playwright E2E Tests

**Framework:** Playwright

```typescript
// e2e/chat.spec.ts

import { test, expect } from '@playwright/test'

test.describe('Chat Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('http://localhost:3000/login')
    await page.fill('[name="email"]', 'test@example.com')
    await page.fill('[name="password"]', 'TestPass123!')
    await page.click('button[type="submit"]')
    await page.waitForURL('http://localhost:3000/chat')
  })
  
  test('should create new chat and send message', async ({ page }) => {
    // Click new chat
    await page.click('[data-testid="new-chat-button"]')
    
    // Wait for new session
    await page.waitForSelector('[data-testid="chat-input"]')
    
    // Type message
    await page.fill('[data-testid="chat-input"]', 'Hello, AI!')
    
    // Send
    await page.click('[data-testid="send-button"]')
    
    // Wait for response
    await page.waitForSelector('[data-testid="assistant-message"]', {
      timeout: 10000
    })
    
    // Verify message appears
    const userMessage = page.locator('[data-testid="user-message"]').last()
    await expect(userMessage).toContainText('Hello, AI!')
    
    const assistantMessage = page.locator('[data-testid="assistant-message"]').last()
    await expect(assistantMessage).toBeVisible()
  })
  
  test('should execute code in sandbox', async ({ page }) => {
    // Create new chat
    await page.click('[data-testid="new-chat-button"]')
    
    // Send code execution request
    await page.fill('[data-testid="chat-input"]', 'Write Python code to calculate 2+2')
    await page.click('[data-testid="send-button"]')
    
    // Wait for tool execution
    await page.waitForSelector('[data-testid="tool-execution"]', {
      timeout: 15000
    })
    
    // Verify code block appears
    const codeBlock = page.locator('[data-testid="code-block"]').last()
    await expect(codeBlock).toBeVisible()
    
    // Verify result
    const result = page.locator('[data-testid="execution-result"]').last()
    await expect(result).toContainText('4')
  })
  
  test('should switch between sessions', async ({ page }) => {
    // Create first session
    await page.click('[data-testid="new-chat-button"]')
    await page.fill('[data-testid="chat-input"]', 'First chat')
    await page.click('[data-testid="send-button"]')
    await page.waitForSelector('[data-testid="assistant-message"]')
    
    // Create second session
    await page.click('[data-testid="new-chat-button"]')
    await page.fill('[data-testid="chat-input"]', 'Second chat')
    await page.click('[data-testid="send-button"]')
    await page.waitForSelector('[data-testid="assistant-message"]')
    
    // Click first session in sidebar
    const firstSession = page.locator('[data-testid="session-item"]').first()
    await firstSession.click()
    
    // Verify first chat is loaded
    await expect(page.locator('[data-testid="user-message"]').first())
      .toContainText('First chat')
  })
  
  test('should show quota warning', async ({ page }) => {
    // Mock quota near limit
    await page.route('**/api/users/quota', route => {
      route.fulfill({
        status: 200,
        body: JSON.stringify({
          used: 950000,
          total: 1000000,
          remaining: 50000,
          percentage: 95
        })
      })
    })
    
    // Reload page
    await page.reload()
    
    // Should show warning
    await expect(page.locator('[data-testid="quota-warning"]')).toBeVisible()
  })
})

// AI MUST CREATE E2E TESTS FOR:
// - Authentication flow
// - Settings management
// - API key management
// - File uploads
// - Model switching
// - Sandbox/local mode switching
```

**Running E2E Tests:**
```bash
# AI MUST RUN

# Run all E2E tests
pnpm e2e

# Run in headed mode (see browser)
pnpm e2e:headed

# Run specific test
pnpm e2e chat.spec.ts

# Generate test report
pnpm e2e --reporter=html
```

## 5. Performance Testing

### 5.1 Load Testing

**Framework:** Locust

```python
# locustfile.py

from locust import HttpUser, task, between
import random

class MrDarkUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Login on start"""
        response = self.client.post('/api/auth/login', json={
            'email': f'user{random.randint(1, 1000)}@example.com',
            'password': 'TestPass123!'
        })
        self.token = response.json()['access_token']
        self.client.headers = {'Authorization': f'Bearer {self.token}'}
    
    @task(3)
    def send_message(self):
        """Send chat message"""
        # Create session if needed
        if not hasattr(self, 'session_id'):
            response = self.client.post('/api/sessions', json={
                'model': 'gpt-3.5-turbo',
                'mode': 'sandbox'
            })
            self.session_id = response.json()['id']
        
        # Send message
        self.client.post(
            f'/api/sessions/{self.session_id}/messages',
            json={'content': 'Test message'}
        )
    
    @task(1)
    def list_sessions(self):
        """List sessions"""
        self.client.get('/api/sessions')
    
    @task(1)
    def get_quota(self):
        """Get quota status"""
        self.client.get('/api/users/quota')

# Run: locust -f locustfile.py --host=http://localhost:8000
```

### 5.2 Performance Benchmarks

**Target Metrics:**
- API response time: < 200ms (p95)
- Chat response time: < 3s (p95)
- Tool execution: < 5s (p95)
- Page load time: < 2s
- Time to interactive: < 3s

**Monitoring:**
```python
# middleware/performance.py

import time
from prometheus_client import Histogram

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint', 'status']
)

async def performance_middleware(request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).observe(duration)
    
    return response
```

## 6. Security Testing

### 6.1 Security Checklist

- [ ] SQL injection protection
- [ ] XSS protection
- [ ] CSRF protection
- [ ] Authentication bypass attempts
- [ ] Authorization bypass attempts
- [ ] Rate limiting
- [ ] Input validation
- [ ] API key encryption
- [ ] Secure headers
- [ ] HTTPS enforcement

### 6.2 Security Tests

```python
# tests/security/test_auth_security.py

class TestAuthSecurity:
    """Test authentication security"""
    
    def test_sql_injection_attempt(self, client):
        """Test SQL injection protection"""
        response = client.post('/api/auth/login', json={
            'email': "admin' OR '1'='1",
            'password': 'anything'
        })
        
        assert response.status_code == 401
    
    def test_rate_limiting(self, client):
        """Test rate limiting on login"""
        # Try 10 failed logins
        for i in range(10):
            client.post('/api/auth/login', json={
                'email': 'test@example.com',
                'password': 'wrong'
            })
        
        # 11th should be rate limited
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'wrong'
        })
        
        assert response.status_code == 429
    
    def test_jwt_tampering(self, client):
        """Test JWT tampering detection"""
        # Get valid token
        response = client.post('/api/auth/signup', json={
            'email': 'test@example.com',
            'password': 'TestPass123!'
        })
        token = response.json()['access_token']
        
        # Tamper with token
        tampered_token = token[:-10] + 'tampered123'
        
        # Try to use tampered token
        response = client.get(
            '/api/users/me',
            headers={'Authorization': f'Bearer {tampered_token}'}
        )
        
        assert response.status_code == 401
```

## 7. Continuous Integration

### 7.1 GitHub Actions Workflow

```yaml
# .github/workflows/test.yml

name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio
      
      - name: Run tests
        run: |
          cd backend
          pytest --cov=. --cov-report=xml --cov-report=term
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage.xml
  
  frontend-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Install pnpm
        run: npm install -g pnpm
      
      - name: Install dependencies
        run: |
          cd frontend
          pnpm install
      
      - name: Run tests
        run: |
          cd frontend
          pnpm test:coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./frontend/coverage/coverage-final.json
  
  e2e-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: |
          cd frontend
          pnpm install
          pnpm exec playwright install --with-deps
      
      - name: Run E2E tests
        run: |
          cd frontend
          pnpm e2e
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: frontend/playwright-report/
```

## 8. Test Execution Checklist

### 8.1 Before Each Commit

- [ ] Run unit tests: `pytest` and `pnpm test`
- [ ] Check code coverage (>80% backend, >70% frontend)
- [ ] Run linter: `flake8` and `eslint`
- [ ] Run formatter: `black` and `prettier`
- [ ] Fix all errors and warnings

### 8.2 Before Each PR

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All E2E tests pass
- [ ] Code coverage meets requirements
- [ ] No console errors in browser
- [ ] Manual testing of changed features
- [ ] Performance benchmarks pass

### 8.3 Before Deployment

- [ ] All tests pass in CI/CD
- [ ] Load testing completed
- [ ] Security scan completed
- [ ] Database migrations tested
- [ ] Rollback plan ready
- [ ] Monitoring configured

---

**Document Version**: 1.0  
**Last Updated**: 2024-01-XX  
**Status**: MANDATORY - MUST FOLLOW EXACTLY

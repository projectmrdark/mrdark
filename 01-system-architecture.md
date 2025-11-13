# Mr.Dark AI Agent Platform - System Architecture

## 1. ภาพรวมระบบ (System Overview)

Mr.Dark เป็น AI Agent Platform ที่รวมความสามารถของ Manus และ ChatGPT เข้าด้วยกัน โดยมีเป้าหมายให้ผู้ใช้สามารถใช้งาน AI Agent ที่มีความสามารถครบถ้วนที่สุดในเว็บไซต์เดียว

### 1.1 Core Principles

1. **Single Platform** - เว็บไซต์เดียวที่รวมทุกความสามารถ
2. **Dual Execution Modes** - รองรับทั้ง Sandbox และ Local Connection
3. **Complete Tool Integration** - ครบทุก Tools จาก Manus + ChatGPT
4. **Professional UI/UX** - เรียบง่ายแบบ GPT + การแสดงผลแบบ Manus
5. **Scalable & Sustainable** - รองรับการขยายและสร้างรายได้

### 1.2 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Mr.Dark Platform                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Frontend (Next.js 14)                      │    │
│  │  - Chat Interface (GPT-style)                          │    │
│  │  - Execution Viewer (Manus-style)                      │    │
│  │  - File Manager & Browser Viewer                       │    │
│  │  - Settings & API Key Management                       │    │
│  └────────────────────────────────────────────────────────┘    │
│                            ↕                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Backend API (FastAPI)                      │    │
│  │  - Authentication & Authorization                       │    │
│  │  - Session Management                                   │    │
│  │  - API Key Rotation System                             │    │
│  │  - Quota Management                                     │    │
│  │  - WebSocket Handler                                    │    │
│  └────────────────────────────────────────────────────────┘    │
│                            ↕                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           AI Agent Orchestrator                         │    │
│  │  - Task Planning & Execution                           │    │
│  │  - Tool Selection & Invocation                         │    │
│  │  - Context Management                                   │    │
│  │  - Multi-Model Support (GPT-4, Claude, Gemini)        │    │
│  └────────────────────────────────────────────────────────┘    │
│                            ↕                                     │
│  ┌──────────────────┬──────────────────────────────────────┐   │
│  │  Sandbox Mode    │    Local Connection Mode             │   │
│  │  (Server-side)   │    (Client-side)                     │   │
│  ├──────────────────┼──────────────────────────────────────┤   │
│  │  - Docker        │    - WebSocket Bridge                │   │
│  │  - Code Exec     │    - Local Agent Client              │   │
│  │  - Browser       │    - File Sync                       │   │
│  │  - File System   │    - Command Execution               │   │
│  └──────────────────┴──────────────────────────────────────┘   │
│                            ↕                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Tool Integration Layer                     │    │
│  │  - Browser Automation (Playwright)                     │    │
│  │  - Code Interpreter (Python, Node.js, etc.)           │    │
│  │  - File Operations (Read, Write, Edit)                │    │
│  │  - Search (Web, Image, News, etc.)                    │    │
│  │  - Image Generation (DALL-E, Stable Diffusion)        │    │
│  │  - Data Analysis (Pandas, Matplotlib)                 │    │
│  │  - Shell Commands                                      │    │
│  │  - API Integrations                                    │    │
│  └────────────────────────────────────────────────────────┘    │
│                            ↕                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Database (Supabase/PostgreSQL)             │    │
│  │  - Users & Authentication                              │    │
│  │  - Sessions & Conversations                            │    │
│  │  - Files & Artifacts                                   │    │
│  │  - Usage & Quota Tracking                              │    │
│  │  - API Keys Pool                                       │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Technology Stack

### 2.1 Frontend

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **State Management**: Zustand
- **Real-time Communication**: WebSocket (Socket.io-client)
- **Code Editor**: Monaco Editor
- **Markdown Rendering**: react-markdown + remark/rehype plugins
- **File Upload**: react-dropzone
- **Icons**: Lucide React

### 2.2 Backend

- **Framework**: FastAPI (Python 3.11+)
- **Language**: Python
- **WebSocket**: FastAPI WebSocket + Socket.io
- **Task Queue**: Celery + Redis (for async tasks)
- **Caching**: Redis
- **File Storage**: S3-compatible (Supabase Storage)
- **Authentication**: JWT + Supabase Auth

### 2.3 AI & Agent

- **LLM Integration**: 
  - OpenAI API (GPT-4, GPT-4 Turbo, GPT-3.5)
  - Anthropic API (Claude 3 Opus, Sonnet, Haiku)
  - Google AI API (Gemini Pro, Gemini Ultra)
- **Agent Framework**: Custom (inspired by LangChain but optimized)
- **Function Calling**: Native support for all models
- **Streaming**: Server-Sent Events (SSE) + WebSocket

### 2.4 Execution Environments

#### Sandbox Mode (Server-side)
- **Container**: Docker + Docker Compose
- **Orchestration**: Docker SDK for Python
- **Browser Automation**: Playwright (Chromium)
- **Code Execution**: Isolated containers per session
- **File System**: Volume mounting + S3 backup
- **Networking**: Isolated networks per session

#### Local Connection Mode (Client-side)
- **Agent Client**: Electron app or Python CLI
- **Communication**: WebSocket over SSL
- **Security**: Token-based authentication + encryption
- **Execution**: Local Python/Node.js runtime
- **File Access**: Sandboxed directory access

### 2.5 Database & Storage

- **Primary Database**: Supabase (PostgreSQL 15+)
- **File Storage**: Supabase Storage (S3-compatible)
- **Caching**: Redis 7+
- **Vector Database**: Supabase pgvector (for future RAG features)

### 2.6 Infrastructure & Deployment

- **Frontend Hosting**: Vercel
- **Backend Hosting**: Railway / Fly.io / DigitalOcean
- **Database**: Supabase Cloud
- **CDN**: Vercel Edge Network
- **Monitoring**: Sentry + Supabase Analytics
- **Logging**: Structured logging to Supabase

## 3. System Components Detail

### 3.1 Frontend Components

#### 3.1.1 Chat Interface
- **Input Area**: Multi-line text input with file attachment support
- **Message List**: Virtualized list for performance
- **Message Types**:
  - User messages
  - Assistant messages (with streaming support)
  - System messages
  - Tool execution results
  - Error messages
- **Features**:
  - Markdown rendering
  - Code syntax highlighting
  - Image preview
  - File download
  - Copy to clipboard
  - Regenerate response

#### 3.1.2 Execution Viewer (Manus-style)
- **Tool Execution Panel**: Shows real-time tool invocations
- **Browser Viewer**: Live browser screenshots + DOM inspector
- **File Explorer**: Tree view of session files
- **Code Editor**: Monaco editor for viewing/editing code
- **Terminal**: Live terminal output viewer
- **Network Inspector**: HTTP requests/responses log

#### 3.1.3 Settings & Management
- **User Profile**: Avatar, name, email
- **API Keys**: Add/remove/manage API keys
- **Quota Display**: Current usage vs. limit
- **Execution Mode**: Toggle between Sandbox and Local
- **Model Selection**: Choose AI model
- **Theme**: Light/Dark mode

### 3.2 Backend Components

#### 3.2.1 API Endpoints

**Authentication**
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user
- `POST /api/auth/refresh` - Refresh JWT token

**Chat & Sessions**
- `POST /api/sessions` - Create new session
- `GET /api/sessions` - List user sessions
- `GET /api/sessions/{id}` - Get session details
- `DELETE /api/sessions/{id}` - Delete session
- `POST /api/sessions/{id}/messages` - Send message
- `GET /api/sessions/{id}/messages` - Get message history
- `WS /api/sessions/{id}/ws` - WebSocket connection

**Files**
- `POST /api/files/upload` - Upload file
- `GET /api/files/{id}` - Download file
- `DELETE /api/files/{id}` - Delete file
- `GET /api/sessions/{id}/files` - List session files

**User Management**
- `GET /api/users/quota` - Get quota usage
- `POST /api/users/api-keys` - Add API key
- `GET /api/users/api-keys` - List API keys
- `DELETE /api/users/api-keys/{id}` - Remove API key

**Admin** (Future)
- `GET /api/admin/users` - List all users
- `GET /api/admin/stats` - Platform statistics
- `POST /api/admin/quota/{user_id}` - Update user quota

#### 3.2.2 WebSocket Protocol

**Client → Server**
```json
{
  "type": "message",
  "content": "User message text",
  "attachments": ["file_id_1", "file_id_2"],
  "model": "gpt-4",
  "mode": "sandbox"
}
```

**Server → Client**
```json
{
  "type": "message_start",
  "message_id": "msg_123"
}

{
  "type": "content_delta",
  "delta": "Partial response text..."
}

{
  "type": "tool_call",
  "tool": "browser",
  "action": "navigate",
  "params": {"url": "https://example.com"}
}

{
  "type": "tool_result",
  "tool": "browser",
  "result": "Screenshot saved",
  "artifacts": ["screenshot.png"]
}

{
  "type": "message_end",
  "message_id": "msg_123",
  "usage": {"tokens": 1234}
}

{
  "type": "error",
  "error": "Error message",
  "code": "RATE_LIMIT_EXCEEDED"
}
```

### 3.3 AI Agent Orchestrator

#### 3.3.1 Agent Loop
```
1. Receive user message
2. Load session context
3. Select AI model
4. Generate response with function calling
5. If function call:
   a. Validate tool and parameters
   b. Execute tool (sandbox or local)
   c. Collect result
   d. Feed back to AI
   e. Repeat from step 4
6. Stream final response to user
7. Save to database
8. Update quota
```

#### 3.3.2 Tool Registry
- **Browser Tools**: navigate, click, type, screenshot, extract
- **Code Tools**: execute_python, execute_node, execute_shell
- **File Tools**: read, write, edit, delete, list
- **Search Tools**: web_search, image_search, news_search
- **Generation Tools**: generate_image, edit_image
- **Data Tools**: analyze_data, create_chart, export_csv
- **System Tools**: get_time, calculate, convert

#### 3.3.3 Context Management
- **Conversation History**: Last N messages (configurable)
- **File Context**: Attached files content
- **Tool Results**: Recent tool execution results
- **System Prompts**: Role and capabilities description
- **Token Management**: Auto-truncate to fit context window

### 3.4 Sandbox System

#### 3.4.1 Container Architecture
```
┌─────────────────────────────────────┐
│      Session Container               │
│  ┌────────────────────────────────┐ │
│  │  Python 3.11 Runtime           │ │
│  │  Node.js 20 Runtime            │ │
│  │  Playwright + Chromium         │ │
│  │  Common tools (git, curl, etc) │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │
│  │  File System (/workspace)      │ │
│  │  - User files                  │ │
│  │  - Generated code              │ │
│  │  - Downloads                   │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │
│  │  Agent Executor Service        │ │
│  │  - Listens on internal port    │ │
│  │  - Executes commands           │ │
│  │  - Returns results             │ │
│  └────────────────────────────────┘ │
└─────────────────────────────────────┘
```

#### 3.4.2 Container Lifecycle
1. **Create**: On first message in session
2. **Warm**: Keep alive for 5 minutes after last activity
3. **Hibernate**: Save state to S3, stop container
4. **Resume**: Restore from S3, start container
5. **Destroy**: After 24 hours or manual deletion

#### 3.4.3 Resource Limits
- **CPU**: 2 cores max
- **Memory**: 4GB max
- **Disk**: 10GB max
- **Network**: 100Mbps
- **Execution Time**: 5 minutes per tool call
- **Concurrent Sessions**: 100 per server

### 3.5 Local Connection System

#### 3.5.1 Agent Client Architecture
```
┌─────────────────────────────────────┐
│      Mr.Dark Local Client           │
│  ┌────────────────────────────────┐ │
│  │  WebSocket Client              │ │
│  │  - Connects to platform        │ │
│  │  - Authenticates with token    │ │
│  │  - Receives commands           │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │
│  │  Command Executor              │ │
│  │  - Python runtime              │ │
│  │  - Node.js runtime             │ │
│  │  - Shell commands              │ │
│  │  - Browser automation          │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │
│  │  File Sync                     │ │
│  │  - Watch workspace directory   │ │
│  │  - Upload changes              │ │
│  │  - Download artifacts          │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │
│  │  Security Sandbox              │ │
│  │  - Restricted file access      │ │
│  │  - Command whitelist           │ │
│  │  - Network isolation           │ │
│  └────────────────────────────────┘ │
└─────────────────────────────────────┘
```

#### 3.5.2 Installation & Setup
1. User downloads client (Electron app or Python package)
2. Client generates authentication token
3. User inputs token on platform
4. Client connects via WebSocket
5. Platform verifies and establishes connection
6. User selects workspace directory
7. Client is ready to execute commands

#### 3.5.3 Security Measures
- **Token-based Auth**: Unique token per client
- **TLS Encryption**: All communication encrypted
- **Sandboxed Execution**: Limited file system access
- **Command Validation**: Whitelist of allowed commands
- **User Confirmation**: Prompt for sensitive operations

## 4. API Key Management System

### 4.1 Key Pool Architecture
```
┌─────────────────────────────────────┐
│      API Key Pool                    │
│  ┌────────────────────────────────┐ │
│  │  Admin Keys (Platform-owned)   │ │
│  │  - Multiple OpenAI keys        │ │
│  │  - Multiple Anthropic keys     │ │
│  │  - Multiple Google keys        │ │
│  │  - Rotation algorithm          │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │
│  │  User Keys (User-provided)     │ │
│  │  - Encrypted storage           │ │
│  │  - Per-user isolation          │ │
│  │  - Priority over admin keys    │ │
│  └────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### 4.2 Key Selection Logic
1. If user has own API key → Use user's key
2. Else → Select from admin key pool
3. Selection algorithm:
   - Round-robin by default
   - Skip keys near rate limit
   - Prefer keys with lower usage
   - Fallback to next provider if all keys exhausted

### 4.3 Rate Limiting & Quota
- **Per-User Quota**: 1M tokens/month (free tier)
- **Per-Key Rate Limit**: Follow provider limits
- **Quota Tracking**: Real-time token counting
- **Quota Reset**: Monthly on signup anniversary
- **Overage Handling**: Block requests, show upgrade prompt

## 5. Data Flow Examples

### 5.1 Simple Chat Message (No Tools)
```
User → Frontend → WebSocket → Backend
Backend → AI Model (with context)
AI Model → Response stream
Backend → WebSocket → Frontend → User
Backend → Save to DB
Backend → Update quota
```

### 5.2 Chat with Tool Execution (Sandbox Mode)
```
User → "Search for latest AI news"
Frontend → WebSocket → Backend
Backend → AI Model
AI Model → Function call: web_search("latest AI news")
Backend → Sandbox container
Sandbox → Execute search tool
Sandbox → Return results
Backend → AI Model (with results)
AI Model → Final response
Backend → WebSocket → Frontend → User
Backend → Save all to DB
```

### 5.3 File Upload and Analysis
```
User → Upload CSV file
Frontend → POST /api/files/upload
Backend → Save to Supabase Storage
Backend → Return file_id
User → "Analyze this CSV"
Frontend → WebSocket (with file_id)
Backend → AI Model
AI Model → Function call: read_file(file_id)
Backend → Fetch from storage
Backend → AI Model (with content)
AI Model → Function call: analyze_data(content)
Backend → Sandbox (execute Python/Pandas)
Sandbox → Generate charts, stats
Backend → AI Model (with results)
AI Model → Final response with insights
Backend → WebSocket → Frontend → User
```

## 6. Scalability Considerations

### 6.1 Horizontal Scaling
- **Frontend**: Auto-scaled on Vercel
- **Backend**: Multiple instances behind load balancer
- **Sandbox**: Distributed across multiple Docker hosts
- **Database**: Supabase handles scaling
- **Redis**: Redis Cluster for high availability

### 6.2 Performance Optimization
- **Caching**: Redis cache for frequent queries
- **CDN**: Static assets on Vercel Edge
- **Database Indexing**: Optimized queries
- **Connection Pooling**: Reuse DB connections
- **Lazy Loading**: Load components on demand
- **Code Splitting**: Reduce initial bundle size

### 6.3 Cost Optimization
- **Container Hibernation**: Stop idle containers
- **Storage Cleanup**: Delete old files automatically
- **API Key Rotation**: Maximize free tier usage
- **Compression**: Gzip/Brotli for all responses
- **Efficient Queries**: Minimize DB operations

## 7. Security Architecture

### 7.1 Authentication & Authorization
- **User Auth**: Supabase Auth (email/password, OAuth)
- **Session Management**: JWT tokens (short-lived)
- **Refresh Tokens**: Long-lived, stored securely
- **API Key Encryption**: AES-256 encryption at rest
- **RBAC**: Role-based access control (user, admin)

### 7.2 Sandbox Security
- **Isolation**: Each session in separate container
- **Network Isolation**: No inter-container communication
- **Resource Limits**: CPU, memory, disk quotas
- **Execution Timeout**: Prevent infinite loops
- **File System**: Read-only system files
- **Secrets**: No access to platform secrets

### 7.3 API Security
- **Rate Limiting**: Per-user, per-endpoint limits
- **Input Validation**: Strict schema validation
- **SQL Injection**: Parameterized queries only
- **XSS Prevention**: Content Security Policy
- **CORS**: Whitelist allowed origins
- **HTTPS Only**: Force SSL/TLS

### 7.4 Data Privacy
- **Encryption**: Data encrypted in transit and at rest
- **Access Control**: Users can only access own data
- **Data Retention**: Auto-delete after configurable period
- **Audit Logs**: Track all data access
- **GDPR Compliance**: Right to delete, export data

## 8. Monitoring & Observability

### 8.1 Metrics
- **System Metrics**: CPU, memory, disk, network
- **Application Metrics**: Request rate, latency, errors
- **Business Metrics**: Active users, sessions, token usage
- **Cost Metrics**: API costs, infrastructure costs

### 8.2 Logging
- **Structured Logs**: JSON format with context
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Aggregation**: Centralized logging (Supabase)
- **Log Retention**: 30 days default

### 8.3 Alerting
- **Error Rate**: Alert if >5% error rate
- **Latency**: Alert if p99 >5 seconds
- **Quota**: Alert if user near limit
- **Cost**: Alert if daily cost >threshold
- **Uptime**: Alert if downtime >1 minute

### 8.4 Tracing
- **Distributed Tracing**: Track requests across services
- **Performance Profiling**: Identify bottlenecks
- **User Sessions**: Replay user interactions

## 9. Future Enhancements

### 9.1 Phase 2 Features
- **Voice Input/Output**: Speech-to-text, text-to-speech
- **Multi-modal**: Image input, video analysis
- **Collaboration**: Shared sessions, real-time collaboration
- **Plugins**: User-created tools and integrations
- **Workflows**: Save and reuse common workflows
- **Templates**: Pre-built prompts and templates

### 9.2 Phase 3 Features
- **Mobile Apps**: iOS and Android native apps
- **Enterprise**: SSO, team management, audit logs
- **Marketplace**: Buy/sell prompts, tools, workflows
- **API Access**: Public API for developers
- **White-label**: Custom branding for enterprises

## 10. Success Metrics

### 10.1 Technical Metrics
- **Uptime**: >99.9%
- **Latency**: p95 <2s, p99 <5s
- **Error Rate**: <1%
- **Container Startup**: <10s
- **Tool Execution**: <30s average

### 10.2 Business Metrics
- **User Growth**: 1000 users in first month
- **Retention**: >50% weekly active
- **Engagement**: >10 messages per session
- **Conversion**: >5% free to paid
- **NPS**: >50

## 11. Risk Mitigation

### 11.1 Technical Risks
- **Sandbox Escape**: Regular security audits, container hardening
- **API Abuse**: Rate limiting, quota enforcement, fraud detection
- **Data Loss**: Regular backups, point-in-time recovery
- **Downtime**: Multi-region deployment, failover automation
- **Performance**: Load testing, auto-scaling, caching

### 11.2 Business Risks
- **API Costs**: Cost monitoring, budget alerts, user quotas
- **Compliance**: GDPR, SOC2, regular audits
- **Competition**: Continuous innovation, user feedback
- **Scaling**: Modular architecture, horizontal scaling
- **Monetization**: Multiple revenue streams, freemium model

---

**Document Version**: 1.0  
**Last Updated**: 2024-01-XX  
**Status**: Draft - Pending Review

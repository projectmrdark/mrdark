# Mr.Dark AI Agent Platform - Complete Planning & Design Documentation

> **Platform Overview**: Mr.Dark is a comprehensive AI Agent platform that combines the best features of Manus and ChatGPT, providing users with powerful AI capabilities, code execution in sandboxes, browser automation, and extensive tool integration.

## 📋 Documentation Index

This repository contains the complete planning, design, and implementation guide for the Mr.Dark platform. All documents are designed to be used by AI developers to build the system from scratch with **zero ambiguity**.

### Core Planning Documents

1. **[System Architecture](./01-system-architecture.md)** - Complete system design and technology stack
2. **[Database Schema](./02-database-schema.md)** - Full database design with all tables, relationships, and constraints
3. **[UI/UX Design](./03-ui-ux-design.md)** - Complete interface design and user experience flows
4. **[AI Agent System](./04-ai-agent-system.md)** - AI integration, tool system, and function calling
5. **[Sandbox & Local Connection](./05-sandbox-local-system.md)** - Code execution environments
6. **[API Keys & Quota Management](./06-api-keys-quota-system.md)** - Key management and usage tracking
7. **[Development Flow](./07-development-flow.md)** - Step-by-step implementation guide
8. **[Testing & QA Plan](./08-testing-qa-plan.md)** - Comprehensive testing strategy
9. **[Deployment & Infrastructure](./09-deployment-infrastructure.md)** - Production deployment guide

## 🎯 Project Goals

### Primary Objectives

1. **Unified AI Experience**: Combine ChatGPT's simplicity with Manus's power
2. **Multi-Model Support**: OpenAI, Anthropic, Google AI models
3. **Code Execution**: Sandbox and local execution modes
4. **Tool Integration**: Comprehensive tool ecosystem
5. **Flexible Quota System**: Free tier + user API keys
6. **Professional UI**: Clean, minimal, powerful

### Key Features

- ✅ Multi-model AI chat (GPT-4, Claude, Gemini)
- ✅ Sandbox code execution (Python, JavaScript, Bash)
- ✅ Local client for privacy-sensitive tasks
- ✅ Browser automation with Playwright
- ✅ File operations and management
- ✅ API key rotation and management
- ✅ Quota tracking and warnings
- ✅ Session management and history
- ✅ Real-time streaming responses
- ✅ Tool execution visualization

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                        │
│  - React 18 + TypeScript                                    │
│  - Tailwind CSS + shadcn/ui                                 │
│  - Real-time WebSocket                                      │
│  - Deployed on Vercel                                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│  - Python 3.11                                              │
│  - Async/await architecture                                 │
│  - WebSocket support                                        │
│  - Deployed on Railway/Fly.io                               │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Supabase   │  │    Redis     │  │   AWS S3     │
│  (Database)  │  │   (Cache)    │  │  (Storage)   │
└──────────────┘  └──────────────┘  └──────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │   AWS ECS        │
                  │  (Sandboxes)     │
                  └──────────────────┘
```

## 📊 Technology Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui + Radix UI
- **State**: Zustand
- **WebSocket**: Socket.IO Client
- **Markdown**: react-markdown + remark-gfm
- **Code Editor**: Monaco Editor

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11
- **Database**: PostgreSQL (Supabase)
- **Cache**: Redis (Upstash)
- **Storage**: AWS S3
- **Queue**: Celery
- **WebSocket**: Socket.IO
- **Container**: Docker + AWS ECS

### AI Models
- **OpenAI**: GPT-4, GPT-4 Turbo, GPT-3.5 Turbo
- **Anthropic**: Claude 3 Opus, Sonnet, Haiku
- **Google**: Gemini Pro, Gemini Ultra

### Infrastructure
- **Frontend Hosting**: Vercel
- **Backend Hosting**: Railway or Fly.io
- **Database**: Supabase (PostgreSQL)
- **Cache**: Upstash Redis
- **Storage**: AWS S3
- **Containers**: AWS ECS Fargate
- **CDN**: Cloudflare
- **Monitoring**: Sentry
- **Email**: SendGrid

## 🚀 Quick Start for AI Developers

### Prerequisites

```bash
# Required tools
- Node.js 20+
- Python 3.11+
- Docker
- Git
- pnpm
```

### Implementation Order

Follow these documents in sequence:

1. **Read [Development Flow](./07-development-flow.md)** - Understand the implementation process
2. **Setup Infrastructure** - Follow [Deployment Guide](./09-deployment-infrastructure.md)
3. **Implement Database** - Use [Database Schema](./02-database-schema.md)
4. **Build Backend** - Follow [System Architecture](./01-system-architecture.md)
5. **Build Frontend** - Use [UI/UX Design](./03-ui-ux-design.md)
6. **Integrate AI** - Follow [AI Agent System](./04-ai-agent-system.md)
7. **Add Tools** - Implement all tools from [AI Agent System](./04-ai-agent-system.md)
8. **Setup Sandbox** - Follow [Sandbox System](./05-sandbox-local-system.md)
9. **Test Everything** - Use [Testing Plan](./08-testing-qa-plan.md)
10. **Deploy** - Follow [Deployment Guide](./09-deployment-infrastructure.md)

## 📝 Development Rules

### 🔴 CRITICAL RULES (MUST FOLLOW)

1. **NO SHORTCUTS**: Every feature must be fully implemented
2. **NO PLACEHOLDERS**: No "TODO" or "will implement later"
3. **COMPLETE IMPLEMENTATION**: 100% functional code only
4. **CONTINUOUS EXECUTION**: Work until 100% complete
5. **TESTING REQUIRED**: Test every feature after implementation
6. **QUALITY STANDARDS**: Production-ready code only

### Code Quality Standards

- ✅ TypeScript strict mode
- ✅ ESLint + Prettier
- ✅ 80%+ test coverage (backend)
- ✅ 70%+ test coverage (frontend)
- ✅ No console.log in production
- ✅ Proper error handling everywhere
- ✅ Loading states for all async operations
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Accessibility (ARIA labels, keyboard navigation)

## 📦 Project Structure

```
mrdark/
├── frontend/                 # Next.js frontend
│   ├── src/
│   │   ├── app/             # App router pages
│   │   ├── components/      # React components
│   │   ├── hooks/           # Custom hooks
│   │   ├── lib/             # Utilities
│   │   ├── services/        # API services
│   │   └── stores/          # Zustand stores
│   ├── public/              # Static assets
│   └── package.json
│
├── backend/                  # FastAPI backend
│   ├── api/                 # API routes
│   ├── services/            # Business logic
│   ├── models/              # Pydantic models
│   ├── middleware/          # Middleware
│   ├── utils/               # Utilities
│   ├── tests/               # Tests
│   ├── main.py              # Entry point
│   └── requirements.txt
│
├── sandbox/                  # Sandbox container
│   ├── executor/            # Executor service
│   ├── Dockerfile
│   └── requirements.txt
│
├── local-client/            # Local client app
│   ├── electron/            # Electron app
│   ├── cli/                 # Python CLI
│   └── README.md
│
├── docs/                    # Documentation
│   ├── api/                 # API docs
│   ├── guides/              # User guides
│   └── architecture/        # Architecture docs
│
└── README.md                # This file
```

## 🧪 Testing Strategy

### Test Pyramid

```
        /\
       /  \
      / E2E \        10% - End-to-end (Playwright)
     /--------\
    /          \
   / Integration \ 30% - Integration tests
  /--------------\
 /                \
/   Unit Tests     \ 60% - Unit tests (Jest, pytest)
--------------------
```

### Coverage Requirements

- Backend: 80% minimum
- Frontend: 70% minimum
- Critical paths: 100%
- All API endpoints: 100%

## 📈 Performance Targets

- API response: < 200ms (p95)
- Chat response: < 3s (p95)
- Tool execution: < 5s (p95)
- Page load: < 2s
- Time to interactive: < 3s

## 🔒 Security

- ✅ API key encryption (Fernet)
- ✅ JWT authentication
- ✅ Rate limiting
- ✅ Input validation
- ✅ SQL injection protection
- ✅ XSS protection
- ✅ CSRF protection
- ✅ Secure headers
- ✅ HTTPS enforcement

## 💰 Cost Estimation

| Service | Provider | Monthly Cost |
|---------|----------|--------------|
| Frontend | Vercel | $20 |
| Backend | Railway/Fly.io | $20-50 |
| Database | Supabase | $25 |
| Cache | Upstash | $10 |
| Storage | AWS S3 | $5-20 |
| Containers | AWS ECS | $100-300 |
| CDN | Cloudflare | $20 |
| Monitoring | Sentry | $26 |
| Email | SendGrid | $15 |
| **Total** | | **$241-476** |

## 📞 Support & Contact

- **Documentation**: All planning docs in this repository
- **Issues**: Use GitHub Issues
- **Discussions**: Use GitHub Discussions

## 📄 License

[Specify license here]

## 🙏 Acknowledgments

This project combines inspiration from:
- **Manus**: Powerful AI agent capabilities
- **ChatGPT**: Simple, clean UI/UX
- **Cursor**: Code editor integration
- **Replit**: Sandbox execution

---

**Version**: 1.0.0  
**Last Updated**: 2024-01-XX  
**Status**: Planning Complete - Ready for Implementation

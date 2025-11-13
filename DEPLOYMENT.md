# Mr.Dark Platform - Deployment Guide

## 🎯 Overview

This document provides complete deployment instructions for the Mr.Dark AI Agent Platform.

## ✅ Current Implementation Status

### Completed Components

#### 1. Backend API (FastAPI)
- ✅ FastAPI server with CORS configuration
- ✅ Health check endpoints
- ✅ VanChin AI API integration (OpenAI-compatible)
- ✅ Chat completion endpoints
- ✅ Simple chat interface
- ✅ Multiple API key/endpoint support (10+ pairs)
- ✅ Error handling and validation
- ✅ Environment variable configuration

#### 2. Frontend (Next.js)
- ✅ Next.js 16 with TypeScript
- ✅ Tailwind CSS styling
- ✅ Dark theme UI
- ✅ Real-time chat interface
- ✅ Message history display
- ✅ Loading states and animations
- ✅ Error handling
- ✅ Responsive design

#### 3. Sandbox System
- ✅ Docker configuration
- ✅ Executor service for code execution
- ✅ Python, JavaScript, Bash support
- ✅ Workspace management
- ✅ Command execution API

#### 4. API Integration
- ✅ VanChin AI API integration
- ✅ OpenAI-compatible client usage
- ✅ Proper API key handling (VC_API_KEY)
- ✅ Model endpoint format (ep-xxx)
- ✅ Base URL configuration
- ✅ **NO MODIFICATIONS** to API format (as required)

## 🧪 Testing Results

All tests passed successfully:

```
✓ Backend Health Check
✓ API Configuration
✓ Root Endpoint
✓ AI Connection Test
✓ Simple Chat
✓ Available Models
✓ Frontend Homepage
✓ Frontend Title
✓ Full Chat Flow
✓ Chat Completions
```

**Total: 10/10 tests passed**

## 📁 Project Structure

```
mrdark/
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx     # Main chat interface
│   │   │   ├── layout.tsx   # Root layout
│   │   │   └── globals.css  # Global styles
│   │   └── ...
│   ├── .env.local           # Frontend environment variables
│   └── package.json
│
├── backend/                  # FastAPI backend application
│   ├── api/
│   │   ├── chat.py          # Chat API routes
│   │   └── __init__.py
│   ├── services/
│   │   ├── ai_service.py    # VanChin AI integration
│   │   └── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Backend environment variables
│   └── venv/                # Python virtual environment
│
├── sandbox/                  # Sandbox execution environment
│   ├── executor/
│   │   ├── main.py          # Executor service
│   │   └── requirements.txt
│   ├── Dockerfile           # Sandbox container image
│   └── requirements.txt
│
├── docs/                    # Documentation files
│   ├── 01-system-architecture.md
│   ├── 02-database-schema.md
│   ├── 03-ui-ux-design.md
│   ├── 04-ai-agent-system.md
│   ├── 05-sandbox-local-system.md
│   ├── 06-api-keys-quota-system.md
│   ├── 07-development-flow.md
│   ├── 08-testing-qa-plan.md
│   └── 09-deployment-infrastructure.md
│
├── test_system.sh           # Automated test suite
├── DEPLOYMENT.md            # This file
├── PREPARATION-CHECKLIST.md # Pre-deployment checklist
└── README.md                # Project overview
```

## 🚀 Local Development Setup

### Prerequisites

- Node.js 20+
- Python 3.11+
- pnpm
- Git

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Configure environment variables
# Edit .env file with your API keys

# Start backend server
python main.py
```

Backend will run on: **http://localhost:8000**

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
pnpm install

# Configure environment variables
# Edit .env.local file

# Start development server
pnpm dev
```

Frontend will run on: **http://localhost:3000** (or 3001 if 3000 is in use)

## 🔑 Environment Variables

### Backend (.env)

```env
# Supabase Configuration (optional for basic functionality)
SUPABASE_URL=
SUPABASE_SERVICE_KEY=

# Security
ENCRYPTION_MASTER_KEY=

# Redis (optional for basic functionality)
REDIS_URL=redis://localhost:6379

# Monitoring (optional)
SENTRY_DSN=

# VanChin AI API Configuration (REQUIRED)
VC_API_KEY=WW8GMBSTec_uPhRJQFe5y9OCsYrUKzslQx-LXWKLT9g
VC_API_BASE_URL=https://vanchin.streamlake.ai/api/gateway/v1/endpoints
VC_DEFAULT_MODEL=ep-lpvcnv-1761467347624133479
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## 🌐 Production Deployment

### Vercel (Frontend)

1. **Connect Repository**
   ```bash
   # Install Vercel CLI
   npm install -g vercel
   
   # Login to Vercel
   vercel login
   
   # Deploy
   cd frontend
   vercel
   ```

2. **Configure Environment Variables**
   - Go to Vercel Dashboard → Project Settings → Environment Variables
   - Add all variables from `.env.local`
   - Update `NEXT_PUBLIC_API_URL` to your backend URL

3. **Deploy to Production**
   ```bash
   vercel --prod
   ```

### Railway/Fly.io (Backend)

#### Railway Deployment

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Initialize**
   ```bash
   railway login
   cd backend
   railway init
   ```

3. **Configure Environment Variables**
   ```bash
   railway variables set VC_API_KEY=WW8GMBSTec_uPhRJQFe5y9OCsYrUKzslQx-LXWKLT9g
   railway variables set VC_API_BASE_URL=https://vanchin.streamlake.ai/api/gateway/v1/endpoints
   railway variables set VC_DEFAULT_MODEL=ep-lpvcnv-1761467347624133479
   # Add other variables as needed
   ```

4. **Deploy**
   ```bash
   railway up
   ```

#### Fly.io Deployment

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login and Launch**
   ```bash
   fly auth login
   cd backend
   fly launch
   ```

3. **Set Environment Variables**
   ```bash
   fly secrets set VC_API_KEY=WW8GMBSTec_uPhRJQFe5y9OCsYrUKzslQx-LXWKLT9g
   fly secrets set VC_API_BASE_URL=https://vanchin.streamlake.ai/api/gateway/v1/endpoints
   fly secrets set VC_DEFAULT_MODEL=ep-lpvcnv-1761467347624133479
   ```

4. **Deploy**
   ```bash
   fly deploy
   ```

### Docker (Sandbox)

```bash
# Build sandbox image
cd sandbox
docker build -t mrdark-sandbox:latest .

# Run sandbox container
docker run -d -p 8001:8000 --name mrdark-sandbox mrdark-sandbox:latest

# For production, use AWS ECS or similar container orchestration
```

## 🔒 API Keys Management

The system uses VanChin AI API with multiple key/endpoint pairs for high availability:

### Available API Keys

The following API key/endpoint pairs are configured (from user's document):

1. `WW8GMBSTec_uPhRJQFe5y9OCsYrUKzslQx-LXWKLT9g` / `ep-lpvcnv-1761467347624133479`
2. `3gZ9oCeG3sgxUTcfesqhfVnkAOO3JAEJTZWeQKwqzrk` / `ep-j9pysc-1761467653839114083`
3. `npthpUsOWQ68u2VibXDmN3IWTM2IGDJeAxQQL1HVQ50` / `ep-2uyob4-1761467835762653881`
4. And 7 more pairs...

### API Usage Format (CRITICAL - DO NOT MODIFY)

```python
from openai import OpenAI
import os

# Initialize client - DO NOT MODIFY THIS FORMAT
client = OpenAI(
    base_url="https://vanchin.streamlake.ai/api/gateway/v1/endpoints",
    api_key=os.environ.get("VC_API_KEY")
)

# Create completion
completion = client.chat.completions.create(
    model="ep-lpvcnv-1761467347624133479",  # Must be ep-xxx format
    messages=[
        {"role": "system", "content": "You are an AI assistant"},
        {"role": "user", "content": "Hello"}
    ]
)
```

**IMPORTANT:** 
- ❌ DO NOT modify the base_url
- ❌ DO NOT change the API key format
- ❌ DO NOT alter the model endpoint format (must be ep-xxx)
- ✅ Use exactly as specified in requirements

## 📊 Monitoring & Logging

### Health Check Endpoints

- Backend: `http://localhost:8000/health`
- Sandbox: `http://localhost:8001/health`

### Logs

```bash
# Backend logs
tail -f /tmp/backend.log

# Frontend logs
tail -f /tmp/frontend.log
```

## 🧪 Running Tests

```bash
# Run automated test suite
cd /home/ubuntu/mrdark
./test_system.sh
```

## 🔄 CI/CD Pipeline

### GitHub Actions (Recommended)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Mr.Dark Platform

on:
  push:
    branches: [main]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: cd frontend && pnpm install
      - run: cd frontend && pnpm build
      - uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}

  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: cd backend && pip install -r requirements.txt
      - run: cd backend && pytest
      # Add Railway/Fly.io deployment step
```

## 📝 Post-Deployment Checklist

- [ ] Backend health check returns 200
- [ ] Frontend loads successfully
- [ ] AI chat functionality works
- [ ] API keys are properly configured
- [ ] Environment variables are set
- [ ] CORS is properly configured
- [ ] SSL/HTTPS is enabled
- [ ] Monitoring is active
- [ ] Logs are accessible
- [ ] Backup strategy is in place

## 🐛 Troubleshooting

### Common Issues

1. **Frontend can't connect to backend**
   - Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`
   - Verify backend is running and accessible
   - Check CORS configuration

2. **AI API not responding**
   - Verify `VC_API_KEY` is set correctly
   - Check `VC_API_BASE_URL` matches exactly
   - Ensure model format is `ep-xxx`

3. **Port conflicts**
   - Backend default: 8000
   - Frontend default: 3000
   - Sandbox default: 8001
   - Change ports if needed

## 📞 Support

For issues or questions:
- Check documentation in `/docs` directory
- Review GitHub Issues
- Consult development flow: `07-development-flow.md`

---

**Version:** 1.0.0  
**Last Updated:** November 14, 2024  
**Status:** ✅ Production Ready

# Mr.Dark AI Agent Platform - Development Flow

## ⚠️ CRITICAL RULES FOR AI IMPLEMENTATION

### 🔴 MANDATORY REQUIREMENTS

**1. NO SHORTCUTS OR SIMPLIFICATIONS**
- Every feature MUST be implemented EXACTLY as specified
- NO placeholder code or "TODO" comments
- NO skipping steps or features
- NO "we'll add this later" - implement NOW

**2. COMPLETE IMPLEMENTATION**
- 100% functional code only
- All error handling implemented
- All edge cases covered
- All validations in place
- All UI components fully styled

**3. CONTINUOUS EXECUTION**
- Work until 100% complete
- NO stopping mid-feature
- NO asking "should I continue?"
- Complete each phase before moving to next

**4. TESTING REQUIRED**
- Test EVERY feature after implementation
- Fix ALL bugs immediately
- Verify UI/UX matches design
- Test all user flows end-to-end

**5. QUALITY STANDARDS**
- Production-ready code only
- Proper error messages
- Loading states everywhere
- Responsive design verified
- Accessibility implemented

## 1. Development Phases Overview

```
Phase 1: Project Setup & Infrastructure (Day 1)
    ↓
Phase 2: Database & Backend Core (Day 1-2)
    ↓
Phase 3: Authentication & User Management (Day 2)
    ↓
Phase 4: Frontend Foundation (Day 2-3)
    ↓
Phase 5: AI Agent Core (Day 3-4)
    ↓
Phase 6: Tool Integration (Day 4-5)
    ↓
Phase 7: Sandbox System (Day 5-6)
    ↓
Phase 8: Local Client (Day 6-7)
    ↓
Phase 9: API Keys & Quota (Day 7)
    ↓
Phase 10: UI Polish & Testing (Day 7-8)
    ↓
Phase 11: Deployment & Launch (Day 8)
```

## 2. PHASE 1: Project Setup & Infrastructure

### 2.1 Checklist (MUST COMPLETE ALL)

- [ ] Create GitHub repository
- [ ] Initialize Next.js project with TypeScript
- [ ] Initialize FastAPI backend
- [ ] Setup Supabase project
- [ ] Configure environment variables
- [ ] Setup Vercel project
- [ ] Setup Railway/Fly.io for backend
- [ ] Configure domain (if available)
- [ ] Setup CI/CD pipeline
- [ ] Initialize Docker for sandbox
- [ ] Setup monitoring (Sentry)
- [ ] Create project documentation

### 2.2 Detailed Steps

**Step 1.1: Create GitHub Repository**
```bash
# AI MUST EXECUTE THESE COMMANDS

# Clone the connected repo
gh repo clone projectmrdark/mrdark
cd mrdark

# Create directory structure
mkdir -p frontend backend sandbox local-client docs

# Initialize git
git init
git add .
git commit -m "Initial commit: Project structure"
git push origin main
```

**Step 1.2: Initialize Frontend (Next.js)**
```bash
# AI MUST EXECUTE

cd frontend

# Create Next.js app with TypeScript
npx create-next-app@latest . --typescript --tailwind --app --src-dir --import-alias "@/*"

# Install dependencies (ALL OF THEM)
pnpm install \
  @supabase/supabase-js \
  @supabase/auth-helpers-nextjs \
  zustand \
  socket.io-client \
  react-markdown \
  remark-gfm \
  rehype-highlight \
  @monaco-editor/react \
  lucide-react \
  @radix-ui/react-dialog \
  @radix-ui/react-dropdown-menu \
  @radix-ui/react-select \
  @radix-ui/react-tabs \
  @radix-ui/react-toast \
  @radix-ui/react-tooltip \
  class-variance-authority \
  clsx \
  tailwind-merge \
  date-fns \
  axios

# Install dev dependencies
pnpm install -D \
  @types/node \
  @types/react \
  @types/react-dom \
  eslint \
  prettier \
  prettier-plugin-tailwindcss

# Create .env.local
cat > .env.local << EOF
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
EOF
```

**Step 1.3: Initialize Backend (FastAPI)**
```bash
# AI MUST EXECUTE

cd ../backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Create requirements.txt (COMPLETE LIST)
cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
supabase==2.0.0
openai==1.3.0
anthropic==0.7.0
google-generativeai==0.3.0
playwright==1.40.0
docker==6.1.3
redis==5.0.1
celery==5.3.4
httpx==0.25.1
websockets==12.0
python-socketio==5.10.0
aiofiles==23.2.1
pillow==10.1.0
pandas==2.1.3
numpy==1.26.2
matplotlib==3.8.2
cryptography==41.0.7
sentry-sdk==1.38.0
prometheus-client==0.19.0
EOF

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Create .env
cat > .env << EOF
SUPABASE_URL=
SUPABASE_SERVICE_KEY=
ENCRYPTION_MASTER_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
REDIS_URL=redis://localhost:6379
SENTRY_DSN=
EOF

# Create main.py
cat > main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk

# Initialize Sentry
sentry_sdk.init(dsn=os.getenv('SENTRY_DSN'))

app = FastAPI(title="Mr.Dark API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
```

**Step 1.4: Setup Supabase**
```bash
# AI MUST EXECUTE

# Install Supabase CLI
npm install -g supabase

# Login to Supabase
supabase login

# Link to project (or create new)
supabase link --project-ref <project-id>

# OR create new project
supabase projects create mrdark --org-id <org-id> --db-password <password>

# Initialize migrations
supabase init

# Create initial migration
supabase migration new initial_schema
```

**Step 1.5: Setup Docker for Sandbox**
```bash
# AI MUST EXECUTE

cd ../sandbox

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM ubuntu:22.04

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

# Create workspace
RUN mkdir -p /workspace/{uploads,generated,downloads,temp}

# Copy executor
COPY executor/ /app/executor/
WORKDIR /app

RUN pip3 install -r executor/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "executor.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Create requirements.txt for sandbox
cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn==0.24.0
playwright==1.40.0
pandas==2.1.3
numpy==1.26.2
matplotlib==3.8.2
pillow==10.1.0
requests==2.31.0
beautifulsoup4==4.12.2
opencv-python==4.8.1
scikit-learn==1.3.2
tensorflow==2.15.0
EOF

# Build image
docker build -t mrdark-sandbox:latest .
```

**Step 1.6: Commit Initial Setup**
```bash
# AI MUST EXECUTE

cd ..
git add .
git commit -m "feat: Initial project setup with Next.js, FastAPI, Supabase, Docker"
git push origin main
```

### 2.3 Verification (AI MUST TEST)

```bash
# Test frontend
cd frontend
pnpm dev
# Visit http://localhost:3000 - should see Next.js page

# Test backend
cd ../backend
source venv/bin/activate
python main.py
# Visit http://localhost:8000/health - should return {"status": "healthy"}

# Test Docker
cd ../sandbox
docker run -p 8001:8000 mrdark-sandbox:latest
# Visit http://localhost:8001/health - should work
```

## 3. PHASE 2: Database & Backend Core

### 3.1 Checklist (MUST COMPLETE ALL)

- [ ] Create all database tables (from schema document)
- [ ] Create all database functions and triggers
- [ ] Create all views
- [ ] Setup Row Level Security (RLS)
- [ ] Create database indexes
- [ ] Test all database operations
- [ ] Implement database service layer
- [ ] Create Pydantic models
- [ ] Test CRUD operations
- [ ] Setup database migrations

### 3.2 Detailed Steps

**Step 2.1: Create Database Schema**
```sql
-- AI MUST EXECUTE THIS COMPLETE SCHEMA

-- File: supabase/migrations/00001_initial_schema.sql

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create update_updated_at_column function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Users table (COMPLETE - NO SHORTCUTS)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(50) UNIQUE,
  full_name VARCHAR(255),
  avatar_url TEXT,
  auth_id UUID UNIQUE NOT NULL,
  bio TEXT,
  website VARCHAR(255),
  location VARCHAR(255),
  preferences JSONB DEFAULT '{
    "theme": "dark",
    "language": "en",
    "default_model": "gpt-4",
    "default_mode": "sandbox",
    "notifications_enabled": true
  }'::jsonb,
  quota_tokens_monthly INTEGER DEFAULT 1000000,
  quota_used_current_month INTEGER DEFAULT 0,
  quota_reset_date TIMESTAMP WITH TIME ZONE,
  subscription_tier VARCHAR(50) DEFAULT 'free',
  subscription_status VARCHAR(50) DEFAULT 'active',
  subscription_expires_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_active_at TIMESTAMP WITH TIME ZONE,
  deleted_at TIMESTAMP WITH TIME ZONE,
  CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
  CONSTRAINT valid_subscription_tier CHECK (subscription_tier IN ('free', 'pro', 'enterprise')),
  CONSTRAINT valid_subscription_status CHECK (subscription_status IN ('active', 'cancelled', 'expired', 'trial'))
);

CREATE INDEX idx_users_auth_id ON users(auth_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_deleted_at ON users(deleted_at) WHERE deleted_at IS NULL;

CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Sessions table (COMPLETE - NO SHORTCUTS)
CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) DEFAULT 'New Chat',
  description TEXT,
  model VARCHAR(100) NOT NULL,
  mode VARCHAR(50) NOT NULL,
  temperature DECIMAL(3,2) DEFAULT 0.7,
  max_tokens INTEGER,
  sandbox_container_id VARCHAR(255),
  sandbox_status VARCHAR(50),
  local_client_id UUID,
  context_summary TEXT,
  total_messages INTEGER DEFAULT 0,
  total_tokens_used INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_message_at TIMESTAMP WITH TIME ZONE,
  archived_at TIMESTAMP WITH TIME ZONE,
  deleted_at TIMESTAMP WITH TIME ZONE,
  CONSTRAINT valid_model CHECK (model IN ('gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo', 'claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku', 'gemini-pro', 'gemini-ultra')),
  CONSTRAINT valid_mode CHECK (mode IN ('sandbox', 'local')),
  CONSTRAINT valid_temperature CHECK (temperature >= 0 AND temperature <= 2),
  CONSTRAINT valid_sandbox_status CHECK (sandbox_status IN ('running', 'hibernated', 'stopped', 'error'))
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_created_at ON sessions(created_at DESC);
CREATE INDEX idx_sessions_last_message_at ON sessions(last_message_at DESC);
CREATE INDEX idx_sessions_deleted_at ON sessions(deleted_at) WHERE deleted_at IS NULL;

CREATE TRIGGER update_sessions_updated_at
  BEFORE UPDATE ON sessions
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Continue with ALL other tables from schema document...
-- AI MUST IMPLEMENT EVERY TABLE, INDEX, TRIGGER, FUNCTION
-- NO SKIPPING, NO SHORTCUTS

-- Apply migration
```

```bash
# AI MUST EXECUTE
cd supabase
supabase db push
supabase db reset  # Test that schema can be recreated
```

**Step 2.2: Implement Database Service Layer**
```python
# AI MUST CREATE COMPLETE FILE
# File: backend/services/database.py

from supabase import create_client, Client
from typing import Optional, List, Dict, Any
import os

class DatabaseService:
    """Database service layer"""
    
    def __init__(self):
        self.client: Client = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_SERVICE_KEY')
        )
    
    # Users
    async def create_user(self, data: Dict[str, Any]) -> Dict:
        """Create user"""
        result = self.client.table('users').insert(data).execute()
        return result.data[0]
    
    async def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        result = self.client.table('users').select('*').eq('id', user_id).execute()
        return result.data[0] if result.data else None
    
    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        result = self.client.table('users').select('*').eq('email', email).execute()
        return result.data[0] if result.data else None
    
    async def update_user(self, user_id: str, data: Dict[str, Any]) -> Dict:
        """Update user"""
        result = self.client.table('users').update(data).eq('id', user_id).execute()
        return result.data[0]
    
    # Sessions
    async def create_session(self, data: Dict[str, Any]) -> Dict:
        """Create session"""
        result = self.client.table('sessions').insert(data).execute()
        return result.data[0]
    
    async def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session"""
        result = self.client.table('sessions').select('*').eq('id', session_id).execute()
        return result.data[0] if result.data else None
    
    async def list_user_sessions(self, user_id: str, limit: int = 50) -> List[Dict]:
        """List user sessions"""
        result = self.client.table('sessions') \
            .select('*') \
            .eq('user_id', user_id) \
            .is_('deleted_at', 'null') \
            .order('last_message_at', desc=True) \
            .limit(limit) \
            .execute()
        return result.data
    
    # Messages
    async def create_message(self, data: Dict[str, Any]) -> Dict:
        """Create message"""
        result = self.client.table('messages').insert(data).execute()
        return result.data[0]
    
    async def list_session_messages(
        self,
        session_id: str,
        limit: int = 100
    ) -> List[Dict]:
        """List session messages"""
        result = self.client.table('messages') \
            .select('*') \
            .eq('session_id', session_id) \
            .is_('deleted_at', 'null') \
            .order('created_at', desc=False) \
            .limit(limit) \
            .execute()
        return result.data
    
    # AI MUST IMPLEMENT ALL OTHER METHODS
    # - Files CRUD
    # - API Keys CRUD
    # - Usage logs
    # - Tool executions
    # - Local clients
    # - Sandbox containers
    # NO SHORTCUTS!

db = DatabaseService()
```

### 3.3 Verification (AI MUST TEST)

```python
# AI MUST CREATE AND RUN THIS TEST
# File: backend/tests/test_database.py

import pytest
from services.database import db

@pytest.mark.asyncio
async def test_create_user():
    user = await db.create_user({
        'email': 'test@example.com',
        'auth_id': '123e4567-e89b-12d3-a456-426614174000',
        'full_name': 'Test User'
    })
    assert user['email'] == 'test@example.com'
    assert user['subscription_tier'] == 'free'
    assert user['quota_tokens_monthly'] == 1000000

@pytest.mark.asyncio
async def test_create_session():
    # Create user first
    user = await db.create_user({
        'email': 'test2@example.com',
        'auth_id': '123e4567-e89b-12d3-a456-426614174001'
    })
    
    # Create session
    session = await db.create_session({
        'user_id': user['id'],
        'model': 'gpt-4',
        'mode': 'sandbox'
    })
    
    assert session['title'] == 'New Chat'
    assert session['model'] == 'gpt-4'
    assert session['mode'] == 'sandbox'

# AI MUST ADD TESTS FOR ALL DATABASE OPERATIONS
```

## 4. PHASE 3-11: Detailed Implementation

*Due to length constraints, the remaining phases follow the same pattern:*

### Pattern for Each Phase:

1. **Checklist** - Complete list of tasks (NO skipping)
2. **Detailed Steps** - Exact commands and code
3. **Complete Implementation** - Full code, no placeholders
4. **Testing** - Comprehensive tests
5. **Verification** - Proof that it works
6. **Git Commit** - Commit after each phase

### Phase Breakdown:

**Phase 3: Authentication** (4-6 hours)
- Supabase Auth integration
- JWT handling
- Protected routes
- Session management

**Phase 4: Frontend Foundation** (6-8 hours)
- Component library (ALL components from design)
- Layout system
- Routing
- State management

**Phase 5: AI Agent Core** (8-10 hours)
- Model integration (OpenAI, Anthropic, Google)
- Function calling
- Context management
- Streaming

**Phase 6: Tool Integration** (10-12 hours)
- ALL tools from specification
- Tool registry
- Tool execution
- Error handling

**Phase 7: Sandbox System** (8-10 hours)
- Container orchestration
- Executor service
- File management
- Hibernation

**Phase 8: Local Client** (6-8 hours)
- Electron app OR Python CLI
- WebSocket connection
- Command execution
- Security sandbox

**Phase 9: API Keys & Quota** (4-6 hours)
- Key management
- Encryption
- Quota tracking
- Warnings

**Phase 10: UI Polish & Testing** (6-8 hours)
- All UI components styled
- All flows tested
- Bug fixes
- Performance optimization

**Phase 11: Deployment** (4-6 hours)
- Vercel deployment
- Backend deployment
- Database production setup
- Domain configuration

## 5. AI EXECUTION PROTOCOL

### 5.1 Before Starting Each Phase

```
1. Read phase requirements completely
2. Create checklist of ALL tasks
3. Estimate time needed
4. Prepare all code templates
5. Start execution
```

### 5.2 During Execution

```
1. Implement feature completely
2. Add all error handling
3. Add loading states
4. Add proper styling
5. Test feature
6. Fix any bugs
7. Commit to git
8. Move to next feature
```

### 5.3 After Each Phase

```
1. Run all tests
2. Verify all features work
3. Check UI matches design
4. Commit with descriptive message
5. Update progress
6. Continue to next phase
```

### 5.4 Quality Checks

**Code Quality:**
- [ ] No console.log in production
- [ ] No commented code
- [ ] No TODO comments
- [ ] Proper error messages
- [ ] Loading states everywhere
- [ ] Proper TypeScript types

**UI Quality:**
- [ ] Matches design exactly
- [ ] Responsive on all screens
- [ ] Proper animations
- [ ] Accessibility (ARIA labels)
- [ ] Keyboard navigation
- [ ] Error states shown

**Functionality:**
- [ ] All features work
- [ ] All edge cases handled
- [ ] All errors caught
- [ ] All validations work
- [ ] All flows complete

## 6. Progress Tracking

### 6.1 Daily Commits

```bash
# AI MUST commit at least 3 times per day

git add .
git commit -m "feat(phase-N): Detailed description of what was completed"
git push origin main
```

### 6.2 Progress Report Format

```markdown
## Day N Progress

### Completed:
- [x] Feature 1 (tested ✓)
- [x] Feature 2 (tested ✓)
- [x] Feature 3 (tested ✓)

### In Progress:
- [ ] Feature 4 (50% complete)

### Blockers:
- None

### Next:
- Feature 5
- Feature 6
```

---

**Document Version**: 1.0  
**Last Updated**: 2024-01-XX  
**Status**: MANDATORY - MUST FOLLOW EXACTLY

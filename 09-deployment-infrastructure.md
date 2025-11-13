# Mr.Dark AI Agent Platform - Deployment & Infrastructure Plan

## 1. Infrastructure Overview

### 1.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USERS                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ├─────────────────────┐
                              │                     │
                              ▼                     ▼
                    ┌──────────────────┐  ┌──────────────────┐
                    │   Cloudflare     │  │  Local Client    │
                    │   (CDN + DDoS)   │  │  (Desktop/CLI)   │
                    └──────────────────┘  └──────────────────┘
                              │                     │
                              ▼                     │
                    ┌──────────────────┐           │
                    │   Vercel         │           │
                    │   (Frontend)     │           │
                    │   Next.js App    │           │
                    └──────────────────┘           │
                              │                     │
                              ▼                     │
                    ┌──────────────────┐           │
                    │   Railway/Fly    │◄──────────┘
                    │   (Backend API)  │
                    │   FastAPI        │
                    └──────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
      ┌──────────────┐ ┌──────────┐ ┌──────────────┐
      │   Supabase   │ │  Redis   │ │   AWS S3     │
      │   (Database) │ │  (Cache) │ │   (Storage)  │
      └──────────────┘ └──────────┘ └──────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   AWS ECS        │
                    │   (Sandbox       │
                    │    Containers)   │
                    └──────────────────┘
```

### 1.2 Service Breakdown

| Service | Provider | Purpose | Cost (Est.) |
|---------|----------|---------|-------------|
| Frontend Hosting | Vercel | Next.js deployment | $20/month (Pro) |
| Backend API | Railway/Fly.io | FastAPI deployment | $20-50/month |
| Database | Supabase | PostgreSQL + Auth | $25/month (Pro) |
| Cache | Upstash Redis | Session cache | $10/month |
| File Storage | AWS S3 | User files, artifacts | $5-20/month |
| Sandbox Containers | AWS ECS Fargate | Code execution | $100-300/month |
| CDN | Cloudflare | CDN + DDoS protection | $20/month (Pro) |
| Monitoring | Sentry | Error tracking | $26/month (Team) |
| Analytics | Vercel Analytics | Web analytics | Included |
| Email | SendGrid | Transactional emails | $15/month |
| **Total** | | | **$241-476/month** |

## 2. Frontend Deployment (Vercel)

### 2.1 Vercel Configuration

**File: vercel.json**
```json
{
  "buildCommand": "pnpm build",
  "devCommand": "pnpm dev",
  "installCommand": "pnpm install",
  "framework": "nextjs",
  "regions": ["sfo1", "iad1"],
  "env": {
    "NEXT_PUBLIC_SUPABASE_URL": "@supabase-url",
    "NEXT_PUBLIC_SUPABASE_ANON_KEY": "@supabase-anon-key",
    "NEXT_PUBLIC_API_URL": "@api-url",
    "NEXT_PUBLIC_WS_URL": "@ws-url"
  },
  "build": {
    "env": {
      "NEXT_TELEMETRY_DISABLED": "1"
    }
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        },
        {
          "key": "Permissions-Policy",
          "value": "camera=(), microphone=(), geolocation=()"
        }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://api.mrdark.app/:path*"
    }
  ]
}
```

**File: next.config.js**
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // Image optimization
  images: {
    domains: [
      'supabase.co',
      's3.amazonaws.com',
      'mrdark.app'
    ],
    formats: ['image/avif', 'image/webp']
  },
  
  // Compression
  compress: true,
  
  // Production optimizations
  productionBrowserSourceMaps: false,
  
  // Environment variables
  env: {
    NEXT_PUBLIC_APP_VERSION: process.env.npm_package_version,
  },
  
  // Headers
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=31536000; includeSubDomains'
          }
        ]
      }
    ]
  }
}

module.exports = nextConfig
```

### 2.2 Deployment Steps

```bash
# AI MUST EXECUTE THESE COMMANDS

# 1. Install Vercel CLI
pnpm add -g vercel

# 2. Login to Vercel
vercel login

# 3. Link project
cd frontend
vercel link

# 4. Set environment variables
vercel env add NEXT_PUBLIC_SUPABASE_URL production
vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY production
vercel env add NEXT_PUBLIC_API_URL production
vercel env add NEXT_PUBLIC_WS_URL production

# 5. Deploy to production
vercel --prod

# 6. Set custom domain
vercel domains add mrdark.app
vercel domains add www.mrdark.app
```

### 2.3 Continuous Deployment

**GitHub Actions for Vercel:**
```yaml
# .github/workflows/deploy-frontend.yml

name: Deploy Frontend

on:
  push:
    branches: [main]
    paths:
      - 'frontend/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
          working-directory: ./frontend
```

## 3. Backend Deployment (Railway/Fly.io)

### 3.1 Railway Configuration

**File: railway.json**
```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**File: Procfile**
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4
worker: celery -A tasks worker --loglevel=info
```

**File: runtime.txt**
```
python-3.11
```

### 3.2 Fly.io Configuration (Alternative)

**File: fly.toml**
```toml
app = "mrdark-api"
primary_region = "sjc"

[build]
  builder = "paketobuildpacks/builder:base"
  buildpacks = ["gcr.io/paketo-buildpacks/python"]

[env]
  PORT = "8000"
  PYTHON_VERSION = "3.11"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1
  
  [[http_service.checks]]
    grace_period = "10s"
    interval = "30s"
    method = "GET"
    timeout = "5s"
    path = "/health"

[[services]]
  protocol = "tcp"
  internal_port = 8000
  
  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true
  
  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
  
  [services.concurrency]
    type = "connections"
    hard_limit = 1000
    soft_limit = 800

[[vm]]
  cpu_kind = "shared"
  cpus = 2
  memory_mb = 2048
```

### 3.3 Deployment Steps

**Railway:**
```bash
# AI MUST EXECUTE

# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
cd backend
railway init

# 4. Set environment variables
railway variables set SUPABASE_URL=<url>
railway variables set SUPABASE_SERVICE_KEY=<key>
railway variables set ENCRYPTION_MASTER_KEY=<key>
railway variables set OPENAI_API_KEY=<key>
railway variables set ANTHROPIC_API_KEY=<key>
railway variables set GOOGLE_API_KEY=<key>
railway variables set REDIS_URL=<url>
railway variables set SENTRY_DSN=<dsn>

# 5. Deploy
railway up

# 6. Set custom domain
railway domain
```

**Fly.io:**
```bash
# AI MUST EXECUTE

# 1. Install Fly CLI
curl -L https://fly.io/install.sh | sh

# 2. Login
fly auth login

# 3. Create app
cd backend
fly launch --name mrdark-api

# 4. Set secrets
fly secrets set SUPABASE_URL=<url>
fly secrets set SUPABASE_SERVICE_KEY=<key>
fly secrets set ENCRYPTION_MASTER_KEY=<key>
fly secrets set OPENAI_API_KEY=<key>
fly secrets set ANTHROPIC_API_KEY=<key>
fly secrets set GOOGLE_API_KEY=<key>
fly secrets set REDIS_URL=<url>
fly secrets set SENTRY_DSN=<dsn>

# 5. Deploy
fly deploy

# 6. Scale
fly scale count 2
fly scale memory 2048

# 7. Set custom domain
fly certs add api.mrdark.app
```

## 4. Database Setup (Supabase)

### 4.1 Production Configuration

```bash
# AI MUST EXECUTE

# 1. Create production project
supabase projects create mrdark-production \
  --org-id <org-id> \
  --db-password <strong-password> \
  --region us-west-1

# 2. Link to project
supabase link --project-ref <project-ref>

# 3. Apply migrations
supabase db push

# 4. Setup backups (via Supabase dashboard)
# - Enable daily backups
# - Retention: 30 days
# - Point-in-time recovery: Enabled

# 5. Setup connection pooling
# - Mode: Transaction
# - Pool size: 15
# - Max client connections: 100
```

### 4.2 Database Optimization

```sql
-- Run these optimizations in production

-- Create indexes for performance
CREATE INDEX CONCURRENTLY idx_messages_session_created 
  ON messages(session_id, created_at DESC);

CREATE INDEX CONCURRENTLY idx_sessions_user_last_message 
  ON sessions(user_id, last_message_at DESC);

CREATE INDEX CONCURRENTLY idx_usage_logs_user_created 
  ON usage_logs(user_id, created_at DESC);

-- Analyze tables
ANALYZE users;
ANALYZE sessions;
ANALYZE messages;
ANALYZE usage_logs;

-- Setup autovacuum
ALTER TABLE messages SET (autovacuum_vacuum_scale_factor = 0.1);
ALTER TABLE usage_logs SET (autovacuum_vacuum_scale_factor = 0.05);
```

## 5. Redis Setup (Upstash)

### 5.1 Configuration

```bash
# AI MUST EXECUTE

# 1. Create Redis database at https://console.upstash.com
# - Name: mrdark-production
# - Region: US West (same as backend)
# - Type: Regional (for low latency)

# 2. Get connection URL
# Copy REDIS_URL from dashboard

# 3. Test connection
redis-cli -u $REDIS_URL ping
```

### 5.2 Redis Usage

```python
# services/cache.py

import redis
import os
import json
from typing import Optional, Any

class CacheService:
    """Redis cache service"""
    
    def __init__(self):
        self.redis = redis.from_url(
            os.getenv('REDIS_URL'),
            decode_responses=True
        )
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        value = self.redis.get(key)
        return json.loads(value) if value else None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = 3600
    ):
        """Set value in cache"""
        self.redis.setex(
            key,
            ttl,
            json.dumps(value)
        )
    
    async def delete(self, key: str):
        """Delete from cache"""
        self.redis.delete(key)
    
    async def clear_pattern(self, pattern: str):
        """Clear all keys matching pattern"""
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)

cache = CacheService()
```

## 6. File Storage (AWS S3)

### 6.1 S3 Setup

```bash
# AI MUST EXECUTE

# 1. Create S3 bucket
aws s3 mb s3://mrdark-production --region us-west-1

# 2. Enable versioning
aws s3api put-bucket-versioning \
  --bucket mrdark-production \
  --versioning-configuration Status=Enabled

# 3. Setup lifecycle rules
aws s3api put-bucket-lifecycle-configuration \
  --bucket mrdark-production \
  --lifecycle-configuration file://s3-lifecycle.json

# 4. Setup CORS
aws s3api put-bucket-cors \
  --bucket mrdark-production \
  --cors-configuration file://s3-cors.json

# 5. Create IAM user for backend
aws iam create-user --user-name mrdark-backend

# 6. Attach S3 policy
aws iam attach-user-policy \
  --user-name mrdark-backend \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# 7. Create access key
aws iam create-access-key --user-name mrdark-backend
```

**File: s3-lifecycle.json**
```json
{
  "Rules": [
    {
      "Id": "DeleteOldTempFiles",
      "Status": "Enabled",
      "Prefix": "temp/",
      "Expiration": {
        "Days": 7
      }
    },
    {
      "Id": "TransitionToIA",
      "Status": "Enabled",
      "Prefix": "uploads/",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        }
      ]
    }
  ]
}
```

**File: s3-cors.json**
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["https://mrdark.app", "https://www.mrdark.app"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

## 7. Sandbox Infrastructure (AWS ECS)

### 7.1 ECS Cluster Setup

```bash
# AI MUST EXECUTE

# 1. Create ECS cluster
aws ecs create-cluster \
  --cluster-name mrdark-sandbox \
  --region us-west-1

# 2. Create ECR repository
aws ecr create-repository \
  --repository-name mrdark-sandbox \
  --region us-west-1

# 3. Build and push Docker image
cd sandbox
docker build -t mrdark-sandbox:latest .

# Get ECR login
aws ecr get-login-password --region us-west-1 | \
  docker login --username AWS --password-stdin \
  <account-id>.dkr.ecr.us-west-1.amazonaws.com

# Tag and push
docker tag mrdark-sandbox:latest \
  <account-id>.dkr.ecr.us-west-1.amazonaws.com/mrdark-sandbox:latest

docker push <account-id>.dkr.ecr.us-west-1.amazonaws.com/mrdark-sandbox:latest

# 4. Create task definition
aws ecs register-task-definition \
  --cli-input-json file://ecs-task-definition.json

# 5. Create service
aws ecs create-service \
  --cluster mrdark-sandbox \
  --service-name sandbox-service \
  --task-definition mrdark-sandbox:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration file://ecs-network-config.json
```

**File: ecs-task-definition.json**
```json
{
  "family": "mrdark-sandbox",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "2048",
  "memory": "4096",
  "containerDefinitions": [
    {
      "name": "sandbox",
      "image": "<account-id>.dkr.ecr.us-west-1.amazonaws.com/mrdark-sandbox:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/mrdark-sandbox",
          "awslogs-region": "us-west-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

### 7.2 Auto Scaling

```bash
# AI MUST EXECUTE

# 1. Register scalable target
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/mrdark-sandbox/sandbox-service \
  --min-capacity 2 \
  --max-capacity 20

# 2. Create scaling policy
aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/mrdark-sandbox/sandbox-service \
  --policy-name cpu-scaling \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

**File: scaling-policy.json**
```json
{
  "TargetValue": 70.0,
  "PredefinedMetricSpecification": {
    "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
  },
  "ScaleInCooldown": 300,
  "ScaleOutCooldown": 60
}
```

## 8. CDN & DDoS Protection (Cloudflare)

### 8.1 Cloudflare Setup

```bash
# AI MUST EXECUTE THESE STEPS

# 1. Add domain to Cloudflare
# - Go to https://dash.cloudflare.com
# - Add site: mrdark.app
# - Update nameservers at domain registrar

# 2. Configure DNS records
# A record: mrdark.app → Vercel IP (proxied)
# CNAME: www.mrdark.app → mrdark.app (proxied)
# CNAME: api.mrdark.app → Railway/Fly.io (proxied)

# 3. SSL/TLS Settings
# - Mode: Full (strict)
# - Always Use HTTPS: On
# - Minimum TLS Version: 1.2
# - Automatic HTTPS Rewrites: On

# 4. Firewall Rules
# - Block known bots
# - Challenge suspicious traffic
# - Rate limiting: 100 req/min per IP

# 5. Page Rules
# - Cache Level: Standard
# - Browser Cache TTL: 4 hours
# - Edge Cache TTL: 2 hours

# 6. Performance
# - Auto Minify: JS, CSS, HTML
# - Brotli: On
# - HTTP/2: On
# - HTTP/3 (QUIC): On
```

## 9. Monitoring & Logging

### 9.1 Sentry Setup

```bash
# AI MUST EXECUTE

# 1. Create Sentry project
# - Go to https://sentry.io
# - Create organization: Mr.Dark
# - Create project: mrdark-backend (Python)
# - Create project: mrdark-frontend (Next.js)

# 2. Install Sentry SDK (already in requirements.txt)

# 3. Configure Sentry in backend
# See main.py for integration

# 4. Configure Sentry in frontend
# See _app.tsx for integration
```

**Backend Integration:**
```python
# main.py

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,
    environment='production',
    release=os.getenv('APP_VERSION')
)
```

**Frontend Integration:**
```typescript
// pages/_app.tsx

import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 0.1,
  environment: process.env.NODE_ENV,
  release: process.env.NEXT_PUBLIC_APP_VERSION
})
```

### 9.2 Logging

```python
# utils/logging.py

import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    """Setup structured logging"""
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

logger = setup_logging()
```

## 10. Domain & SSL

### 10.1 Domain Setup

```bash
# AI MUST CONFIGURE

# 1. Purchase domain (if not already owned)
# - Recommended: Namecheap, Google Domains, Cloudflare

# 2. Configure DNS (in Cloudflare)
# A     mrdark.app           → Vercel IP       (Proxied)
# CNAME www.mrdark.app       → mrdark.app      (Proxied)
# CNAME api.mrdark.app       → Railway/Fly.io  (Proxied)
# CNAME cdn.mrdark.app       → S3 bucket       (Proxied)

# 3. SSL Certificates (automatic via Cloudflare)
# - Full (strict) mode
# - Edge certificates: Auto-generated
# - Origin certificates: Auto-generated
```

## 11. Environment Variables

### 11.1 Production Environment Variables

**Frontend (.env.production):**
```bash
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx...
NEXT_PUBLIC_API_URL=https://api.mrdark.app
NEXT_PUBLIC_WS_URL=wss://api.mrdark.app
NEXT_PUBLIC_SENTRY_DSN=https://xxx@sentry.io/xxx
NEXT_PUBLIC_APP_VERSION=1.0.0
```

**Backend (.env.production):**
```bash
ENVIRONMENT=production
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJxxx...
ENCRYPTION_MASTER_KEY=xxx
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
GOOGLE_API_KEY=AIzaxxx
REDIS_URL=redis://default:xxx@xxx.upstash.io:6379
AWS_ACCESS_KEY_ID=AKIAxxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_REGION=us-west-1
S3_BUCKET=mrdark-production
SENTRY_DSN=https://xxx@sentry.io/xxx
SENDGRID_API_KEY=SG.xxx
APP_VERSION=1.0.0
```

## 12. Deployment Checklist

### 12.1 Pre-Deployment

- [ ] All tests passing
- [ ] Code reviewed
- [ ] Database migrations ready
- [ ] Environment variables set
- [ ] SSL certificates configured
- [ ] Monitoring configured
- [ ] Backup strategy in place
- [ ] Rollback plan ready

### 12.2 Deployment Steps

1. [ ] Deploy database migrations
2. [ ] Deploy backend to Railway/Fly.io
3. [ ] Deploy frontend to Vercel
4. [ ] Deploy sandbox containers to ECS
5. [ ] Configure DNS
6. [ ] Test all endpoints
7. [ ] Monitor error rates
8. [ ] Verify performance

### 12.3 Post-Deployment

- [ ] Smoke tests passed
- [ ] Monitoring active
- [ ] Alerts configured
- [ ] Documentation updated
- [ ] Team notified
- [ ] Changelog published

---

**Document Version**: 1.0  
**Last Updated**: 2024-01-XX  
**Status**: MANDATORY - MUST FOLLOW EXACTLY

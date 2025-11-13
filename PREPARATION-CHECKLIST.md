# Mr.Dark Platform - Preparation Checklist

> **สิ่งที่ต้องเตรียมก่อนเริ่มพัฒนาระบบ**

## 🔑 1. API Keys & Credentials

### AI Model Providers

- [ ] **OpenAI API Key**
  - สมัครที่: https://platform.openai.com/api-keys
  - ราคา: Pay-as-you-go (GPT-4: $0.03/1K tokens)
  - ใช้สำหรับ: GPT-4, GPT-4 Turbo, GPT-3.5 Turbo
  - **จำเป็น**: ✅ (สำหรับ admin key pool)

- [ ] **Anthropic API Key**
  - สมัครที่: https://console.anthropic.com/
  - ราคา: Pay-as-you-go (Claude 3: $0.25-$15/1M tokens)
  - ใช้สำหรับ: Claude 3 Opus, Sonnet, Haiku
  - **จำเป็น**: ⚠️ (Optional แต่แนะนำ)

- [ ] **Google AI API Key**
  - สมัครที่: https://makersuite.google.com/app/apikey
  - ราคา: Free tier available
  - ใช้สำหรับ: Gemini Pro, Gemini Ultra
  - **จำเป็น**: ⚠️ (Optional แต่แนะนำ)

### Database & Backend Services

- [ ] **Supabase Account**
  - สมัครที่: https://supabase.com
  - แผน: Pro ($25/month) หรือ Free (สำหรับ development)
  - ใช้สำหรับ: PostgreSQL Database + Authentication
  - **จำเป็น**: ✅ (หลัก)
  - **ข้อมูลที่ต้องเก็บ**:
    - `SUPABASE_URL`
    - `SUPABASE_ANON_KEY`
    - `SUPABASE_SERVICE_KEY`

- [ ] **Upstash Redis**
  - สมัครที่: https://console.upstash.com
  - แผน: Pay-as-you-go (เริ่มต้น $10/month)
  - ใช้สำหรับ: Session cache, rate limiting
  - **จำเป็น**: ✅ (หลัก)
  - **ข้อมูลที่ต้องเก็บ**:
    - `REDIS_URL`

- [ ] **AWS Account**
  - สมัครที่: https://aws.amazon.com
  - ใช้สำหรับ: S3 (file storage), ECS (sandbox containers)
  - **จำเป็น**: ✅ (หลัก)
  - **ข้อมูลที่ต้องเก็บ**:
    - `AWS_ACCESS_KEY_ID`
    - `AWS_SECRET_ACCESS_KEY`
    - `AWS_REGION`
    - `S3_BUCKET`

### Hosting & Deployment

- [ ] **Vercel Account**
  - สมัครที่: https://vercel.com
  - แผน: Pro ($20/month) หรือ Hobby (Free)
  - ใช้สำหรับ: Frontend hosting (Next.js)
  - **จำเป็น**: ✅ (หลัก)

- [ ] **Railway Account** (หรือ Fly.io)
  - Railway: https://railway.app
  - Fly.io: https://fly.io
  - แผน: $20-50/month
  - ใช้สำหรับ: Backend API hosting (FastAPI)
  - **จำเป็น**: ✅ (เลือก 1 ใน 2)

- [ ] **Cloudflare Account**
  - สมัครที่: https://cloudflare.com
  - แผน: Pro ($20/month) หรือ Free
  - ใช้สำหรับ: CDN, DDoS protection, DNS
  - **จำเป็น**: ✅ (หลัก)

### Monitoring & Email

- [ ] **Sentry Account**
  - สมัครที่: https://sentry.io
  - แผน: Team ($26/month) หรือ Developer (Free)
  - ใช้สำหรับ: Error tracking, monitoring
  - **จำเป็น**: ✅ (แนะนำสูง)
  - **ข้อมูลที่ต้องเก็บ**:
    - `SENTRY_DSN`

- [ ] **SendGrid Account**
  - สมัครที่: https://sendgrid.com
  - แผน: Essentials ($15/month) หรือ Free (100 emails/day)
  - ใช้สำหรับ: Transactional emails
  - **จำเป็น**: ✅ (แนะนำสูง)
  - **ข้อมูลที่ต้องเก็บ**:
    - `SENDGRID_API_KEY`

## 🌐 2. Domain & DNS

- [ ] **Domain Name**
  - ซื้อที่: Namecheap, Google Domains, Cloudflare
  - แนะนำ: `mrdark.app` หรือชื่ออื่นที่ต้องการ
  - ราคา: ~$10-15/year
  - **จำเป็น**: ✅ (หลัก)

- [ ] **DNS Configuration**
  - ตั้งค่า nameservers ไปที่ Cloudflare
  - เพิ่ม DNS records:
    - `A` record: `mrdark.app` → Vercel
    - `CNAME`: `www.mrdark.app` → `mrdark.app`
    - `CNAME`: `api.mrdark.app` → Railway/Fly.io
  - **จำเป็น**: ✅ (หลัก)

## 🔐 3. Security & Encryption

- [ ] **Encryption Master Key**
  - สร้าง random key สำหรับ encrypt API keys
  - วิธีสร้าง: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
  - **จำเป็น**: ✅ (หลัก)
  - **ข้อมูลที่ต้องเก็บ**:
    - `ENCRYPTION_MASTER_KEY`

- [ ] **JWT Secret**
  - สร้าง random secret สำหรับ JWT tokens
  - วิธีสร้าง: `openssl rand -hex 32`
  - **จำเป็น**: ✅ (หลัก)
  - **ข้อมูลที่ต้องเก็บ**:
    - `JWT_SECRET`

## 💻 4. Development Tools

### Required Software

- [ ] **Node.js 20+**
  - ดาวน์โหลด: https://nodejs.org
  - **จำเป็น**: ✅

- [ ] **Python 3.11+**
  - ดาวน์โหลด: https://python.org
  - **จำเป็น**: ✅

- [ ] **Docker Desktop**
  - ดาวน์โหลด: https://docker.com
  - **จำเป็น**: ✅ (สำหรับ sandbox)

- [ ] **Git**
  - ดาวน์โหลด: https://git-scm.com
  - **จำเป็น**: ✅

- [ ] **pnpm**
  - ติดตั้ง: `npm install -g pnpm`
  - **จำเป็น**: ✅

### Recommended Tools

- [ ] **VS Code** (หรือ editor อื่นที่ถนัด)
- [ ] **Postman** (สำหรับ test API)
- [ ] **TablePlus** (สำหรับดู database)
- [ ] **Redis Insight** (สำหรับดู Redis)

## 📦 5. GitHub Setup

- [ ] **GitHub Repository**
  - Repository: `projectmrdark/mrdark` (✅ สร้างแล้ว)
  - เอกสารวางแผน: ✅ อัพโหลดแล้ว

- [ ] **GitHub Secrets** (สำหรับ CI/CD)
  - `VERCEL_TOKEN`
  - `VERCEL_ORG_ID`
  - `VERCEL_PROJECT_ID`
  - `RAILWAY_TOKEN` (หรือ `FLY_API_TOKEN`)

## 💰 6. Budget Planning

### Monthly Costs (Estimated)

| Service | Cost | Priority |
|---------|------|----------|
| Vercel Pro | $20 | ✅ Required |
| Railway/Fly.io | $20-50 | ✅ Required |
| Supabase Pro | $25 | ✅ Required |
| Upstash Redis | $10 | ✅ Required |
| AWS (S3 + ECS) | $100-300 | ✅ Required |
| Cloudflare Pro | $20 | ✅ Required |
| Sentry Team | $26 | ⚠️ Recommended |
| SendGrid | $15 | ⚠️ Recommended |
| Domain | $1-2 | ✅ Required |
| **Total** | **$237-469** | |

### AI API Costs (Variable)

- OpenAI: Pay-as-you-go (~$50-200/month ขึ้นกับ usage)
- Anthropic: Pay-as-you-go (~$30-100/month)
- Google AI: Free tier available

**Total Estimated**: $320-770/month (ขึ้นกับ traffic และ AI usage)

## 📋 7. Pre-Development Checklist

### Environment Setup

- [ ] ติดตั้ง Node.js, Python, Docker, Git
- [ ] Clone repository: `gh repo clone projectmrdark/mrdark`
- [ ] อ่านเอกสารทั้งหมดใน repository
- [ ] เตรียม API keys ทั้งหมด
- [ ] สร้าง `.env` files สำหรับ frontend และ backend

### Account Setup

- [ ] สร้าง Supabase project
- [ ] สร้าง Upstash Redis database
- [ ] สร้าง AWS S3 bucket
- [ ] สร้าง Vercel project
- [ ] สร้าง Railway/Fly.io project
- [ ] เพิ่ม domain เข้า Cloudflare
- [ ] สร้าง Sentry projects (frontend + backend)
- [ ] สร้าง SendGrid account

### Configuration

- [ ] ตั้งค่า DNS records
- [ ] ตั้งค่า SSL certificates (auto via Cloudflare)
- [ ] ตั้งค่า environment variables ทุก platform
- [ ] ตั้งค่า GitHub secrets สำหรับ CI/CD

## 🚀 8. Ready to Start?

เมื่อเตรียมทุกอย่างเรียบร้อยแล้ว:

1. ✅ อ่าน `README.md` ใน repository
2. ✅ เริ่มจาก `07-development-flow.md`
3. ✅ ทำตาม Phase 1: Project Setup
4. ✅ ดำเนินการต่อเนื่องตาม Development Flow

## 📞 9. Support

หากมีปัญหาหรือข้อสงสัย:
- ตรวจสอบเอกสารใน repository
- ดู troubleshooting ในแต่ละ document
- ถามใน GitHub Discussions

---

## ✅ Quick Start Commands

```bash
# 1. Clone repository
gh repo clone projectmrdark/mrdark
cd mrdark

# 2. Setup frontend
cd frontend
pnpm install
cp .env.example .env.local
# แก้ไข .env.local ใส่ API keys

# 3. Setup backend
cd ../backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# แก้ไข .env ใส่ API keys

# 4. Setup database
cd ../
supabase init
supabase link --project-ref <your-project-ref>
supabase db push

# 5. Run development servers
# Terminal 1 (Frontend)
cd frontend && pnpm dev

# Terminal 2 (Backend)
cd backend && python main.py

# 6. Open browser
# http://localhost:3000
```

---

**Status**: ✅ เอกสารครบถ้วน - พร้อมเริ่มพัฒนา  
**Last Updated**: 2024-01-XX

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import sentry_sdk

# Load environment variables
load_dotenv()

# Initialize Sentry (if DSN is provided)
sentry_dsn = os.getenv('SENTRY_DSN')
if sentry_dsn:
    sentry_sdk.init(dsn=sentry_dsn)

app = FastAPI(
    title="Mr.Dark AI Agent Platform API",
    version="1.0.0",
    description="Backend API for Mr.Dark AI Agent Platform"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from api.chat import router as chat_router
app.include_router(chat_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Mr.Dark AI Agent Platform API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Mr.Dark Backend API"
    }

@app.get("/api/config")
async def get_config():
    """Get API configuration (for testing)"""
    return {
        "vc_api_configured": bool(os.getenv('VC_API_KEY')),
        "vc_base_url": os.getenv('VC_API_BASE_URL'),
        "vc_default_model": os.getenv('VC_DEFAULT_MODEL'),
        "supabase_configured": bool(os.getenv('SUPABASE_URL')),
        "redis_configured": bool(os.getenv('REDIS_URL'))
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

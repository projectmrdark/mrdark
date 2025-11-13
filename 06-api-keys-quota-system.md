# Mr.Dark AI Agent Platform - API Keys Management & Quota System

## 1. API Keys Management Overview

### 1.1 Key Types

**Admin Keys (Platform-owned):**
- Multiple keys from different providers
- Shared across all free-tier users
- Rotated automatically to maximize usage
- Monitored for rate limits and costs

**User Keys (User-provided):**
- User's own API keys
- Encrypted and stored securely
- Used exclusively for that user
- No quota limits when using own keys

### 1.2 Key Priority Logic

```
User sends message
    ↓
Check if user has own API key for selected model
    ↓
    ├─ Yes → Use user's key (no quota deduction)
    │
    └─ No → Use admin key pool
           ↓
           Check user's quota
           ↓
           ├─ Quota available → Select best admin key
           │                    ↓
           │                    Deduct from quota
           │
           └─ Quota exceeded → Block request
                               ↓
                               Prompt: Add own key OR Upgrade
```

## 2. API Key Storage & Security

### 2.1 Encryption

```python
# security/encryption.py

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import os
import base64

class APIKeyEncryption:
    """Encrypt/decrypt API keys"""
    
    def __init__(self):
        # Get encryption key from environment
        # In production, use AWS KMS or similar
        self.master_key = os.getenv('ENCRYPTION_MASTER_KEY')
        if not self.master_key:
            raise ValueError("ENCRYPTION_MASTER_KEY not set")
        
        # Derive encryption key
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'mrdark_salt_v1',  # In production, use random salt per key
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(
            kdf.derive(self.master_key.encode())
        )
        self.cipher = Fernet(key)
    
    def encrypt(self, api_key: str) -> str:
        """Encrypt API key"""
        encrypted = self.cipher.encrypt(api_key.encode())
        return encrypted.decode()
    
    def decrypt(self, encrypted_key: str) -> str:
        """Decrypt API key"""
        decrypted = self.cipher.decrypt(encrypted_key.encode())
        return decrypted.decode()
    
    def hash_key(self, api_key: str) -> str:
        """Create hash for lookup (non-reversible)"""
        import hashlib
        return hashlib.sha256(api_key.encode()).hexdigest()

encryption = APIKeyEncryption()
```

### 2.2 Key Storage

```python
# services/api_key_service.py

from models import ApiKey
from security.encryption import encryption

class APIKeyService:
    """Manage API keys"""
    
    async def add_user_key(
        self,
        user_id: str,
        provider: str,
        api_key: str,
        key_name: str = None
    ) -> ApiKey:
        """Add user's API key"""
        
        # Validate key first
        is_valid = await self.validate_key(provider, api_key)
        if not is_valid:
            raise ValueError("Invalid API key")
        
        # Encrypt key
        encrypted_key = encryption.encrypt(api_key)
        key_hash = encryption.hash_key(api_key)
        
        # Store in database
        db_key = await db.api_keys.create({
            'user_id': user_id,
            'provider': provider,
            'key_name': key_name or f"{provider} Key",
            'key_encrypted': encrypted_key,
            'key_hash': key_hash,
            'is_admin_key': False,
            'is_active': True,
            'is_valid': True
        })
        
        return db_key
    
    async def get_user_key(
        self,
        user_id: str,
        provider: str
    ) -> Optional[str]:
        """Get user's decrypted API key"""
        
        # Find key in database
        db_key = await db.api_keys.find_one({
            'user_id': user_id,
            'provider': provider,
            'is_active': True,
            'is_valid': True,
            'deleted_at': None
        })
        
        if not db_key:
            return None
        
        # Decrypt and return
        return encryption.decrypt(db_key.key_encrypted)
    
    async def validate_key(
        self,
        provider: str,
        api_key: str
    ) -> bool:
        """Validate API key by making test request"""
        
        try:
            if provider == 'openai':
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                # Test with minimal request
                client.models.list()
                return True
            
            elif provider == 'anthropic':
                from anthropic import Anthropic
                client = Anthropic(api_key=api_key)
                # Test request
                client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1,
                    messages=[{"role": "user", "content": "test"}]
                )
                return True
            
            elif provider == 'google':
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                # Test request
                model = genai.GenerativeModel('gemini-pro')
                model.generate_content("test")
                return True
            
            else:
                return False
        
        except Exception as e:
            print(f"Key validation failed: {e}")
            return False
    
    async def delete_user_key(
        self,
        user_id: str,
        key_id: str
    ):
        """Delete user's API key"""
        
        await db.api_keys.update(
            {'id': key_id, 'user_id': user_id},
            {'deleted_at': datetime.utcnow()}
        )
    
    async def list_user_keys(self, user_id: str) -> List[ApiKey]:
        """List user's API keys (without decrypting)"""
        
        keys = await db.api_keys.find({
            'user_id': user_id,
            'deleted_at': None
        })
        
        # Return without encrypted key
        return [
            {
                'id': key.id,
                'provider': key.provider,
                'key_name': key.key_name,
                'is_active': key.is_active,
                'is_valid': key.is_valid,
                'total_requests': key.total_requests,
                'total_tokens': key.total_tokens,
                'last_used_at': key.last_used_at,
                'created_at': key.created_at
            }
            for key in keys
        ]
```

## 3. Admin Key Pool Management

### 3.1 Key Pool Architecture

```python
# services/key_pool_service.py

import asyncio
from typing import Optional
from datetime import datetime, timedelta

class APIKeyPool:
    """Manage pool of admin API keys"""
    
    def __init__(self):
        self.keys_by_provider = {}
        self.lock = asyncio.Lock()
    
    async def initialize(self):
        """Load admin keys from database"""
        
        admin_keys = await db.api_keys.find({
            'is_admin_key': True,
            'is_active': True,
            'is_valid': True,
            'deleted_at': None
        })
        
        for key in admin_keys:
            if key.provider not in self.keys_by_provider:
                self.keys_by_provider[key.provider] = []
            
            self.keys_by_provider[key.provider].append({
                'id': key.id,
                'key': encryption.decrypt(key.key_encrypted),
                'total_requests': key.total_requests,
                'total_tokens': key.total_tokens,
                'current_rpm': key.current_rpm,
                'current_tpm': key.current_tpm,
                'rate_limit_rpm': key.rate_limit_rpm,
                'rate_limit_tpm': key.rate_limit_tpm,
                'rate_limit_reset_at': key.rate_limit_reset_at,
                'last_used_at': key.last_used_at
            })
    
    async def get_best_key(
        self,
        provider: str,
        estimated_tokens: int = 1000
    ) -> Optional[Dict]:
        """Get best available key from pool"""
        
        async with self.lock:
            if provider not in self.keys_by_provider:
                return None
            
            keys = self.keys_by_provider[provider]
            
            # Filter out rate-limited keys
            available_keys = [
                key for key in keys
                if self._is_key_available(key, estimated_tokens)
            ]
            
            if not available_keys:
                # All keys rate-limited, wait for reset
                return None
            
            # Select key with lowest usage
            best_key = min(
                available_keys,
                key=lambda k: k['total_requests']
            )
            
            return best_key
    
    def _is_key_available(
        self,
        key: Dict,
        estimated_tokens: int
    ) -> bool:
        """Check if key is available (not rate-limited)"""
        
        now = datetime.utcnow()
        
        # Check if rate limit reset time has passed
        if key['rate_limit_reset_at']:
            if key['rate_limit_reset_at'] > now:
                # Still rate-limited
                return False
            else:
                # Reset counters
                key['current_rpm'] = 0
                key['current_tpm'] = 0
                key['rate_limit_reset_at'] = None
        
        # Check RPM limit
        if key['rate_limit_rpm']:
            if key['current_rpm'] >= key['rate_limit_rpm']:
                return False
        
        # Check TPM limit
        if key['rate_limit_tpm']:
            if key['current_tpm'] + estimated_tokens > key['rate_limit_tpm']:
                return False
        
        return True
    
    async def record_usage(
        self,
        key_id: str,
        tokens: int,
        success: bool = True
    ):
        """Record key usage"""
        
        # Update in-memory counters
        for provider, keys in self.keys_by_provider.items():
            for key in keys:
                if key['id'] == key_id:
                    key['total_requests'] += 1
                    key['total_tokens'] += tokens
                    key['current_rpm'] += 1
                    key['current_tpm'] += tokens
                    key['last_used_at'] = datetime.utcnow()
                    
                    # Set rate limit reset time (1 minute from now)
                    if not key['rate_limit_reset_at']:
                        key['rate_limit_reset_at'] = (
                            datetime.utcnow() + timedelta(minutes=1)
                        )
        
        # Update database
        await db.api_keys.update(
            {'id': key_id},
            {
                '$inc': {
                    'total_requests': 1,
                    'total_tokens': tokens,
                    'current_rpm': 1,
                    'current_tpm': tokens
                },
                'last_used_at': datetime.utcnow()
            }
        )
    
    async def handle_rate_limit(
        self,
        key_id: str,
        reset_after: int = 60
    ):
        """Handle rate limit error"""
        
        # Mark key as rate-limited
        reset_at = datetime.utcnow() + timedelta(seconds=reset_after)
        
        # Update in-memory
        for provider, keys in self.keys_by_provider.items():
            for key in keys:
                if key['id'] == key_id:
                    key['rate_limit_reset_at'] = reset_at
        
        # Update database
        await db.api_keys.update(
            {'id': key_id},
            {'rate_limit_reset_at': reset_at}
        )

key_pool = APIKeyPool()
```

### 3.2 Key Rotation Strategy

```python
# services/key_rotation.py

class KeyRotationStrategy:
    """Smart key rotation to maximize usage"""
    
    @staticmethod
    async def select_key(
        provider: str,
        user_id: str,
        estimated_tokens: int
    ) -> Tuple[str, bool]:
        """
        Select best API key for request
        
        Returns:
            (api_key, is_user_key)
        """
        
        # 1. Try user's own key first
        user_key = await api_key_service.get_user_key(user_id, provider)
        if user_key:
            return (user_key, True)
        
        # 2. Check user's quota
        user = await db.users.find_one({'id': user_id})
        if user.quota_used_current_month + estimated_tokens > user.quota_tokens_monthly:
            raise QuotaExceededError("Monthly quota exceeded")
        
        # 3. Get best admin key from pool
        key_info = await key_pool.get_best_key(provider, estimated_tokens)
        if not key_info:
            # All keys rate-limited, try fallback provider
            fallback = self._get_fallback_provider(provider)
            if fallback:
                key_info = await key_pool.get_best_key(fallback, estimated_tokens)
        
        if not key_info:
            raise RateLimitError("All API keys are rate-limited. Please try again later.")
        
        return (key_info['key'], False)
    
    @staticmethod
    def _get_fallback_provider(provider: str) -> Optional[str]:
        """Get fallback provider"""
        fallbacks = {
            'openai': 'anthropic',
            'anthropic': 'google',
            'google': 'openai'
        }
        return fallbacks.get(provider)
```

## 4. Quota System

### 4.1 Quota Tiers

```python
# config/quota_tiers.py

QUOTA_TIERS = {
    'free': {
        'tokens_monthly': 1_000_000,  # 1M tokens
        'price_usd': 0,
        'features': [
            'Basic AI models',
            'Sandbox execution',
            'File uploads (10MB max)',
            'Community support'
        ]
    },
    'pro': {
        'tokens_monthly': 10_000_000,  # 10M tokens
        'price_usd': 20,
        'features': [
            'All AI models',
            'Priority execution',
            'File uploads (100MB max)',
            'Email support',
            'Custom API keys',
            'Export conversations'
        ]
    },
    'enterprise': {
        'tokens_monthly': 100_000_000,  # 100M tokens
        'price_usd': 200,
        'features': [
            'Unlimited AI models',
            'Dedicated resources',
            'File uploads (1GB max)',
            'Priority support',
            'SSO integration',
            'Team management',
            'Custom deployment',
            'SLA guarantee'
        ]
    }
}
```

### 4.2 Quota Tracking

```python
# services/quota_service.py

class QuotaService:
    """Manage user quotas"""
    
    async def check_quota(
        self,
        user_id: str,
        estimated_tokens: int
    ) -> bool:
        """Check if user has enough quota"""
        
        user = await db.users.find_one({'id': user_id})
        
        # Check if quota needs reset
        if user.quota_reset_date and user.quota_reset_date < datetime.utcnow():
            await self.reset_quota(user_id)
            user = await db.users.find_one({'id': user_id})
        
        # Check quota
        remaining = user.quota_tokens_monthly - user.quota_used_current_month
        return remaining >= estimated_tokens
    
    async def deduct_quota(
        self,
        user_id: str,
        tokens: int
    ):
        """Deduct tokens from user's quota"""
        
        # Update user quota
        await db.users.update(
            {'id': user_id},
            {
                '$inc': {'quota_used_current_month': tokens},
                'updated_at': datetime.utcnow()
            }
        )
        
        # Log usage
        await db.usage_logs.create({
            'user_id': user_id,
            'tokens_total': tokens,
            'created_at': datetime.utcnow()
        })
    
    async def reset_quota(self, user_id: str):
        """Reset user's monthly quota"""
        
        await db.users.update(
            {'id': user_id},
            {
                'quota_used_current_month': 0,
                'quota_reset_date': datetime.utcnow() + timedelta(days=30),
                'updated_at': datetime.utcnow()
            }
        )
    
    async def get_quota_status(self, user_id: str) -> Dict:
        """Get user's quota status"""
        
        user = await db.users.find_one({'id': user_id})
        
        # Check if needs reset
        if user.quota_reset_date and user.quota_reset_date < datetime.utcnow():
            await self.reset_quota(user_id)
            user = await db.users.find_one({'id': user_id})
        
        used = user.quota_used_current_month
        total = user.quota_tokens_monthly
        remaining = total - used
        percentage = (used / total * 100) if total > 0 else 0
        
        return {
            'used': used,
            'total': total,
            'remaining': remaining,
            'percentage': percentage,
            'reset_date': user.quota_reset_date,
            'tier': user.subscription_tier
        }
    
    async def upgrade_tier(
        self,
        user_id: str,
        new_tier: str
    ):
        """Upgrade user's subscription tier"""
        
        if new_tier not in QUOTA_TIERS:
            raise ValueError(f"Invalid tier: {new_tier}")
        
        tier_config = QUOTA_TIERS[new_tier]
        
        await db.users.update(
            {'id': user_id},
            {
                'subscription_tier': new_tier,
                'quota_tokens_monthly': tier_config['tokens_monthly'],
                'subscription_status': 'active',
                'subscription_expires_at': datetime.utcnow() + timedelta(days=30),
                'updated_at': datetime.utcnow()
            }
        )

quota_service = QuotaService()
```

### 4.3 Quota Enforcement

```python
# middleware/quota_middleware.py

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class QuotaMiddleware(BaseHTTPMiddleware):
    """Enforce quota limits on API requests"""
    
    async def dispatch(self, request: Request, call_next):
        # Skip quota check for certain endpoints
        if request.url.path in ['/health', '/auth/login', '/auth/signup']:
            return await call_next(request)
        
        # Get user from request
        user = request.state.user if hasattr(request.state, 'user') else None
        if not user:
            return await call_next(request)
        
        # Estimate tokens for request
        estimated_tokens = self.estimate_tokens(request)
        
        # Check quota
        has_quota = await quota_service.check_quota(
            user.id,
            estimated_tokens
        )
        
        if not has_quota:
            raise HTTPException(
                status_code=429,
                detail={
                    'error': 'quota_exceeded',
                    'message': 'Monthly quota exceeded',
                    'quota_status': await quota_service.get_quota_status(user.id)
                }
            )
        
        # Process request
        response = await call_next(request)
        
        return response
    
    def estimate_tokens(self, request: Request) -> int:
        """Estimate tokens for request"""
        
        # Simple estimation based on endpoint
        if '/chat' in request.url.path:
            # Assume average chat uses 2000 tokens
            return 2000
        elif '/generate' in request.url.path:
            # Image generation equivalent
            return 5000
        else:
            return 1000
```

## 5. Cost Tracking

### 5.1 Token Pricing

```python
# config/pricing.py

# Pricing in USD per 1M tokens
TOKEN_PRICING = {
    'openai': {
        'gpt-4': {
            'prompt': 30.00,
            'completion': 60.00
        },
        'gpt-4-turbo': {
            'prompt': 10.00,
            'completion': 30.00
        },
        'gpt-3.5-turbo': {
            'prompt': 0.50,
            'completion': 1.50
        }
    },
    'anthropic': {
        'claude-3-opus': {
            'prompt': 15.00,
            'completion': 75.00
        },
        'claude-3-sonnet': {
            'prompt': 3.00,
            'completion': 15.00
        },
        'claude-3-haiku': {
            'prompt': 0.25,
            'completion': 1.25
        }
    },
    'google': {
        'gemini-pro': {
            'prompt': 0.50,
            'completion': 1.50
        },
        'gemini-ultra': {
            'prompt': 10.00,
            'completion': 30.00
        }
    }
}

def calculate_cost(
    model: str,
    provider: str,
    tokens_prompt: int,
    tokens_completion: int
) -> float:
    """Calculate cost in USD cents"""
    
    pricing = TOKEN_PRICING.get(provider, {}).get(model)
    if not pricing:
        return 0
    
    cost_prompt = (tokens_prompt / 1_000_000) * pricing['prompt']
    cost_completion = (tokens_completion / 1_000_000) * pricing['completion']
    
    # Return in cents
    return int((cost_prompt + cost_completion) * 100)
```

### 5.2 Cost Monitoring

```python
# services/cost_monitoring.py

class CostMonitoringService:
    """Monitor and alert on costs"""
    
    async def record_cost(
        self,
        user_id: str,
        model: str,
        provider: str,
        tokens_prompt: int,
        tokens_completion: int
    ):
        """Record cost for request"""
        
        cost_cents = calculate_cost(
            model,
            provider,
            tokens_prompt,
            tokens_completion
        )
        
        # Save to usage logs
        await db.usage_logs.create({
            'user_id': user_id,
            'model': model,
            'provider': provider,
            'tokens_prompt': tokens_prompt,
            'tokens_completion': tokens_completion,
            'tokens_total': tokens_prompt + tokens_completion,
            'cost_prompt': int((tokens_prompt / 1_000_000) * TOKEN_PRICING[provider][model]['prompt'] * 100),
            'cost_completion': int((tokens_completion / 1_000_000) * TOKEN_PRICING[provider][model]['completion'] * 100),
            'cost_total': cost_cents,
            'created_at': datetime.utcnow()
        })
    
    async def get_daily_cost(self, date: datetime = None) -> float:
        """Get total cost for a day"""
        
        if not date:
            date = datetime.utcnow()
        
        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        
        result = await db.usage_logs.aggregate([
            {
                '$match': {
                    'created_at': {'$gte': start, '$lt': end}
                }
            },
            {
                '$group': {
                    '_id': None,
                    'total_cost': {'$sum': '$cost_total'}
                }
            }
        ])
        
        if result:
            return result[0]['total_cost'] / 100  # Convert cents to dollars
        return 0.0
    
    async def check_budget_alert(self):
        """Check if daily budget exceeded"""
        
        daily_budget = 1000  # $1000 per day
        current_cost = await self.get_daily_cost()
        
        if current_cost > daily_budget:
            # Send alert
            await send_admin_alert(
                f"Daily budget exceeded: ${current_cost:.2f} / ${daily_budget}"
            )
            
            # Optionally pause free tier
            # await self.pause_free_tier()
    
    async def get_user_cost_breakdown(
        self,
        user_id: str,
        days: int = 30
    ) -> Dict:
        """Get user's cost breakdown"""
        
        start = datetime.utcnow() - timedelta(days=days)
        
        result = await db.usage_logs.aggregate([
            {
                '$match': {
                    'user_id': user_id,
                    'created_at': {'$gte': start}
                }
            },
            {
                '$group': {
                    '_id': '$model',
                    'total_tokens': {'$sum': '$tokens_total'},
                    'total_cost': {'$sum': '$cost_total'},
                    'request_count': {'$sum': 1}
                }
            }
        ])
        
        return {
            'breakdown': [
                {
                    'model': r['_id'],
                    'tokens': r['total_tokens'],
                    'cost_usd': r['total_cost'] / 100,
                    'requests': r['request_count']
                }
                for r in result
            ],
            'total_cost_usd': sum(r['total_cost'] for r in result) / 100,
            'total_tokens': sum(r['total_tokens'] for r in result)
        }

cost_monitoring = CostMonitoringService()
```

## 6. Quota Warning System

### 6.1 Warning Thresholds

```python
# services/quota_warnings.py

class QuotaWarningService:
    """Send warnings when quota is running low"""
    
    WARNING_THRESHOLDS = [0.50, 0.80, 0.90, 0.95, 1.00]  # 50%, 80%, 90%, 95%, 100%
    
    async def check_and_warn(self, user_id: str):
        """Check quota and send warnings if needed"""
        
        status = await quota_service.get_quota_status(user_id)
        percentage = status['percentage'] / 100
        
        # Check which threshold crossed
        for threshold in self.WARNING_THRESHOLDS:
            if percentage >= threshold:
                # Check if already warned for this threshold
                already_warned = await self._check_if_warned(
                    user_id,
                    threshold
                )
                
                if not already_warned:
                    await self._send_warning(user_id, threshold, status)
                    await self._mark_as_warned(user_id, threshold)
    
    async def _send_warning(
        self,
        user_id: str,
        threshold: float,
        status: Dict
    ):
        """Send warning notification"""
        
        user = await db.users.find_one({'id': user_id})
        
        if threshold < 1.0:
            # Warning
            message = f"""
            ⚠️ Quota Warning
            
            You've used {status['percentage']:.1f}% of your monthly quota.
            
            Used: {status['used']:,} tokens
            Remaining: {status['remaining']:,} tokens
            Resets: {status['reset_date'].strftime('%Y-%m-%d')}
            
            Consider:
            - Adding your own API key (no quota limits)
            - Upgrading to Pro ($20/month for 10M tokens)
            """
        else:
            # Quota exceeded
            message = f"""
            🚫 Quota Exceeded
            
            You've used all your monthly quota.
            
            To continue using Mr.Dark:
            1. Add your own API key (Settings → API Keys)
            2. Upgrade to Pro ($20/month for 10M tokens)
            
            Your quota will reset on {status['reset_date'].strftime('%Y-%m-%d')}
            """
        
        # Send email
        await send_email(
            to=user.email,
            subject=f"Mr.Dark Quota {'Exceeded' if threshold >= 1.0 else 'Warning'}",
            body=message
        )
        
        # Send in-app notification
        await send_notification(
            user_id=user_id,
            type='quota_warning',
            message=message,
            threshold=threshold
        )
    
    async def _check_if_warned(
        self,
        user_id: str,
        threshold: float
    ) -> bool:
        """Check if user already warned for this threshold this month"""
        
        # Check in database or cache
        key = f"quota_warning:{user_id}:{threshold}"
        return await redis.exists(key)
    
    async def _mark_as_warned(
        self,
        user_id: str,
        threshold: float
    ):
        """Mark user as warned"""
        
        key = f"quota_warning:{user_id}:{threshold}"
        # Expire after 31 days
        await redis.setex(key, 31 * 24 * 3600, "1")

quota_warnings = QuotaWarningService()
```

## 7. API Endpoints

### 7.1 API Key Management Endpoints

```python
# api/api_keys.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/users/api-keys")

class AddAPIKeyRequest(BaseModel):
    provider: str
    api_key: str
    key_name: str = None

class APIKeyResponse(BaseModel):
    id: str
    provider: str
    key_name: str
    is_active: bool
    is_valid: bool
    total_requests: int
    total_tokens: int
    last_used_at: datetime = None
    created_at: datetime

@router.post("/", response_model=APIKeyResponse)
async def add_api_key(
    request: AddAPIKeyRequest,
    user: User = Depends(get_current_user)
):
    """Add user's API key"""
    
    try:
        key = await api_key_service.add_user_key(
            user_id=user.id,
            provider=request.provider,
            api_key=request.api_key,
            key_name=request.key_name
        )
        
        return key
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[APIKeyResponse])
async def list_api_keys(user: User = Depends(get_current_user)):
    """List user's API keys"""
    
    keys = await api_key_service.list_user_keys(user.id)
    return keys

@router.delete("/{key_id}")
async def delete_api_key(
    key_id: str,
    user: User = Depends(get_current_user)
):
    """Delete API key"""
    
    await api_key_service.delete_user_key(user.id, key_id)
    return {"success": True}

@router.post("/{key_id}/test")
async def test_api_key(
    key_id: str,
    user: User = Depends(get_current_user)
):
    """Test if API key is valid"""
    
    key = await db.api_keys.find_one({'id': key_id, 'user_id': user.id})
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")
    
    api_key = encryption.decrypt(key.key_encrypted)
    is_valid = await api_key_service.validate_key(key.provider, api_key)
    
    # Update validity in database
    await db.api_keys.update(
        {'id': key_id},
        {'is_valid': is_valid}
    )
    
    return {"valid": is_valid}
```

### 7.2 Quota Endpoints

```python
# api/quota.py

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/users/quota")

@router.get("/")
async def get_quota_status(user: User = Depends(get_current_user)):
    """Get user's quota status"""
    
    status = await quota_service.get_quota_status(user.id)
    return status

@router.get("/usage")
async def get_usage_history(
    days: int = 30,
    user: User = Depends(get_current_user)
):
    """Get usage history"""
    
    start = datetime.utcnow() - timedelta(days=days)
    
    logs = await db.usage_logs.find({
        'user_id': user.id,
        'created_at': {'$gte': start}
    }).sort('created_at', -1).to_list(length=1000)
    
    return {
        'logs': logs,
        'summary': {
            'total_tokens': sum(log.tokens_total for log in logs),
            'total_requests': len(logs),
            'total_cost_usd': sum(log.cost_total for log in logs) / 100
        }
    }

@router.post("/upgrade")
async def upgrade_subscription(
    tier: str,
    user: User = Depends(get_current_user)
):
    """Upgrade subscription tier"""
    
    # In production, integrate with Stripe or similar
    # For now, just update tier
    
    await quota_service.upgrade_tier(user.id, tier)
    
    return {
        'success': True,
        'new_tier': tier,
        'quota': QUOTA_TIERS[tier]['tokens_monthly']
    }
```

---

**Document Version**: 1.0  
**Last Updated**: 2024-01-XX  
**Status**: Draft - Pending Review

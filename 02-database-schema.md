# Mr.Dark AI Agent Platform - Database Schema & Data Models

## 1. Database Overview

### 1.1 Database Technology
- **Primary Database**: PostgreSQL 15+ (via Supabase)
- **Extensions**: 
  - `uuid-ossp` - UUID generation
  - `pgcrypto` - Encryption functions
  - `pg_trgm` - Text search
  - `pgvector` - Vector similarity (for future RAG)
- **Caching Layer**: Redis 7+
- **File Storage**: Supabase Storage (S3-compatible)

### 1.2 Design Principles
1. **Normalization**: 3NF for data integrity
2. **Indexing**: Strategic indexes for performance
3. **Soft Deletes**: Retain data for audit/recovery
4. **Timestamps**: Track creation and modification
5. **UUID**: Use UUIDs for primary keys (security)
6. **Encryption**: Sensitive data encrypted at rest
7. **Audit Trail**: Track all important changes

## 2. Core Tables

### 2.1 Users Table

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(50) UNIQUE,
  full_name VARCHAR(255),
  avatar_url TEXT,
  
  -- Authentication (managed by Supabase Auth)
  auth_id UUID UNIQUE NOT NULL, -- Links to auth.users
  
  -- Profile
  bio TEXT,
  website VARCHAR(255),
  location VARCHAR(255),
  
  -- Preferences
  preferences JSONB DEFAULT '{
    "theme": "dark",
    "language": "en",
    "default_model": "gpt-4",
    "default_mode": "sandbox",
    "notifications_enabled": true
  }'::jsonb,
  
  -- Quota & Billing
  quota_tokens_monthly INTEGER DEFAULT 1000000, -- 1M tokens
  quota_used_current_month INTEGER DEFAULT 0,
  quota_reset_date TIMESTAMP WITH TIME ZONE,
  subscription_tier VARCHAR(50) DEFAULT 'free', -- free, pro, enterprise
  subscription_status VARCHAR(50) DEFAULT 'active', -- active, cancelled, expired
  subscription_expires_at TIMESTAMP WITH TIME ZONE,
  
  -- Metadata
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_active_at TIMESTAMP WITH TIME ZONE,
  deleted_at TIMESTAMP WITH TIME ZONE, -- Soft delete
  
  -- Constraints
  CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
  CONSTRAINT valid_subscription_tier CHECK (subscription_tier IN ('free', 'pro', 'enterprise')),
  CONSTRAINT valid_subscription_status CHECK (subscription_status IN ('active', 'cancelled', 'expired', 'trial'))
);

-- Indexes
CREATE INDEX idx_users_auth_id ON users(auth_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_deleted_at ON users(deleted_at) WHERE deleted_at IS NULL;

-- Triggers
CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

### 2.2 Sessions Table

```sql
CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Session Info
  title VARCHAR(255) DEFAULT 'New Chat',
  description TEXT,
  
  -- Configuration
  model VARCHAR(100) NOT NULL, -- gpt-4, claude-3-opus, gemini-pro
  mode VARCHAR(50) NOT NULL, -- sandbox, local
  temperature DECIMAL(3,2) DEFAULT 0.7,
  max_tokens INTEGER,
  
  -- Execution Environment
  sandbox_container_id VARCHAR(255), -- Docker container ID (if sandbox mode)
  sandbox_status VARCHAR(50), -- running, hibernated, stopped
  local_client_id UUID, -- Connected local client (if local mode)
  
  -- State
  context_summary TEXT, -- AI-generated summary of conversation
  total_messages INTEGER DEFAULT 0,
  total_tokens_used INTEGER DEFAULT 0,
  
  -- Metadata
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_message_at TIMESTAMP WITH TIME ZONE,
  archived_at TIMESTAMP WITH TIME ZONE,
  deleted_at TIMESTAMP WITH TIME ZONE,
  
  -- Constraints
  CONSTRAINT valid_model CHECK (model IN ('gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo', 'claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku', 'gemini-pro', 'gemini-ultra')),
  CONSTRAINT valid_mode CHECK (mode IN ('sandbox', 'local')),
  CONSTRAINT valid_temperature CHECK (temperature >= 0 AND temperature <= 2),
  CONSTRAINT valid_sandbox_status CHECK (sandbox_status IN ('running', 'hibernated', 'stopped', 'error'))
);

-- Indexes
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_created_at ON sessions(created_at DESC);
CREATE INDEX idx_sessions_last_message_at ON sessions(last_message_at DESC);
CREATE INDEX idx_sessions_deleted_at ON sessions(deleted_at) WHERE deleted_at IS NULL;
CREATE INDEX idx_sessions_sandbox_status ON sessions(sandbox_status) WHERE sandbox_status = 'running';

-- Triggers
CREATE TRIGGER update_sessions_updated_at
  BEFORE UPDATE ON sessions
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

### 2.3 Messages Table

```sql
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  
  -- Message Info
  role VARCHAR(50) NOT NULL, -- user, assistant, system, tool
  content TEXT,
  content_type VARCHAR(50) DEFAULT 'text', -- text, markdown, code, image, file
  
  -- AI Response Metadata (for assistant messages)
  model VARCHAR(100), -- Which model generated this
  finish_reason VARCHAR(50), -- stop, length, function_call, content_filter
  tokens_prompt INTEGER,
  tokens_completion INTEGER,
  tokens_total INTEGER,
  
  -- Function Calling
  function_calls JSONB, -- Array of function calls made
  tool_results JSONB, -- Array of tool execution results
  
  -- Streaming State
  is_streaming BOOLEAN DEFAULT false,
  stream_completed_at TIMESTAMP WITH TIME ZONE,
  
  -- User Feedback
  user_rating INTEGER, -- 1-5 stars
  user_feedback TEXT,
  
  -- Metadata
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  deleted_at TIMESTAMP WITH TIME ZONE,
  
  -- Constraints
  CONSTRAINT valid_role CHECK (role IN ('user', 'assistant', 'system', 'tool')),
  CONSTRAINT valid_content_type CHECK (content_type IN ('text', 'markdown', 'code', 'image', 'file', 'error')),
  CONSTRAINT valid_finish_reason CHECK (finish_reason IN ('stop', 'length', 'function_call', 'content_filter', 'error')),
  CONSTRAINT valid_user_rating CHECK (user_rating >= 1 AND user_rating <= 5)
);

-- Indexes
CREATE INDEX idx_messages_session_id ON messages(session_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_role ON messages(role);
CREATE INDEX idx_messages_deleted_at ON messages(deleted_at) WHERE deleted_at IS NULL;

-- Triggers
CREATE TRIGGER update_messages_updated_at
  BEFORE UPDATE ON messages
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Trigger to update session stats
CREATE TRIGGER update_session_stats_on_message
  AFTER INSERT ON messages
  FOR EACH ROW
  EXECUTE FUNCTION update_session_message_stats();
```

### 2.4 Files Table

```sql
CREATE TABLE files (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  session_id UUID REFERENCES sessions(id) ON DELETE SET NULL,
  message_id UUID REFERENCES messages(id) ON DELETE SET NULL,
  
  -- File Info
  filename VARCHAR(255) NOT NULL,
  original_filename VARCHAR(255) NOT NULL,
  mime_type VARCHAR(255) NOT NULL,
  size_bytes BIGINT NOT NULL,
  
  -- Storage
  storage_path TEXT NOT NULL, -- Path in Supabase Storage
  storage_bucket VARCHAR(100) DEFAULT 'user-files',
  url TEXT, -- Public URL (if public)
  
  -- File Type Classification
  file_category VARCHAR(50), -- image, document, code, data, archive, other
  is_public BOOLEAN DEFAULT false,
  
  -- Processing Status
  processing_status VARCHAR(50) DEFAULT 'pending', -- pending, processing, completed, failed
  extracted_text TEXT, -- For documents/images (OCR)
  metadata JSONB, -- File-specific metadata (dimensions, duration, etc.)
  
  -- Metadata
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  deleted_at TIMESTAMP WITH TIME ZONE,
  
  -- Constraints
  CONSTRAINT valid_file_category CHECK (file_category IN ('image', 'document', 'code', 'data', 'archive', 'audio', 'video', 'other')),
  CONSTRAINT valid_processing_status CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed'))
);

-- Indexes
CREATE INDEX idx_files_user_id ON files(user_id);
CREATE INDEX idx_files_session_id ON files(session_id);
CREATE INDEX idx_files_message_id ON files(message_id);
CREATE INDEX idx_files_created_at ON files(created_at DESC);
CREATE INDEX idx_files_file_category ON files(file_category);
CREATE INDEX idx_files_deleted_at ON files(deleted_at) WHERE deleted_at IS NULL;

-- Triggers
CREATE TRIGGER update_files_updated_at
  BEFORE UPDATE ON files
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

### 2.5 API Keys Table

```sql
CREATE TABLE api_keys (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE, -- NULL for admin keys
  
  -- Key Info
  provider VARCHAR(50) NOT NULL, -- openai, anthropic, google
  key_name VARCHAR(255), -- User-friendly name
  key_hash VARCHAR(255) NOT NULL UNIQUE, -- Hashed key for lookup
  key_encrypted TEXT NOT NULL, -- Encrypted actual key
  
  -- Key Type
  is_admin_key BOOLEAN DEFAULT false, -- Platform-owned vs user-owned
  
  -- Usage Tracking
  total_requests INTEGER DEFAULT 0,
  total_tokens INTEGER DEFAULT 0,
  last_used_at TIMESTAMP WITH TIME ZONE,
  
  -- Rate Limiting
  rate_limit_rpm INTEGER, -- Requests per minute
  rate_limit_tpm INTEGER, -- Tokens per minute
  current_rpm INTEGER DEFAULT 0,
  current_tpm INTEGER DEFAULT 0,
  rate_limit_reset_at TIMESTAMP WITH TIME ZONE,
  
  -- Status
  is_active BOOLEAN DEFAULT true,
  is_valid BOOLEAN DEFAULT true, -- Set to false if key validation fails
  last_error TEXT,
  last_error_at TIMESTAMP WITH TIME ZONE,
  
  -- Metadata
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  deleted_at TIMESTAMP WITH TIME ZONE,
  
  -- Constraints
  CONSTRAINT valid_provider CHECK (provider IN ('openai', 'anthropic', 'google', 'other'))
);

-- Indexes
CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);
CREATE INDEX idx_api_keys_provider ON api_keys(provider);
CREATE INDEX idx_api_keys_is_admin_key ON api_keys(is_admin_key);
CREATE INDEX idx_api_keys_is_active ON api_keys(is_active) WHERE is_active = true;
CREATE INDEX idx_api_keys_key_hash ON api_keys(key_hash);
CREATE INDEX idx_api_keys_deleted_at ON api_keys(deleted_at) WHERE deleted_at IS NULL;

-- Triggers
CREATE TRIGGER update_api_keys_updated_at
  BEFORE UPDATE ON api_keys
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

### 2.6 Usage Logs Table

```sql
CREATE TABLE usage_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  session_id UUID REFERENCES sessions(id) ON DELETE SET NULL,
  message_id UUID REFERENCES messages(id) ON DELETE SET NULL,
  api_key_id UUID REFERENCES api_keys(id) ON DELETE SET NULL,
  
  -- Usage Info
  model VARCHAR(100) NOT NULL,
  provider VARCHAR(50) NOT NULL,
  
  -- Token Usage
  tokens_prompt INTEGER DEFAULT 0,
  tokens_completion INTEGER DEFAULT 0,
  tokens_total INTEGER DEFAULT 0,
  
  -- Cost (in USD cents)
  cost_prompt INTEGER DEFAULT 0, -- Cost in cents
  cost_completion INTEGER DEFAULT 0,
  cost_total INTEGER DEFAULT 0,
  
  -- Request Info
  request_duration_ms INTEGER,
  response_cached BOOLEAN DEFAULT false,
  
  -- Metadata
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Constraints
  CONSTRAINT valid_provider CHECK (provider IN ('openai', 'anthropic', 'google', 'other'))
);

-- Indexes
CREATE INDEX idx_usage_logs_user_id ON usage_logs(user_id);
CREATE INDEX idx_usage_logs_session_id ON usage_logs(session_id);
CREATE INDEX idx_usage_logs_created_at ON usage_logs(created_at DESC);
CREATE INDEX idx_usage_logs_user_created ON usage_logs(user_id, created_at DESC);

-- Partitioning by month for performance
-- (To be implemented as data grows)
```

### 2.7 Tool Executions Table

```sql
CREATE TABLE tool_executions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  message_id UUID REFERENCES messages(id) ON DELETE SET NULL,
  
  -- Tool Info
  tool_name VARCHAR(100) NOT NULL,
  tool_action VARCHAR(100),
  tool_params JSONB,
  
  -- Execution
  execution_mode VARCHAR(50) NOT NULL, -- sandbox, local
  execution_status VARCHAR(50) NOT NULL, -- pending, running, completed, failed, timeout
  
  -- Results
  result JSONB,
  result_summary TEXT,
  error_message TEXT,
  
  -- Performance
  started_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE,
  duration_ms INTEGER,
  
  -- Artifacts
  artifacts JSONB, -- Array of file IDs or URLs produced
  
  -- Metadata
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Constraints
  CONSTRAINT valid_execution_mode CHECK (execution_mode IN ('sandbox', 'local')),
  CONSTRAINT valid_execution_status CHECK (execution_status IN ('pending', 'running', 'completed', 'failed', 'timeout', 'cancelled'))
);

-- Indexes
CREATE INDEX idx_tool_executions_session_id ON tool_executions(session_id);
CREATE INDEX idx_tool_executions_message_id ON tool_executions(message_id);
CREATE INDEX idx_tool_executions_tool_name ON tool_executions(tool_name);
CREATE INDEX idx_tool_executions_created_at ON tool_executions(created_at DESC);
CREATE INDEX idx_tool_executions_status ON tool_executions(execution_status);
```

### 2.8 Local Clients Table

```sql
CREATE TABLE local_clients (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Client Info
  client_name VARCHAR(255) NOT NULL,
  client_type VARCHAR(50) NOT NULL, -- electron, python-cli, docker
  client_version VARCHAR(50),
  
  -- Authentication
  auth_token_hash VARCHAR(255) NOT NULL UNIQUE,
  auth_token_encrypted TEXT NOT NULL,
  
  -- Connection
  is_connected BOOLEAN DEFAULT false,
  last_connected_at TIMESTAMP WITH TIME ZONE,
  last_disconnected_at TIMESTAMP WITH TIME ZONE,
  connection_count INTEGER DEFAULT 0,
  
  -- Client Capabilities
  capabilities JSONB DEFAULT '{
    "python": true,
    "nodejs": true,
    "browser": true,
    "shell": true
  }'::jsonb,
  
  -- Workspace
  workspace_path TEXT,
  
  -- Metadata
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  deleted_at TIMESTAMP WITH TIME ZONE,
  
  -- Constraints
  CONSTRAINT valid_client_type CHECK (client_type IN ('electron', 'python-cli', 'docker', 'other'))
);

-- Indexes
CREATE INDEX idx_local_clients_user_id ON local_clients(user_id);
CREATE INDEX idx_local_clients_is_connected ON local_clients(is_connected) WHERE is_connected = true;
CREATE INDEX idx_local_clients_auth_token_hash ON local_clients(auth_token_hash);
CREATE INDEX idx_local_clients_deleted_at ON local_clients(deleted_at) WHERE deleted_at IS NULL;

-- Triggers
CREATE TRIGGER update_local_clients_updated_at
  BEFORE UPDATE ON local_clients
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

### 2.9 Sandbox Containers Table

```sql
CREATE TABLE sandbox_containers (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  
  -- Container Info
  container_id VARCHAR(255) UNIQUE NOT NULL, -- Docker container ID
  container_name VARCHAR(255) UNIQUE NOT NULL,
  image_name VARCHAR(255) NOT NULL,
  
  -- Status
  status VARCHAR(50) NOT NULL, -- creating, running, hibernated, stopped, error
  
  -- Resources
  cpu_limit DECIMAL(4,2), -- CPU cores
  memory_limit_mb INTEGER,
  disk_limit_mb INTEGER,
  
  -- Resource Usage (current)
  cpu_usage_percent DECIMAL(5,2),
  memory_usage_mb INTEGER,
  disk_usage_mb INTEGER,
  
  -- Network
  internal_ip VARCHAR(50),
  exposed_ports JSONB, -- Array of port mappings
  
  -- Lifecycle
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  started_at TIMESTAMP WITH TIME ZONE,
  hibernated_at TIMESTAMP WITH TIME ZONE,
  stopped_at TIMESTAMP WITH TIME ZONE,
  last_activity_at TIMESTAMP WITH TIME ZONE,
  
  -- State Persistence
  state_snapshot_url TEXT, -- S3 URL of hibernated state
  
  -- Constraints
  CONSTRAINT valid_status CHECK (status IN ('creating', 'running', 'hibernated', 'stopped', 'error', 'destroying'))
);

-- Indexes
CREATE INDEX idx_sandbox_containers_session_id ON sandbox_containers(session_id);
CREATE INDEX idx_sandbox_containers_container_id ON sandbox_containers(container_id);
CREATE INDEX idx_sandbox_containers_status ON sandbox_containers(status);
CREATE INDEX idx_sandbox_containers_last_activity ON sandbox_containers(last_activity_at);
```

### 2.10 Webhooks Table (Future)

```sql
CREATE TABLE webhooks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Webhook Info
  name VARCHAR(255) NOT NULL,
  url TEXT NOT NULL,
  secret VARCHAR(255), -- For signature verification
  
  -- Events
  events JSONB NOT NULL, -- Array of event types to subscribe to
  
  -- Status
  is_active BOOLEAN DEFAULT true,
  last_triggered_at TIMESTAMP WITH TIME ZONE,
  total_triggers INTEGER DEFAULT 0,
  failed_triggers INTEGER DEFAULT 0,
  
  -- Metadata
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  deleted_at TIMESTAMP WITH TIME ZONE
);

-- Indexes
CREATE INDEX idx_webhooks_user_id ON webhooks(user_id);
CREATE INDEX idx_webhooks_is_active ON webhooks(is_active) WHERE is_active = true;
```

## 3. Database Functions & Triggers

### 3.1 Update Timestamp Function

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### 3.2 Update Session Stats Function

```sql
CREATE OR REPLACE FUNCTION update_session_message_stats()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE sessions
  SET 
    total_messages = total_messages + 1,
    total_tokens_used = total_tokens_used + COALESCE(NEW.tokens_total, 0),
    last_message_at = NEW.created_at,
    updated_at = NOW()
  WHERE id = NEW.session_id;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### 3.3 Update User Quota Function

```sql
CREATE OR REPLACE FUNCTION update_user_quota(
  p_user_id UUID,
  p_tokens INTEGER
)
RETURNS VOID AS $$
DECLARE
  v_quota_reset_date TIMESTAMP WITH TIME ZONE;
BEGIN
  SELECT quota_reset_date INTO v_quota_reset_date
  FROM users
  WHERE id = p_user_id;
  
  -- Reset quota if past reset date
  IF v_quota_reset_date IS NULL OR v_quota_reset_date < NOW() THEN
    UPDATE users
    SET 
      quota_used_current_month = p_tokens,
      quota_reset_date = NOW() + INTERVAL '1 month',
      updated_at = NOW()
    WHERE id = p_user_id;
  ELSE
    UPDATE users
    SET 
      quota_used_current_month = quota_used_current_month + p_tokens,
      updated_at = NOW()
    WHERE id = p_user_id;
  END IF;
END;
$$ LANGUAGE plpgsql;
```

### 3.4 Get Available API Key Function

```sql
CREATE OR REPLACE FUNCTION get_available_api_key(
  p_user_id UUID,
  p_provider VARCHAR(50)
)
RETURNS UUID AS $$
DECLARE
  v_key_id UUID;
BEGIN
  -- First, try to get user's own key
  SELECT id INTO v_key_id
  FROM api_keys
  WHERE user_id = p_user_id
    AND provider = p_provider
    AND is_active = true
    AND is_valid = true
    AND deleted_at IS NULL
  LIMIT 1;
  
  -- If no user key, get admin key with lowest usage
  IF v_key_id IS NULL THEN
    SELECT id INTO v_key_id
    FROM api_keys
    WHERE is_admin_key = true
      AND provider = p_provider
      AND is_active = true
      AND is_valid = true
      AND deleted_at IS NULL
      AND (rate_limit_reset_at IS NULL OR rate_limit_reset_at < NOW())
    ORDER BY total_requests ASC
    LIMIT 1;
  END IF;
  
  RETURN v_key_id;
END;
$$ LANGUAGE plpgsql;
```

### 3.5 Clean Old Data Function

```sql
CREATE OR REPLACE FUNCTION clean_old_data()
RETURNS VOID AS $$
BEGIN
  -- Delete sessions older than 90 days (soft deleted)
  UPDATE sessions
  SET deleted_at = NOW()
  WHERE created_at < NOW() - INTERVAL '90 days'
    AND deleted_at IS NULL;
  
  -- Delete files older than 30 days (soft deleted)
  UPDATE files
  SET deleted_at = NOW()
  WHERE created_at < NOW() - INTERVAL '30 days'
    AND deleted_at IS NULL;
  
  -- Hard delete soft-deleted records older than 7 days
  DELETE FROM messages WHERE deleted_at < NOW() - INTERVAL '7 days';
  DELETE FROM files WHERE deleted_at < NOW() - INTERVAL '7 days';
  DELETE FROM sessions WHERE deleted_at < NOW() - INTERVAL '7 days';
END;
$$ LANGUAGE plpgsql;
```

## 4. Views

### 4.1 User Stats View

```sql
CREATE VIEW user_stats AS
SELECT 
  u.id AS user_id,
  u.email,
  u.subscription_tier,
  u.quota_tokens_monthly,
  u.quota_used_current_month,
  (u.quota_tokens_monthly - u.quota_used_current_month) AS quota_remaining,
  COUNT(DISTINCT s.id) AS total_sessions,
  COUNT(DISTINCT m.id) AS total_messages,
  COALESCE(SUM(ul.tokens_total), 0) AS total_tokens_used_all_time,
  COALESCE(SUM(ul.cost_total), 0) AS total_cost_cents_all_time,
  u.created_at,
  u.last_active_at
FROM users u
LEFT JOIN sessions s ON s.user_id = u.id AND s.deleted_at IS NULL
LEFT JOIN messages m ON m.session_id = s.id AND m.deleted_at IS NULL
LEFT JOIN usage_logs ul ON ul.user_id = u.id
WHERE u.deleted_at IS NULL
GROUP BY u.id;
```

### 4.2 Session Summary View

```sql
CREATE VIEW session_summary AS
SELECT 
  s.id AS session_id,
  s.user_id,
  s.title,
  s.model,
  s.mode,
  s.total_messages,
  s.total_tokens_used,
  s.created_at,
  s.last_message_at,
  COUNT(DISTINCT m.id) AS message_count,
  COUNT(DISTINCT f.id) AS file_count,
  COUNT(DISTINCT te.id) AS tool_execution_count
FROM sessions s
LEFT JOIN messages m ON m.session_id = s.id AND m.deleted_at IS NULL
LEFT JOIN files f ON f.session_id = s.id AND f.deleted_at IS NULL
LEFT JOIN tool_executions te ON te.session_id = s.id
WHERE s.deleted_at IS NULL
GROUP BY s.id;
```

### 4.3 API Key Usage View

```sql
CREATE VIEW api_key_usage AS
SELECT 
  ak.id AS api_key_id,
  ak.user_id,
  ak.provider,
  ak.key_name,
  ak.is_admin_key,
  ak.total_requests,
  ak.total_tokens,
  ak.last_used_at,
  ak.is_active,
  ak.is_valid,
  COUNT(DISTINCT ul.id) AS usage_count_last_30_days,
  COALESCE(SUM(ul.tokens_total), 0) AS tokens_last_30_days
FROM api_keys ak
LEFT JOIN usage_logs ul ON ul.api_key_id = ak.id 
  AND ul.created_at > NOW() - INTERVAL '30 days'
WHERE ak.deleted_at IS NULL
GROUP BY ak.id;
```

## 5. Row Level Security (RLS) Policies

### 5.1 Users Table Policies

```sql
-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Users can read their own data
CREATE POLICY users_select_own
  ON users FOR SELECT
  USING (auth.uid() = auth_id);

-- Users can update their own data
CREATE POLICY users_update_own
  ON users FOR UPDATE
  USING (auth.uid() = auth_id);
```

### 5.2 Sessions Table Policies

```sql
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;

-- Users can read their own sessions
CREATE POLICY sessions_select_own
  ON sessions FOR SELECT
  USING (user_id IN (SELECT id FROM users WHERE auth_id = auth.uid()));

-- Users can insert their own sessions
CREATE POLICY sessions_insert_own
  ON sessions FOR INSERT
  WITH CHECK (user_id IN (SELECT id FROM users WHERE auth_id = auth.uid()));

-- Users can update their own sessions
CREATE POLICY sessions_update_own
  ON sessions FOR UPDATE
  USING (user_id IN (SELECT id FROM users WHERE auth_id = auth.uid()));

-- Users can delete their own sessions
CREATE POLICY sessions_delete_own
  ON sessions FOR DELETE
  USING (user_id IN (SELECT id FROM users WHERE auth_id = auth.uid()));
```

### 5.3 Messages Table Policies

```sql
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Users can read messages from their own sessions
CREATE POLICY messages_select_own
  ON messages FOR SELECT
  USING (session_id IN (
    SELECT id FROM sessions 
    WHERE user_id IN (SELECT id FROM users WHERE auth_id = auth.uid())
  ));

-- Users can insert messages to their own sessions
CREATE POLICY messages_insert_own
  ON messages FOR INSERT
  WITH CHECK (session_id IN (
    SELECT id FROM sessions 
    WHERE user_id IN (SELECT id FROM users WHERE auth_id = auth.uid())
  ));
```

### 5.4 Files Table Policies

```sql
ALTER TABLE files ENABLE ROW LEVEL SECURITY;

-- Users can read their own files
CREATE POLICY files_select_own
  ON files FOR SELECT
  USING (user_id IN (SELECT id FROM users WHERE auth_id = auth.uid()));

-- Users can insert their own files
CREATE POLICY files_insert_own
  ON files FOR INSERT
  WITH CHECK (user_id IN (SELECT id FROM users WHERE auth_id = auth.uid()));

-- Users can delete their own files
CREATE POLICY files_delete_own
  ON files FOR DELETE
  USING (user_id IN (SELECT id FROM users WHERE auth_id = auth.uid()));
```

### 5.5 API Keys Table Policies

```sql
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;

-- Users can read their own API keys (not admin keys)
CREATE POLICY api_keys_select_own
  ON api_keys FOR SELECT
  USING (user_id IN (SELECT id FROM users WHERE auth_id = auth.uid()));

-- Users can insert their own API keys
CREATE POLICY api_keys_insert_own
  ON api_keys FOR INSERT
  WITH CHECK (user_id IN (SELECT id FROM users WHERE auth_id = auth.uid()));

-- Users can delete their own API keys
CREATE POLICY api_keys_delete_own
  ON api_keys FOR DELETE
  USING (user_id IN (SELECT id FROM users WHERE auth_id = auth.uid()));
```

## 6. Data Models (TypeScript/Python)

### 6.1 TypeScript Models (Frontend)

```typescript
// types/database.ts

export interface User {
  id: string;
  email: string;
  username?: string;
  full_name?: string;
  avatar_url?: string;
  auth_id: string;
  bio?: string;
  website?: string;
  location?: string;
  preferences: UserPreferences;
  quota_tokens_monthly: number;
  quota_used_current_month: number;
  quota_reset_date?: string;
  subscription_tier: 'free' | 'pro' | 'enterprise';
  subscription_status: 'active' | 'cancelled' | 'expired' | 'trial';
  subscription_expires_at?: string;
  created_at: string;
  updated_at: string;
  last_active_at?: string;
}

export interface UserPreferences {
  theme: 'light' | 'dark';
  language: string;
  default_model: string;
  default_mode: 'sandbox' | 'local';
  notifications_enabled: boolean;
}

export interface Session {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  model: string;
  mode: 'sandbox' | 'local';
  temperature: number;
  max_tokens?: number;
  sandbox_container_id?: string;
  sandbox_status?: 'running' | 'hibernated' | 'stopped' | 'error';
  local_client_id?: string;
  context_summary?: string;
  total_messages: number;
  total_tokens_used: number;
  created_at: string;
  updated_at: string;
  last_message_at?: string;
  archived_at?: string;
}

export interface Message {
  id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system' | 'tool';
  content?: string;
  content_type: 'text' | 'markdown' | 'code' | 'image' | 'file' | 'error';
  model?: string;
  finish_reason?: 'stop' | 'length' | 'function_call' | 'content_filter' | 'error';
  tokens_prompt?: number;
  tokens_completion?: number;
  tokens_total?: number;
  function_calls?: FunctionCall[];
  tool_results?: ToolResult[];
  is_streaming: boolean;
  stream_completed_at?: string;
  user_rating?: number;
  user_feedback?: string;
  created_at: string;
  updated_at: string;
}

export interface FunctionCall {
  name: string;
  arguments: Record<string, any>;
}

export interface ToolResult {
  tool: string;
  action: string;
  result: any;
  error?: string;
  artifacts?: string[];
}

export interface File {
  id: string;
  user_id: string;
  session_id?: string;
  message_id?: string;
  filename: string;
  original_filename: string;
  mime_type: string;
  size_bytes: number;
  storage_path: string;
  storage_bucket: string;
  url?: string;
  file_category?: 'image' | 'document' | 'code' | 'data' | 'archive' | 'audio' | 'video' | 'other';
  is_public: boolean;
  processing_status: 'pending' | 'processing' | 'completed' | 'failed';
  extracted_text?: string;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface ApiKey {
  id: string;
  user_id?: string;
  provider: 'openai' | 'anthropic' | 'google' | 'other';
  key_name?: string;
  is_admin_key: boolean;
  total_requests: number;
  total_tokens: number;
  last_used_at?: string;
  is_active: boolean;
  is_valid: boolean;
  last_error?: string;
  last_error_at?: string;
  created_at: string;
  updated_at: string;
}

export interface UsageLog {
  id: string;
  user_id: string;
  session_id?: string;
  message_id?: string;
  api_key_id?: string;
  model: string;
  provider: string;
  tokens_prompt: number;
  tokens_completion: number;
  tokens_total: number;
  cost_prompt: number;
  cost_completion: number;
  cost_total: number;
  request_duration_ms?: number;
  response_cached: boolean;
  created_at: string;
}

export interface ToolExecution {
  id: string;
  session_id: string;
  message_id?: string;
  tool_name: string;
  tool_action?: string;
  tool_params?: Record<string, any>;
  execution_mode: 'sandbox' | 'local';
  execution_status: 'pending' | 'running' | 'completed' | 'failed' | 'timeout' | 'cancelled';
  result?: any;
  result_summary?: string;
  error_message?: string;
  started_at?: string;
  completed_at?: string;
  duration_ms?: number;
  artifacts?: any[];
  created_at: string;
}

export interface LocalClient {
  id: string;
  user_id: string;
  client_name: string;
  client_type: 'electron' | 'python-cli' | 'docker' | 'other';
  client_version?: string;
  is_connected: boolean;
  last_connected_at?: string;
  last_disconnected_at?: string;
  connection_count: number;
  capabilities: {
    python: boolean;
    nodejs: boolean;
    browser: boolean;
    shell: boolean;
  };
  workspace_path?: string;
  created_at: string;
  updated_at: string;
}
```

### 6.2 Python Models (Backend)

```python
# models/database.py

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class UserPreferences(BaseModel):
    theme: str = "dark"
    language: str = "en"
    default_model: str = "gpt-4"
    default_mode: str = "sandbox"
    notifications_enabled: bool = True

class User(BaseModel):
    id: UUID
    email: EmailStr
    username: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    auth_id: UUID
    bio: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    quota_tokens_monthly: int = 1_000_000
    quota_used_current_month: int = 0
    quota_reset_date: Optional[datetime] = None
    subscription_tier: str = "free"
    subscription_status: str = "active"
    subscription_expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    last_active_at: Optional[datetime] = None

class Session(BaseModel):
    id: UUID
    user_id: UUID
    title: str = "New Chat"
    description: Optional[str] = None
    model: str
    mode: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    sandbox_container_id: Optional[str] = None
    sandbox_status: Optional[str] = None
    local_client_id: Optional[UUID] = None
    context_summary: Optional[str] = None
    total_messages: int = 0
    total_tokens_used: int = 0
    created_at: datetime
    updated_at: datetime
    last_message_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None

class Message(BaseModel):
    id: UUID
    session_id: UUID
    role: str
    content: Optional[str] = None
    content_type: str = "text"
    model: Optional[str] = None
    finish_reason: Optional[str] = None
    tokens_prompt: Optional[int] = None
    tokens_completion: Optional[int] = None
    tokens_total: Optional[int] = None
    function_calls: Optional[List[Dict[str, Any]]] = None
    tool_results: Optional[List[Dict[str, Any]]] = None
    is_streaming: bool = False
    stream_completed_at: Optional[datetime] = None
    user_rating: Optional[int] = None
    user_feedback: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class File(BaseModel):
    id: UUID
    user_id: UUID
    session_id: Optional[UUID] = None
    message_id: Optional[UUID] = None
    filename: str
    original_filename: str
    mime_type: str
    size_bytes: int
    storage_path: str
    storage_bucket: str = "user-files"
    url: Optional[str] = None
    file_category: Optional[str] = None
    is_public: bool = False
    processing_status: str = "pending"
    extracted_text: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

class ApiKey(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    provider: str
    key_name: Optional[str] = None
    key_hash: str
    key_encrypted: str
    is_admin_key: bool = False
    total_requests: int = 0
    total_tokens: int = 0
    last_used_at: Optional[datetime] = None
    rate_limit_rpm: Optional[int] = None
    rate_limit_tpm: Optional[int] = None
    current_rpm: int = 0
    current_tpm: int = 0
    rate_limit_reset_at: Optional[datetime] = None
    is_active: bool = True
    is_valid: bool = True
    last_error: Optional[str] = None
    last_error_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class UsageLog(BaseModel):
    id: UUID
    user_id: UUID
    session_id: Optional[UUID] = None
    message_id: Optional[UUID] = None
    api_key_id: Optional[UUID] = None
    model: str
    provider: str
    tokens_prompt: int = 0
    tokens_completion: int = 0
    tokens_total: int = 0
    cost_prompt: int = 0
    cost_completion: int = 0
    cost_total: int = 0
    request_duration_ms: Optional[int] = None
    response_cached: bool = False
    created_at: datetime

class ToolExecution(BaseModel):
    id: UUID
    session_id: UUID
    message_id: Optional[UUID] = None
    tool_name: str
    tool_action: Optional[str] = None
    tool_params: Optional[Dict[str, Any]] = None
    execution_mode: str
    execution_status: str
    result: Optional[Any] = None
    result_summary: Optional[str] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    artifacts: Optional[List[Any]] = None
    created_at: datetime

class LocalClient(BaseModel):
    id: UUID
    user_id: UUID
    client_name: str
    client_type: str
    client_version: Optional[str] = None
    is_connected: bool = False
    last_connected_at: Optional[datetime] = None
    last_disconnected_at: Optional[datetime] = None
    connection_count: int = 0
    capabilities: Dict[str, bool] = Field(default_factory=lambda: {
        "python": True,
        "nodejs": True,
        "browser": True,
        "shell": True
    })
    workspace_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
```

## 7. Redis Cache Schema

### 7.1 Cache Keys Structure

```
# User session cache
user:session:{user_id} → User object (TTL: 1 hour)

# API key cache
api_key:{key_hash} → ApiKey object (TTL: 5 minutes)

# Rate limiting
rate_limit:user:{user_id}:{endpoint} → Request count (TTL: 1 minute)
rate_limit:api_key:{key_id} → Token count (TTL: 1 minute)

# Active sessions
active_session:{session_id} → Session object (TTL: 5 minutes)

# WebSocket connections
ws:connection:{user_id} → Connection ID (TTL: until disconnect)

# Quota cache
quota:{user_id} → Remaining tokens (TTL: 1 hour)

# Container status
container:{container_id} → Status object (TTL: 1 minute)
```

### 7.2 Cache Invalidation Strategy

- **User updates** → Invalidate `user:session:{user_id}`
- **API key updates** → Invalidate `api_key:{key_hash}`
- **Session updates** → Invalidate `active_session:{session_id}`
- **Quota updates** → Invalidate `quota:{user_id}`
- **On logout** → Clear all user-related caches

## 8. Database Migrations Strategy

### 8.1 Migration Tools
- **Supabase Migrations**: Built-in migration system
- **Version Control**: All migrations in Git
- **Rollback**: Support for rollback on failure

### 8.2 Migration Workflow
1. Create migration file (SQL)
2. Test on local Supabase instance
3. Review and approve
4. Apply to staging
5. Test thoroughly
6. Apply to production
7. Monitor for issues

### 8.3 Backup Strategy
- **Automated Backups**: Daily full backups (Supabase)
- **Point-in-Time Recovery**: 7 days retention
- **Manual Backups**: Before major migrations
- **Backup Testing**: Monthly restore tests

## 9. Performance Optimization

### 9.1 Indexing Strategy
- **Primary Keys**: All tables have UUID primary keys
- **Foreign Keys**: Indexed for join performance
- **Frequently Queried**: user_id, session_id, created_at
- **Composite Indexes**: (user_id, created_at) for user queries

### 9.2 Query Optimization
- **Pagination**: Use cursor-based pagination for large lists
- **Eager Loading**: Join related tables when needed
- **Lazy Loading**: Load heavy fields (content, metadata) on demand
- **Caching**: Cache frequent queries in Redis

### 9.3 Data Archival
- **Old Sessions**: Archive sessions >90 days to cold storage
- **Old Files**: Move files >30 days to glacier storage
- **Usage Logs**: Aggregate old logs, delete raw data
- **Cleanup Job**: Run daily cleanup function

---

**Document Version**: 1.0  
**Last Updated**: 2024-01-XX  
**Status**: Draft - Pending Review

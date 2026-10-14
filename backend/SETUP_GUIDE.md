# Enterprise AI Platform - Setup Guide

This guide explains how to set up and use the adjusted files for the Enterprise AI Workflow and Automation Platform with login, signup, permissions, and role-based access control.

## Updated Files

### 1. Auth-Service Models (`services/auth-service/app/models.py`)
- Added `Company` model for multi-tenancy
- Added `Permission` model for fine-grained permissions
- Added `Role` model for role-based access control
- Added `RolePermission` association table for many-to-many relationship
- Updated `User` model with additional fields:
  - `username`, `first_name`, `last_name`, `full_name`
  - `is_superuser`, `is_verified`
  - `role_id` (foreign key to Role)
  - `company_id` (foreign key to Company)
  - `password_hash` (backward compatibility with `hashed_password`)

### 2. Auth-Service Schemas (`services/auth-service/app/schemas.py`)
- Updated `RegisterRequest` to include optional fields:
  - `username`, `first_name`, `last_name`
- Updated `UserResponse` to include:
  - `username`, `first_name`, `last_name`, `full_name`
  - `is_superuser`, `is_verified`

### 3. Auth-Service Main (`services/auth-service/app/main.py`)
- Updated `/auth/register` endpoint to handle new user fields
- Auto-generates `username` from email if not provided
- Auto-generates `full_name` from first/last name

### 4. add_permissions.py
- Updated to work with auth-service database structure
- Seeds 22 permissions across modules:
  - Documents (upload, view, delete, view all)
  - Search & Chat (search, chat, extract, summarize, download)
  - User Management (view users, block users)
  - Role Management (view, create, update, delete roles)
  - Company Management (view, manage companies)

### 5. populate.py
- Updated to work with auth-service structure
- Creates two roles:
  - **Super role** (code: `admin`) - All permissions
  - **Employee role** (code: `user`) - Limited permissions
- Creates default company: "Document AI System"
- Creates 3 superusers:
  1. `superuser@example.com` / `Admin@1234`
  2. `syedjawadali92@gmail.com` / `Admin@1234`
  3. `nicenick1992@gmail.com` / `Admin@1234`

### 6. start.py
- Updated to support microservices architecture
- Can start individual services:
  - `python start.py` - API Gateway (port 8000)
  - `python start.py auth` - Auth Service (port 8001)
  - `python start.py workflow` - Workflow Service (port 8002)
  - `python start.py ai` - AI Service (port 8003)
  - `python start.py integration` - Integration Service (port 8004)
  - `python start.py notification` - Notification Service (port 8005)
  - `python start.py audit` - Audit Service (port 8006)
- Supports custom ports and production mode

### 7. test_db.py
- Updated to work with the new database configuration
- Creates `platform` database (matches docker-compose.yml)
- Enables `pgvector` and `uuid-ossp` extensions
- Creates schemas: `auth`, `workflow`, `ai`, `audit`, `integration`
- Environment variable support for configuration

### 8. test_groq.py
- Added error handling for missing API key
- Better output formatting
- Clear instructions for setup

### 9. init_db.py
- Updated to initialize all service databases
- Creates tables for auth, workflow, ai, and audit services

### 10. init_auth_db.py (NEW)
- Dedicated script to initialize only auth-service tables
- Useful for faster development cycles

## Setup Instructions

### Prerequisites
- Python 3.9+
- PostgreSQL 16+ with pgvector extension
- Redis
- RabbitMQ

### Step 1: Environment Setup
```bash
# Copy environment file
cp .env.example .env

# Edit .env with your configuration
# Required:
# - JWT_SECRET
# - GROQ_API_KEY (if using Groq)
# - Database credentials (if not using defaults)
```

### Step 2: Database Setup
```bash
# Option A: Using Docker (Recommended)
docker compose up -d postgres

# Option B: Local PostgreSQL
python test_db.py
```

### Step 3: Initialize Database Tables
```bash
# Initialize all service tables
python init_db.py

# OR initialize only auth-service
python init_auth_db.py
```

### Step 4: Seed Permissions
```bash
python add_permissions.py
```

### Step 5: Seed Roles and Users
```bash
python populate.py
```

### Step 6: Start Services

#### Option A: Start All Services (Docker)
```bash
docker compose up
```

#### Option B: Start Individual Services (Development)
```bash
# Start auth-service
python start.py auth

# In another terminal, start workflow-service
python start.py workflow

# In another terminal, start ai-service
python start.py ai

# In another terminal, start api-gateway
python start.py gateway
```

## API Usage

### Register a New User
```bash
curl -X POST http://localhost:8001/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "role": "USER",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login
```bash
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

### Access Protected Endpoints
Use the access token from login response:
```bash
curl -X GET http://localhost:8000/api/v1/workflows \
  -H "Authorization: Bearer <access_token>"
```

## Default Credentials

After running `populate.py`, you can use these credentials:

| Email | Password | Role | Superuser |
|-------|----------|------|-----------|
| superuser@example.com | Admin@1234 | Super | Yes |
| syedjawadali92@gmail.com | Admin@1234 | Super | Yes |
| nicenick1992@gmail.com | Admin@1234 | Super | Yes |

## Permission Structure

### Documents Module
- `can_upload_document` - Upload PDF documents
- `can_view_documents` - View own documents
- `can_delete_document` - Delete own documents
- `can_view_all_documents` - View all users documents (admin)

### Search & Chat Module
- `can_search` - Search document content
- `can_chat` - Ask AI questions about documents
- `can_extract` - Extract structured data from documents
- `can_summarize` - Generate AI summaries
- `can_download_report` - Download PDF reports

### User Management Module
- `can_view_users` - View user list
- `can_block_users` - Block or unblock users

### Role Management Module
- `can_view_roles` - View roles
- `can_create_role` - Create new roles
- `can_update_role` - Update role permissions
- `can_delete_role` - Delete roles

### Company Management Module
- `can_view_companies` - View companies
- `can_manage_companies` - Create/update/delete companies

## Role Permissions

### Super Role (admin)
- All permissions

### Employee Role (user)
- `can_upload_document`
- `can_view_documents`
- `can_delete_document`
- `can_search`
- `can_chat`
- `can_summarize`
- `can_download_report`

## Troubleshooting

### Database Connection Issues
```bash
# Test database connection
python test_db.py

# Check if PostgreSQL is running
docker compose ps postgres
```

### Permission Errors
```bash
# Re-seed permissions
python add_permissions.py
```

### User Login Issues
```bash
# Re-populate users
python populate.py
```

### Service Won't Start
```bash
# Check port availability
netstat -an | grep 8001

# Use different port
python start.py auth --port 8002
```

## Architecture Notes

- **Auth Service** (port 8001): Handles authentication, authorization, user management
- **Workflow Service** (port 8002): Manages business workflows
- **AI Service** (port 8003): AI reasoning and LangGraph flows
- **Integration Service** (port 8004): External integrations
- **Notification Service** (port 8005): Notifications
- **Audit Service** (port 8006): Audit logging
- **API Gateway** (port 8000): Single entry point for all services

## Next Steps

1. Implement API Gateway routing with JWT verification
2. Add role-based permission checking in each service
3. Implement frontend integration
4. Add audit logging for all user actions
5. Set up proper Alembic migrations for schema changes

# SUPPORT SYSTEM PHASE 1 - COMPLETE WORKING FLOW

## PROJECT OVERVIEW

AI-Based Support Intelligence System - Phase 1
- **Purpose**: Customer Support Management System with Authentication & Authorization
- **Version**: 1.0.0
- **Status**: Development Ready

---

## TABLE OF CONTENTS

1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Installation & Setup](#installation--setup)
5. [Database Setup](#database-setup)
6. [Configuration](#configuration)
7. [API Endpoints](#api-endpoints)
8. [Authentication Flow](#authentication-flow)
9. [Testing Guide](#testing-guide)
10. [Troubleshooting](#troubleshooting)
11. [Development Workflow](#development-workflow)

---

## SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│           FastAPI Application Server                     │
│  (Port 8000 - http://127.0.0.1:8000)                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │          API Routes Layer                        │  │
│  │  ├─ /api/customer/* (Customer Auth)             │  │
│  │  ├─ /api/engineer/* (Engineer Auth)             │  │
│  │  └─ /api/* (Future endpoints)                   │  │
│  └──────────────────────────────────────────────────┘  │
│                        │                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │    Authentication & Authorization Layer          │  │
│  │  ├─ JWT Token Management                        │  │
│  │  ├─ Cookie-based Session Management             │  │
│  │  ├─ Permission Verification                     │  │
│  │  └─ Role-based Access Control                   │  │
│  └──────────────────────────────────────────────────┘  │
│                        │                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │      Database Access Layer                       │  │
│  │  ├─ PyMongo Driver                              │  │
│  │  ├─ Connection Management                       │  │
│  │  └─ Data Validation (Pydantic)                  │  │
│  └──────────────────────────────────────────────────┘  │
│                        │                                │
└────────────────────────┼────────────────────────────────┘
                         │
                    [MongoDB]
                    Port 27017
                    Database: support_system_db
```

---

## TECHNOLOGY STACK

### Backend Framework
- **FastAPI** 0.104.1+ - Modern async Python web framework
- **Uvicorn** - ASGI server for running FastAPI
- **Python** 3.10+ - Programming language

### Database
- **MongoDB** 5.0+ - NoSQL database
- **PyMongo** 4.16.0+ - Python MongoDB driver

### Authentication & Security
- **PyJWT** - JWT token creation and validation
- **bcrypt** - Password hashing and verification
- **Pydantic** - Data validation and settings management

### Development Tools
- **pydantic-settings** - Environment variable management
- **httpx** - HTTP client for testing

---

## PROJECT STRUCTURE

```
support-system-phase1/
│
├── .venv/                          # Virtual environment
│
├── support-system-phase1/          # Application root
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app initialization
│   │   ├── config.py               # Configuration & settings
│   │   ├── database.py             # MongoDB connection & initialization
│   │   │
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── jwt_handler.py      # JWT token creation/validation
│   │   │   └── permissions.py      # Authorization & permission checks
│   │   │
│   │   ├── models/
│   │   │   ├── customer.py         # Customer data model
│   │   │   ├── role.py             # Role data model
│   │   │   └── support_engineer.py # Engineer data model
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── customer_auth.py    # Customer login/register/me endpoints
│   │   │   └── engineer_auth.py    # Engineer login/me endpoints
│   │   │
│   │   ├── schemas/
│   │   │   ├── customer.py         # Customer request/response schemas
│   │   │   └── support_engineer.py # Engineer request/response schemas
│   │   │
│   │   ├── utils/
│   │   │   └── security.py         # Password hashing/verification utilities
│   │   │
│   │   └── .env                    # Environment variables
│   │
│   ├── init_db.py                  # Database initialization script
│   ├── mongo_setup.js              # MongoDB shell setup script
│   └── requirements.txt            # Python dependencies
│
├── COMPLETE_WORKING_FLOW.txt       # This file
└── README.md                       # Project README
```

---

## INSTALLATION & SETUP

### Step 1: Clone/Setup Project

```bash
# Navigate to project directory
cd "e:\A Simprosys Intern Project\support-system-phase1"

# Create virtual environment (if not exists)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### Step 2: Install Dependencies

```bash
# Navigate to app directory
cd support-system-phase1/app

# Install all required packages
pip install -r requirements.txt

# Or install individually:
pip install fastapi uvicorn pymongo pydantic-settings PyJWT bcrypt python-multipart
```

### Step 3: Start MongoDB

**Option A: Using Docker (Recommended)**
```bash
# Pull MongoDB image (first time only)
docker pull mongo:latest

# Run MongoDB container
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Verify connection
docker logs mongodb
```

**Option B: Local Installation**
```bash
# Windows - Start MongoDB service
net start MongoDB

# Linux
sudo systemctl start mongod

# Mac
brew services start mongodb-community
```

**Verify MongoDB is Running:**
```bash
# Test connection
mongosh
# You should see a connection prompt
```

### Step 4: Initialize Database

**Option A: Using Python Script**
```bash
# From project root directory
python support-system-phase1/init_db.py
```

**Option B: Using MongoDB Shell**
```bash
# Open MongoDB shell
mongosh

# Load and run setup script
load("mongo_setup.js")
```

---

## DATABASE SETUP

### Collections Structure

#### 1. **roles** Collection
```json
{
  "_id": ObjectId,
  "role_id": 1,
  "role_name": "admin",
  "permissions": ["create_ticket", "view_all_tickets", ...],
  "created_at": ISODate
}
```

#### 2. **support_engineers** Collection
```json
{
  "_id": ObjectId,
  "support_id": 100,
  "name": "System Admin",
  "email": "admin@company.com",
  "password": "$2b$12$...",  // bcrypt hash
  "role_id": 1,
  "department": "administration",
  "is_active": true,
  "is_online": false,
  "last_seen": ISODate,
  "created_at": ISODate
}
```

#### 3. **customers** Collection
```json
{
  "_id": ObjectId,
  "customer_id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "password": "$2b$12$...",  // bcrypt hash
  "is_active": true,
  "created_at": ISODate,
  "last_login": ISODate
}
```

#### 4. **refresh_tokens** Collection
```json
{
  "_id": ObjectId,
  "user_id": 1,
  "user_type": "customer",
  "token": "eyJhbGciOiAiSFM...",
  "is_active": true,
  "expires_at": ISODate,
  "created_at": ISODate,
  "revoked_at": null
}
```

#### 5. **tickets** Collection (Future Use)
```json
{
  "_id": ObjectId,
  "ticket_number": "TKT-001",
  "customer_id": 1,
  "assigned_engineer_id": 100,
  "title": "Login Issue",
  "description": "Cannot login with correct password",
  "status": "open",
  "priority": "high",
  "created_at": ISODate,
  "updated_at": ISODate,
  "resolved_at": null
}
```

#### 6. **messages** Collection (Future Use)
```json
{
  "_id": ObjectId,
  "ticket_id": ObjectId,
  "sender_id": 1,
  "sender_type": "customer",
  "message": "Please help me with login issue",
  "created_at": ISODate
}
```

### Default Data

**Roles:**
- Admin (ID: 1)
- Support Engineer (ID: 2)

**Admin User:**
- Email: `admin@company.com`
- Password: `AdminPass123!`
- Support ID: 100

**Support Engineers:**
1. Rahul Kumar (rahul@company.com) - Technical
2. Priya Sharma (priya@company.com) - Billing
3. Amit Singh (amit@company.com) - Customer Success

---

## CONFIGURATION

### Environment Variables (.env)

Located at: `support-system-phase1/app/.env`

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=support_system_db

# JWT Configuration
SECRET_KEY=your-secret-key-change-in-production-must-be-32-chars-minimum
ALGORITHM=HS256

# Token Expiry (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=5
REFRESH_TOKEN_EXPIRE_MINUTES=10

# Cookie Configuration
COOKIE_NAME=access_token
COOKIE_DOMAIN=None
COOKIE_PATH=/
COOKIE_SECURE=False
COOKIE_HTTPONLY=True
COOKIE_SAMESITE=lax

# Session Configuration
SESSION_SECRET_KEY=session-secret-key-very-secret
SESSION_EXPIRE_MINUTES=60
```

### Config Class (config.py)

All settings are loaded from `.env` file using Pydantic Settings:

```python
class Settings(BaseSettings):
    MONGODB_URL: str
    DATABASE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    COOKIE_NAME: str
    COOKIE_DOMAIN: Optional[str]
    COOKIE_PATH: str
    COOKIE_SECURE: bool
    COOKIE_HTTPONLY: bool
    COOKIE_SAMESITE: str
    SESSION_SECRET_KEY: str
    SESSION_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()
```

---

## API ENDPOINTS

### Base URL
```
http://localhost:8000
```

### Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Root Endpoints

#### 1. GET `/`
Returns API information and available endpoints

**Response:**
```json
{
  "message": "AI-Based Support Intelligence System - Phase 1",
  "app_name": "Customer Support with RAG",
  "version": "1.0.0",
  "status": "running",
  "docs_url": "/docs",
  "endpoints": {
    "customer": {
      "register": "/api/customer/register",
      "login": "/api/customer/login",
      "me": "/api/customer/me",
      "logout": "/api/customer/logout",
      "refresh": "/api/customer/refresh"
    },
    "engineer": {
      "login": "/api/engineer/login",
      "me": "/api/engineer/me",
      "logout": "/api/engineer/logout",
      "refresh": "/api/engineer/refresh"
    }
  }
}
```

#### 2. GET `/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "Support System API",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

---

### CUSTOMER ENDPOINTS

#### 1. POST `/api/customer/register`
Register a new customer account

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "customer_id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00.000Z",
    "last_login": null
  }
}
```

**Errors:**
- `400 Bad Request`: Email already registered / Invalid password
- `422 Unprocessable Entity`: Invalid input format

---

#### 2. POST `/api/customer/login`
Login as customer

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "customer_id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00.000Z",
    "last_login": "2024-01-15T10:35:00.000Z"
  }
}
```

**Errors:**
- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Account inactive

---

#### 3. GET `/api/customer/me`
Get current customer profile

**Headers:**
```
Cookie: access_token=<jwt_token>
```

**Response (200 OK):**
```json
{
  "customer_id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00.000Z",
  "last_login": "2024-01-15T10:35:00.000Z"
}
```

**Errors:**
- `401 Unauthorized`: Token missing or expired
- `404 Not Found`: Customer not found
- `403 Forbidden`: Account inactive

---

#### 4. POST `/api/customer/logout`
Logout customer (revoke refresh tokens, clear cookie)

**Headers:**
```
Cookie: access_token=<jwt_token>
```

**Response (200 OK):**
```json
{
  "message": "Logged out successfully",
  "status": "success"
}
```

**Errors:**
- `401 Unauthorized`: Token missing or invalid

---

#### 5. POST `/api/customer/refresh`
Refresh access token using refresh token

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 300
}
```

**Errors:**
- `401 Unauthorized`: Invalid or expired refresh token
- `401 Unauthorized`: Token revoked

---

### ENGINEER ENDPOINTS

#### 1. POST `/api/engineer/login`
Login as support engineer

**Request Body:**
```json
{
  "email": "rahul@company.com",
  "password": "TechPass123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "support_id": 101,
    "name": "Rahul Kumar",
    "email": "rahul@company.com",
    "role_id": 2,
    "department": "technical",
    "is_active": true,
    "is_online": true,
    "created_at": "2024-01-15T10:30:00.000Z",
    "last_seen": "2024-01-15T10:35:00.000Z"
  }
}
```

**Errors:**
- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Account inactive

---

#### 2. GET `/api/engineer/me`
Get current engineer profile

**Headers:**
```
Cookie: access_token=<jwt_token>
```

**Response (200 OK):**
```json
{
  "support_id": 101,
  "name": "Rahul Kumar",
  "email": "rahul@company.com",
  "role_id": 2,
  "department": "technical",
  "is_active": true,
  "is_online": true,
  "created_at": "2024-01-15T10:30:00.000Z",
  "last_seen": "2024-01-15T10:35:00.000Z"
}
```

**Errors:**
- `401 Unauthorized`: Token missing or expired
- `404 Not Found`: Engineer not found
- `403 Forbidden`: Account inactive

---

#### 3. POST `/api/engineer/logout`
Logout engineer

**Headers:**
```
Cookie: access_token=<jwt_token>
```

**Response (200 OK):**
```json
{
  "message": "Logged out successfully",
  "status": "success"
}
```

---

#### 4. POST `/api/engineer/refresh`
Refresh engineer access token

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 300
}
```

---

## AUTHENTICATION FLOW

### 1. Customer Registration Flow

```
┌─────────────────┐
│   Client        │
└────────┬────────┘
         │
         │ POST /api/customer/register
         │ { name, email, password }
         ▼
┌──────────────────┐
│   FastAPI App    │
├──────────────────┤
│ 1. Check email   │
│    uniqueness    │
│                  │
│ 2. Hash password │
│    (bcrypt)      │
│                  │
│ 3. Create        │
│    customer doc  │
│                  │
│ 4. Generate JWT: │
│    - Access      │
│    - Refresh     │
│                  │
│ 5. Store refresh │
│    in DB         │
│                  │
│ 6. Set cookie    │
│    (access)      │
└────────┬─────────┘
         │
         │ Response:
         │ - access_token
         │ - refresh_token
         │ - user object
         │ - Set-Cookie header
         ▼
┌─────────────────┐
│   Client        │
│ (Logged In)     │
└─────────────────┘
```

### 2. Customer Login Flow

```
┌─────────────────┐
│   Client        │
└────────┬────────┘
         │
         │ POST /api/customer/login
         │ { email, password }
         ▼
┌──────────────────┐
│   FastAPI App    │
├──────────────────┤
│ 1. Find customer │
│    by email      │
│                  │
│ 2. Verify pwd    │
│    (bcrypt)      │
│                  │
│ 3. Check if      │
│    is_active     │
│                  │
│ 4. Generate JWT: │
│    - Access      │
│    - Refresh     │
│                  │
│ 5. Store refresh │
│    in DB         │
│                  │
│ 6. Set cookie    │
│    (access)      │
│                  │
│ 7. Update        │
│    last_login    │
└────────┬─────────┘
         │
         │ Response: tokens + user
         ▼
┌─────────────────┐
│   Client        │
│ (Logged In)     │
└─────────────────┘
```

### 3. Token Refresh Flow

```
┌─────────────────┐
│   Client        │
│ (Access expired)│
└────────┬────────┘
         │
         │ POST /api/customer/refresh
         │ { refresh_token }
         ▼
┌──────────────────┐
│   FastAPI App    │
├──────────────────┤
│ 1. Decode        │
│    refresh token │
│                  │
│ 2. Find token    │
│    in DB         │
│                  │
│ 3. Check if      │
│    is_active     │
│                  │
│ 4. Generate new  │
│    access token  │
│                  │
│ 5. Set cookie    │
│    (new access)  │
└────────┬─────────┘
         │
         │ Response:
         │ - access_token
         │ - expires_in
         │ - Set-Cookie header
         ▼
┌─────────────────┐
│   Client        │
│ (Token renewed) │
└─────────────────┘
```

### 4. Request with Authentication

```
┌─────────────────────────────┐
│    Client Request           │
├─────────────────────────────┤
│ GET /api/customer/me        │
│ Headers:                    │
│   Cookie: access_token=...  │
└────────┬────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│    Permission Manager            │
├──────────────────────────────────┤
│ 1. Extract token from cookie    │
│                                  │
│ 2. Verify JWT signature         │
│    (SECRET_KEY, HS256)          │
│                                  │
│ 3. Check expiry (exp claim)     │
│                                  │
│ 4. Validate token type          │
│    (access vs refresh)          │
│                                  │
│ 5. Verify user type             │
│    (customer vs engineer)       │
│                                  │
│ 6. Return payload with          │
│    user_id & claims             │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│    Route Handler                 │
├──────────────────────────────────┤
│ 1. Fetch customer from DB        │
│    using customer_id             │
│                                  │
│ 2. Check is_active status       │
│                                  │
│ 3. Return customer data          │
└────────┬─────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│    Response (200 OK)        │
│    Customer object          │
└─────────────────────────────┘
```

### Token Structure (JWT)

**Access Token Payload:**
```json
{
  "sub": 1,                    // user_id
  "user_type": "customer",     // or "engineer"
  "email": "john@example.com",
  "type": "access",
  "iat": 1705336200,           // issued at
  "exp": 1705336500            // expires in 5 minutes
}
```

**Refresh Token Payload:**
```json
{
  "sub": 1,                    // user_id
  "user_type": "customer",
  "email": "john@example.com",
  "type": "refresh",
  "iat": 1705336200,
  "exp": 1705952200            // expires in 10 minutes
}
```

---

## TESTING GUIDE

### Prerequisites
- MongoDB running (localhost:27017)
- FastAPI server running (localhost:8000)
- API credentials initialized (run mongo_setup.js)

### Using Swagger UI (Recommended)

1. Open browser: http://localhost:8000/docs
2. Click on endpoint
3. Click "Try it out"
4. Fill in request body
5. Click "Execute"

### Using cURL Commands

#### 1. Register Customer
```bash
curl -X POST "http://localhost:8000/api/customer/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Smith",
    "email": "alice@example.com",
    "password": "AlicePass123!"
  }'
```

#### 2. Login Customer
```bash
curl -X POST "http://localhost:8000/api/customer/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "AlicePass123!"
  }' \
  -v  # -v to see Set-Cookie headers
```

#### 3. Get Current Customer (with cookie)
```bash
curl -X GET "http://localhost:8000/api/customer/me" \
  -H "Cookie: access_token=<YOUR_ACCESS_TOKEN>"
```

#### 4. Login Engineer
```bash
curl -X POST "http://localhost:8000/api/engineer/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "rahul@company.com",
    "password": "TechPass123!"
  }'
```

#### 5. Refresh Token
```bash
curl -X POST "http://localhost:8000/api/customer/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "<YOUR_REFRESH_TOKEN>"
  }'
```

#### 6. Logout
```bash
curl -X POST "http://localhost:8000/api/customer/logout" \
  -H "Cookie: access_token=<YOUR_ACCESS_TOKEN>"
```

### Using Postman

1. Import collection (if available) or create requests manually
2. Set up environment variables:
   - `base_url`: http://localhost:8000
   - `access_token`: (set from login response)
   - `refresh_token`: (set from login response)

3. Test endpoints:
   - POST register
   - POST login
   - GET me
   - POST logout
   - POST refresh

### Test Scenarios

#### Scenario 1: Registration Flow
```
1. Register new customer
   Status: 201 Created
   ✓ Check user received access_token
   ✓ Check user received refresh_token
   ✓ Check customer_id is assigned
   ✓ Check cookie is set

2. Try register same email again
   Status: 400 Bad Request
   ✓ Check "Email already registered" message
```

#### Scenario 2: Login & Profile Access
```
1. Login with valid credentials
   Status: 200 OK
   ✓ Check tokens received
   ✓ Check last_login updated

2. Get profile (/me)
   Status: 200 OK
   ✓ Check all customer data returned

3. Logout
   Status: 200 OK
   ✓ Check "Logged out successfully" message

4. Try /me after logout
   Status: 401 Unauthorized
   ✓ Check token invalid message
```

#### Scenario 3: Token Expiry & Refresh
```
1. Get access token from login
2. Wait 5+ minutes (or manually expire)
3. Try /me with expired token
   Status: 401 Unauthorized

4. Use refresh token
   Status: 200 OK
   ✓ Check new access_token received
   ✓ Check new cookie set

5. Use new access token for /me
   Status: 200 OK
```

#### Scenario 4: Invalid Credentials
```
1. Login with wrong email
   Status: 401 Unauthorized
   ✓ Check "Invalid email or password"

2. Login with wrong password
   Status: 401 Unauthorized
   ✓ Check "Invalid email or password"

3. Account inactive (set is_active=false in DB)
   Status: 403 Forbidden
   ✓ Check "account is inactive"
```

#### Scenario 5: Engineer Authentication
```
1. Login as engineer
   Status: 200 OK
   ✓ Check role_id is 2
   ✓ Check support_id assigned

2. Get engineer profile
   Status: 200 OK
   ✓ Check department info
   ✓ Check is_online status

3. Logout
   Status: 200 OK
```

---

## TROUBLESHOOTING

### MongoDB Connection Issues

**Error: "Cannot connect to MongoDB"**
```
Solution:
1. Check MongoDB is running:
   - Docker: docker ps | grep mongodb
   - Local: Check mongod process

2. Verify port 27017 is open:
   - netstat -an | findstr 27017 (Windows)
   - lsof -i :27017 (Linux/Mac)

3. Check MONGODB_URL in .env:
   - Should be: mongodb://localhost:27017
   - For Docker with bridge: mongodb://host.docker.internal:27017

4. Restart MongoDB:
   - Docker: docker restart mongodb
   - Local: Restart mongod service
```

### FastAPI Server Issues

**Error: "Address already in use"**
```
Solution:
1. Find process using port 8000:
   - netstat -ano | findstr :8000 (Windows)
   - lsof -i :8000 (Linux/Mac)

2. Kill process:
   - taskkill /PID <PID> /F (Windows)
   - kill -9 <PID> (Linux/Mac)

3. Or use different port:
   - uvicorn main:app --reload --port 8001
```

**Error: "Module not found"**
```
Solution:
1. Check virtual environment is activated:
   - (.venv) should appear in terminal

2. Reinstall dependencies:
   - pip install -r requirements.txt

3. Check Python path:
   - python --version
   - which python
```

### Authentication Issues

**Error: "401 Unauthorized"**
```
Causes:
1. Token missing:
   - Cookie not sent
   - Token expired

2. Token invalid:
   - Malformed token
   - Wrong SECRET_KEY
   - Token for wrong user type

Solution:
1. Check browser cookies:
   - F12 → Application → Cookies

2. Verify token in JWT:
   - Visit jwt.io
   - Paste token
   - Check payload

3. Get fresh token:
   - Login again
   - Use new token
```

**Error: "403 Forbidden"**
```
Causes:
1. Account inactive (is_active = false)
2. Token type mismatch (customer token on engineer endpoint)
3. Insufficient permissions

Solution:
1. Check DB:
   - db.customers.findOne({email: "..."})
   - Verify is_active: true

2. Use correct endpoint:
   - Customer token → /api/customer/*
   - Engineer token → /api/engineer/*

3. Reactivate account in DB if needed
```

### Database Issues

**Error: "Duplicate key error"**
```
Cause: Email already exists

Solution:
1. Use different email
2. Delete record:
   - db.customers.deleteOne({email: "..."})
3. Check uniqueness:
   - db.customers.getIndexes()
```

**Missing Collections/Indexes**
```
Solution:
1. Run initialization script:
   - python init_db.py
   OR
   - mongosh < mongo_setup.js

2. Manual creation:
   - db.createCollection("collection_name")
   - db.collection.createIndex(...)
```

---

## DEVELOPMENT WORKFLOW

### Daily Development Cycle

```
1. Activate Virtual Environment
   .venv\Scripts\activate

2. Start MongoDB
   docker start mongodb
   OR access local MongoDB

3. Start FastAPI Server
   cd support-system-phase1/app
   uvicorn main:app --reload

4. Open API Docs
   http://localhost:8000/docs

5. Make Changes
   Edit code in your IDE

6. Test Changes
   - Use Swagger UI
   - Check browser console
   - Monitor server logs

7. Commit Changes
   git add .
   git commit -m "Description of changes"
```

### Project Organization

**By Feature:**
```
routes/
├── customer_auth.py    # Customer endpoints
├── engineer_auth.py    # Engineer endpoints
└── tickets.py          # Ticket endpoints (future)
```

**By Layer:**
```
├── auth/               # Authentication layer
├── models/             # Data models
├── schemas/            # Request/response schemas
├── routes/             # API endpoints
├── utils/              # Utility functions
└── database.py         # Database layer
```

### Adding New Endpoints

1. Create route file: `routes/new_feature.py`
2. Define request/response schemas: `schemas/new_feature.py`
3. Add router to `main.py`: `app.include_router(new_router)`
4. Test using Swagger UI

### New Dependencies

```bash
# Install
pip install package_name

# Add to requirements.txt
pip freeze > requirements.txt

# Commit
git add requirements.txt
git commit -m "Add package_name dependency"
```

### Database Migrations

For schema changes:
1. Plan the change
2. Create migration script (or instructions)
3. Test on dev database
4. Document in CHANGELOG
5. Execute on production with backup

---

## PERFORMANCE CONSIDERATIONS

### Database Optimization
- All frequently queried fields have indexes
- `created_at` indexed for sorting
- Unique constraints on `email` fields

### Security Best Practices
- Passwords hashed with bcrypt (12 rounds)
- JWT tokens signed with SECRET_KEY
- HTTP-only cookies prevent XSS
- SameSite=Lax prevents CSRF
- Refresh tokens stored in DB (can be revoked)

### Caching Opportunities (Future)
- Cache roles in memory (rarely change)
- Cache permission mappings
- Session caching with Redis

---

## NEXT PHASES

### Phase 2 Features
- Ticket management system
- Real-time messaging
- Admin dashboard
- Analytics and reporting

### Phase 3 Features
- RAG (Retrieval-Augmented Generation) integration
- AI-powered ticket routing
- Knowledge base search
- Automated ticket classification

---

## FILES QUICK REFERENCE

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app initialization, routers |
| `config.py` | Environment variables & configuration |
| `database.py` | MongoDB connection & initialization |
| `auth/jwt_handler.py` | JWT creation, validation, refresh |
| `auth/permissions.py` | Permission checks, dependency injection |
| `routes/customer_auth.py` | Customer auth endpoints |
| `routes/engineer_auth.py` | Engineer auth endpoints |
| `schemas/*.py` | Request/response data models |
| `utils/security.py` | Password hashing, verification |
| `.env` | Environment variables |
| `mongo_setup.js` | MongoDB shell setup script |
| `init_db.py` | Python database initialization |

---

## SUPPORT & CONTACT

For issues or questions:
1. Check Troubleshooting section
2. Review API documentation at /docs
3. Check MongoDB setup in mongo_setup.js
4. Verify .env configuration

---

**Last Updated**: April 2, 2026
**Version**: 1.0.0
**Status**: Development Ready


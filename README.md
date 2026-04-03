# Support System Phase 1 - AI-Based Support Intelligence Platform

![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge)
![MongoDB](https://img.shields.io/badge/MongoDB-5.0+-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Database Setup](#database-setup)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**Support System Phase 1** is a modern, secure, and scalable customer support management platform built with FastAPI and MongoDB. It provides comprehensive authentication, authorization, and session management capabilities with a focus on security and user-friendly API design.

This is the foundation for an **AI-Based Support Intelligence System** that will incorporate Retrieval-Augmented Generation (RAG) technology in future phases to provide intelligent ticket routing, automated classification, and AI-powered support suggestions.

**Current Status**: ✅ Phase 1 Complete (Authentication & Authorization)

---

## ✨ Features

### Authentication & Authorization
- 🔐 **Secure Registration**: Customer self-registration with email validation
- 🔑 **JWT-Based Authentication**: Token-based user authentication
- 🔄 **Token Refresh**: Automatic token refresh mechanism
- 🍪 **HTTP-Only Cookies**: Secure session management with anti-CSRF protection
- 🛡️ **Password Hashing**: bcrypt with 12 salt rounds for maximum security

### User Management
- 👥 **Multi-Role Support**: Customers, Support Engineers, Admins
- ✅ **Account Activation**: Control user access with `is_active` flag
- 📊 **User Profiles**: Comprehensive user information management
- 🔔 **Session Tracking**: Last login/last seen timestamps

### API Features
- 📚 **Auto Generated Documentation**: Swagger UI at `/docs`
- ⚡ **Async Processing**: Non-blocking I/O with async/await
- ✔️ **Data Validation**: Pydantic-based request/response validation
- 🔍 **Error Handling**: Comprehensive error messages and HTTP status codes
- 🚀 **CORS Support**: Cross-origin requests enabled

### Database
- 📈 **Indexed Queries**: Optimized database performance
- 🔗 **Relationships**: Proper data relationships and constraints
- 💾 **Refresh Token Storage**: Track active sessions in database

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Server**: Uvicorn (ASGI)
- **Language**: Python 3.10+

### Database
- **Primary DB**: MongoDB 5.0+
- **Driver**: PyMongo 4.16.0+

### Authentication & Security
- **JWT**: PyJWT (token management)
- **Password Hashing**: bcrypt (12 rounds)
- **Settings**: Pydantic Settings (environment configuration)

### Development & Tools
- **Virtual Environment**: Python venv
- **Dependency Management**: pip
- **Version Control**: Git

### Testing & Documentation
- **API Docs**: Swagger UI (built-in)
- **ReDoc**: Alternative API documentation
- **Manual Testing**: Postman compatible

---

## 📁 Project Structure

```
support-system-phase1/
│
├── .venv/                              # Virtual environment
├── .git/                               # Git repository
│
├── support-system-phase1/              # Main application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI app entry point
│   │   ├── config.py                   # Configuration & settings
│   │   ├── database.py                 # MongoDB setup & connection
│   │   │
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── jwt_handler.py          # JWT token operations
│   │   │   └── permissions.py          # Authorization & permission checks
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── customer_auth.py        # Customer auth endpoints
│   │   │   └── engineer_auth.py        # Engineer auth endpoints
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── customer.py             # Customer data models
│   │   │   └── support_engineer.py     # Engineer data models
│   │   │
│   │   ├── models/
│   │   │   ├── customer.py             # Customer business logic
│   │   │   ├── role.py                 # Role definitions
│   │   │   └── support_engineer.py     # Engineer business logic
│   │   │
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── security.py             # Security utilities
│   │   │
│   │   └── .env                        # Environment variables
│   │
│   ├── init_db.py                      # Database initialization script
│   ├── mongo_setup.js                  # MongoDB setup script
│   ├── requirements.txt                # Python dependencies
│   └── .gitignore                      # Git ignore file
│
├── COMPLETE_WORKING_FLOW.md            # Complete system documentation
├── IMPLEMENTATION_DETAILS_PPT_GUIDE.md # Presentation guide
├── FIXES_APPLIED.md                    # Bug fixes documentation
├── README.md                           # This file
└── LICENSE                             # MIT License

```

---

## 🚀 Installation

### Prerequisites
- **Python 3.10+** installed
- **MongoDB 5.0+** (local or Docker)
- **Git** (for cloning)
- **pip** (Python package manager)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/support-system-phase1.git
cd support-system-phase1
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
cd support-system-phase1/app

# Install all required packages
pip install -r requirements.txt

# Or install manually:
pip install fastapi uvicorn pymongo pydantic-settings PyJWT bcrypt python-multipart
```

### Step 4: Start MongoDB

**Option A: Docker (Recommended)**
```bash
# Pull MongoDB image
docker pull mongo:latest

# Run MongoDB container


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

**Verify MongoDB Connection:**
```bash
mongosh
# Should show connection prompt
exit
```

### Step 5: Initialize Database

```bash
# Option A: Using Python script
python init_db.py

# Option B: Using MongoDB Shell
mongosh < mongo_setup.js
```

After setup, you should see:
```
✓ Database: support_system_db created
✓ Collections created
✓ Indexes created
✓ Roles inserted
✓ Admin user created
✓ Support engineers created
```

---

## ⚙️ Configuration

### Environment Variables (.env)

Located at: `support-system-phase1/app/.env`

```env
# MongoDB Configuration
MONGODB_URL
DATABASE_NAME=support_system_db

# JWT Configuration
SECRET_KEY=your-secret-key-change-in-production-must-be-32-chars-minimum
ALGORITHM=HS256

# Token Expiry (minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=5
REFRESH_TOKEN_EXPIRE_MINUTES=10

# Cookie Configuration
COOKIE_NAME=access_token
COOKIE_DOMAIN=None
COOKIE_PATH=/
COOKIE_SECURE=False          # Set to True in production (HTTPS)
COOKIE_HTTPONLY=True
COOKIE_SAMESITE=lax

# Session Configuration
SESSION_SECRET_KEY=session-secret-key-very-secret
SESSION_EXPIRE_MINUTES=60
```

### Production Recommendations

```env
# For HTTPS/Production
SECRET_KEY=your-very-long-and-secure-secret-key-minimum-32-characters
COOKIE_SECURE=True
COOKIE_SAMESITE=strict
MONGODB_URL

# Add database authentication
MONGODB_USERNAME=your_username
MONGODB_PASSWORD=your_password
```

---

## ▶️ Running the Application

### Start FastAPI Server

```bash
cd support-system-phase1/app

# Start with auto-reload (development)
uvicorn main:app --reload

# Or without auto-reload (production)
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Access the Application

- **API Root**: http://localhost:8000/
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Expected Output

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
✅ Connected to MongoDB
✅ Indexes created successfully
✅ Admin role inserted
✅ Support role inserted
INFO:     Application startup complete.
```

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Authentication Flow

#### 1. Customer Registration
```bash
POST /customer/register

# Request
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}

# Response (201 Created)
{
  "access_token": "eyJhbGciOi...",
  "refresh_token": "eyJhbGciOi...",
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

#### 2. Customer Login
```bash
POST /customer/login

# Request
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}

# Response (200 OK)
# Same as registration response
# Access token also set in HTTP-only cookie
```

#### 3. Get Current Customer
```bash
GET /customer/me

# With access token in cookie (automatic if logged in)
# Response (200 OK)
{
  "customer_id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00.000Z",
  "last_login": "2024-01-15T10:35:00.000Z"
}
```

#### 4. Refresh Access Token
```bash
POST /customer/refresh?refresh_token=eyJhbGciOi...

# Response (200 OK)
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "expires_in": 300
}
```

#### 5. Logout
```bash
POST /customer/logout

# Response (200 OK)
{
  "message": "Logged out successfully",
  "status": "success"
}
```

### Engineering Endpoints

Same as customer endpoints but at:
- `POST /engineer/login`
- `GET /engineer/me`
- `POST /engineer/logout`
- `POST /engineer/refresh`

---

## 💾 Database Setup

### Collections

| Collection | Purpose | Key Fields |
|-----------|---------|-----------|
| **customers** | Customer accounts | customer_id, email, password, is_active |
| **support_engineers** | Support staff | support_id, email, role_id, department |
| **roles** | User roles | role_id, role_name, permissions |
| **refresh_tokens** | Session management | user_id, user_type, is_active |
| **tickets** | Support tickets (future) | ticket_number, status, priority |
| **messages** | Communications (future) | ticket_id, sender_id, message |

### Default Users

**Admin:**
- Email: `admin@company.com`
- Password: `AdminPass123!`
- Support ID: 100

**Engineers:**
1. Rahul Kumar (rahul@company.com) - Technical
2. Priya Sharma (priya@company.com) - Billing
3. Amit Singh (amit@company.com) - Customer Success

### Verify Database

```bash
mongosh

# Use database
use support_system_db

# Check collections
show collections

# Count documents
db.customers.countDocuments()
db.support_engineers.countDocuments()
db.roles.countDocuments()

# List admin user
db.support_engineers.findOne({ role_id: 1 })

# List all engineers
db.support_engineers.find({ role_id: 2 })
```

---

## 🧪 Testing

### Using Swagger UI (Recommended)

1. Open http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Fill in request parameters
4. Click "Execute"
5. View response

### Using cURL

**Register:**
```bash
curl -X POST "http://localhost:8000/api/customer/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Smith",
    "email": "alice@example.com",
    "password": "AlicePass123!"
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/customer/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "AlicePass123!"
  }' \
  -v  # -v to see Set-Cookie headers
```

**Get Profile:**
```bash
curl -X GET "http://localhost:8000/api/customer/me" \
  -H "Cookie: access_token=<YOUR_TOKEN>" \
  -v
```

### Using Postman

1. Import collection (create manually or use examples above)
2. Set up environment variables:
   - `base_url`: http://localhost:8000
   - `access_token`: (auto-filled from login)
   - `refresh_token`: (auto-filled from login)
3. Test endpoints in order

### Test Scenarios

**Scenario 1: Complete Registration Flow**
```
1. Register with new email
2. Verify 201 Created response
3. Check tokens in response
4. Verify cookie is set
```

**Scenario 2: Login Flow**
```
1. Login with registered email
2. Verify 200 OK
3. Check tokens received
4. Use token to access /me
```

**Scenario 3: Token Refresh**
```
1. Login to get tokens
2. Wait for access token to expire (5 min)
3. Call refresh endpoint
4. Use new token to access /me
```

**Scenario 4: Error Cases**
```
1. Register with duplicate email → 400
2. Login with wrong password → 401
3. Access /me without token → 401
4. Use expired token → 401
```

---

## 🚀 Future Enhancements

### Phase 2: Ticket Management
- Create and manage support tickets
- Assign tickets to engineers
- Real-time ticket status tracking
- Priority levels (Low, Medium, High, Critical)
- Ticket history and comments

### Phase 3: AI Integration
- **RAG (Retrieval-Augmented Generation)**
  - Knowledge base search and indexing
  - Intelligent ticket classification
  - Automated resolution suggestions
  - Context-aware responses

- **Analytics Dashboard**
  - Support metrics and KPIs
  - Response time tracking
  - Customer satisfaction scores
  - Engineer performance analytics

### Phase 4: Advanced Features
- Real-time notifications
- Bulk email support
- Multi-language support
- Mobile app integration
- Third-party integrations

---

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest` - when added)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 Python style guide
- Use type hints
- Write docstrings for functions
- Use meaningful variable names

### Commit Messages

```
feat: Add new feature description
fix: Fix bug description
docs: Update documentation
refactor: Refactor code section
test: Add tests
```

---

## 📋 Requirements

### Runtime Requirements
- Python 3.10+
- MongoDB 5.0+
- 512 MB RAM minimum
- 100 MB disk space

### Development Requirements
- Git
- Virtual environment (venv/conda)
- Code editor (VS Code recommended)
- Postman or similar API testing tool

---

## 🔒 Security Considerations

### Implemented
✅ Password hashing (bcrypt 12 rounds)
✅ JWT token signing (HS256)
✅ Short-lived access tokens (5 minutes)
✅ HTTP-only cookies (prevents XSS)
✅ SameSite=Lax (CSRF protection)
✅ Input validation (Pydantic)
✅ CORS configured
✅ Unique email constraints

### Production Recommendations
- 🔒 Use HTTPS only (`COOKIE_SECURE=True`)
- 🔐 Use strong `SECRET_KEY` (minimum 32 characters)
- 🛡️ Enable MongoDB authentication
- 📊 Implement rate limiting
- 🔍 Add request logging
- 📝 Monitor and audit logs
- 🔄 Keep dependencies updated

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team & Acknowledgments

**Developed as**: Simprosys Intern Project - Support System Phase 1

**Project Guide**: [Your College/Organization]

**Development Date**: January - April 2024

---

## 📞 Support & Contact

For issues, questions, or suggestions:

1. Check [COMPLETE_WORKING_FLOW.md](COMPLETE_WORKING_FLOW.md) for detailed documentation
2. Review [IMPLEMENTATION_DETAILS_PPT_GUIDE.md](IMPLEMENTATION_DETAILS_PPT_GUIDE.md) for architecture
3. Check [FIXES_APPLIED.md](FIXES_APPLIED.md) if experiencing issues
4. Open an issue on GitHub

---

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [JWT Guide](https://jwt.io/)
- [RESTful API Design](https://restfulapi.net/)
- [Python bcrypt](https://pypi.org/project/bcrypt/)

---

**Status**: ✅ Production Ready for Phase 1
**Last Updated**: April 2, 2026
**Version**: 1.0.0


# from fastapi import FastAPI, HTTPException, status
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from app.database import db
# from app.routes import customer_auth, engineer_auth
# from app.utils.security import security_service
# from datetime import datetime
# from pydantic import BaseModel, EmailStr

# app = FastAPI(
#     title="Support System - Phase 1",
#     description="Customer Support System with RAG - Authentication & Authorization",
#     version="1.0.0"
# )

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# # Include routers
# app.include_router(customer_auth.router)
# app.include_router(engineer_auth.router)

# @app.on_event("startup")
# async def startup_event():
#     """Initialize database on startup"""
#     db.connect()

# @app.on_event("shutdown")
# async def shutdown_event():
#     """Close database on shutdown"""
#     db.disconnect()

# @app.get("/")
# async def root():
#     return {
#         "message": "AI-Based Support Intelligence System - Phase 1",
#         "description": "Customer Support System with Authentication & Authorization",
#         "version": "1.0.0",
#         "docs_url": "/docs",
#         "endpoints": {
#             "customer": "/api/customer/register, /api/customer/login, /api/customer/me",
#             "engineer": "/api/engineer/register, /api/engineer/login, /api/engineer/me"
#         }
#     }

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy", "service": "Support System API"}

# class AdminBootstrap(BaseModel):
#     """Bootstrap admin user creation"""
#     email: EmailStr
#     password: str
#     name: str = "System Administrator"

# @app.post("/bootstrap/admin")
# async def bootstrap_admin(admin_data: AdminBootstrap):
#     """
#     Create first admin user (only works if no admin exists)
#     This endpoint is only available for initial setup
#     """
#     database = db.get_db()
    
#     # Check if any admin already exists
#     existing_admin = database.support_engineers.find_one({"role_id": 1})
#     if existing_admin:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Admin user already exists. This endpoint is only for initial setup."
#         )
    
#     # Check if email already exists
#     existing_email = database.support_engineers.find_one({"email": admin_data.email})
#     if existing_email:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email already registered"
#         )
    
#     # Validate password strength
#     if len(admin_data.password) < 8:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Password must be at least 8 characters long"
#         )
    
#     # Hash password
#     hashed_pw = security_service.hash_password(admin_data.password)
    
#     # Create admin document
#     admin_doc = {
#         "support_id": 100,
#         "name": admin_data.name,
#         "email": admin_data.email,
#         "password": hashed_pw,
#         "role_id": 1,  # Admin role
#         "department": "Administration",
#         "is_active": True,
#         "is_online": False,
#         "last_seen": datetime.utcnow(),
#         "created_at": datetime.utcnow()
#     }
    
#     database.support_engineers.insert_one(admin_doc)
    
#     return {
#         "message": "Admin user created successfully",
#         "user": {
#             "support_id": 100,
#             "name": admin_data.name,
#             "email": admin_data.email,
#             "role_id": 1,
#             "department": "Administration",
#             "is_active": True,
#             "created_at": admin_doc["created_at"]
#         }
#     }

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import db
from routes import customer_auth, engineer_auth
from datetime import datetime

app = FastAPI(
    title="Support System - Phase 1",
    description="Customer Support System with RAG - Authentication & Authorization",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(customer_auth.router)
app.include_router(engineer_auth.router)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """Close database on shutdown"""
    db.disconnect()

@app.get("/")
async def root():
    return {
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

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Support System API",
        "timestamp": datetime.utcnow()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

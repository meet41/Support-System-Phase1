# from fastapi import APIRouter, HTTPException, status, Depends
# from datetime import timedelta, datetime
# from app.database import db
# from app.schemas.customer import (
#     CustomerRegister, 
#     CustomerLogin, 
#     TokenResponse
# )
# from app.utils.security import security_service
# from app.auth.jwt_handler import jwt_handler
# from app.auth.permissions import permission_manager
# from app.config import settings

# router = APIRouter(prefix="/api/customer", tags=["Customer Auth"])

# @router.post("/register", response_model=TokenResponse, status_code=201)
# async def register_customer(user_data: CustomerRegister):
#     """Register a new customer"""
#     database = db.get_db()
    
#     # Check if email exists
#     existing = database.customers.find_one({"email": user_data.email})
#     if existing:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email already registered"
#         )
    
#     # Get next customer_id
#     last_customer = database.customers.find_one(
#         sort=[("customer_id", -1)]
#     )
#     next_id = (last_customer["customer_id"] + 1) if last_customer else 1
    
#     # Hash password
#     hashed_pw = security_service.hash_password(user_data.password)
    
#     # Create customer document
#     customer_doc = {
#         "customer_id": next_id,
#         "name": user_data.name,
#         "email": user_data.email,
#         "password": hashed_pw,
#         "is_active": True,
#         "created_at": datetime.utcnow(),
#         "last_login": None
#     }
    
#     result = database.customers.insert_one(customer_doc)
    
#     # Create tokens
#     access_token = jwt_handler.create_access_token(
#         data={"sub": next_id, "type": "customer", "email": user_data.email}
#     )
#     refresh_token = jwt_handler.create_refresh_token(
#         data={"sub": next_id, "type": "customer"}
#     )
    
#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "token_type": "bearer",
#         "user": {
#             "customer_id": next_id,
#             "name": user_data.name,
#             "email": user_data.email,
#             "is_active": True,
#             "created_at": customer_doc["created_at"],
#             "last_login": None
#         }
#     }

# @router.post("/login", response_model=TokenResponse)
# async def login_customer(credentials: CustomerLogin):
#     """Login customer"""
#     database = db.get_db()
    
#     customer = database.customers.find_one({"email": credentials.email})
    
#     if not customer or not security_service.verify_password(
#         credentials.password, 
#         customer["password"]
#     ):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid email or password"
#         )
    
#     if not customer.get("is_active"):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Customer account is inactive"
#         )
    
#     # Update last_login
#     database.customers.update_one(
#         {"customer_id": customer["customer_id"]},
#         {"$set": {"last_login": datetime.utcnow()}}
#     )
    
#     access_token = jwt_handler.create_access_token(
#         data={"sub": customer["customer_id"], "type": "customer", "email": customer["email"]}
#     )
#     refresh_token = jwt_handler.create_refresh_token(
#         data={"sub": customer["customer_id"], "type": "customer"}
#     )
    
#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "token_type": "bearer",
#         "user": {
#             "customer_id": customer["customer_id"],
#             "name": customer["name"],
#             "email": customer["email"],
#             "is_active": customer["is_active"],
#             "created_at": customer["created_at"],
#             "last_login": datetime.utcnow()
#         }
#     }

# @router.get("/me")
# async def get_current_customer(current_user=Depends(permission_manager.get_current_customer)):
#     """Get current logged-in customer"""
#     database = db.get_db()
#     customer = database.customers.find_one(
#         {"customer_id": current_user["customer_id"]}
#     )
    
#     if not customer:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Customer not found"
#         )
    
#     return {
#         "customer_id": customer["customer_id"],
#         "name": customer["name"],
#         "email": customer["email"],
#         "is_active": customer["is_active"],
#         "created_at": customer["created_at"],
#         "last_login": customer["last_login"]
#     }



from fastapi import APIRouter, HTTPException, status, Depends, Response, Request
from datetime import datetime
from pydantic import BaseModel
from database import db
from schemas.customer import (
    CustomerRegister, 
    CustomerLogin, 
    TokenResponse,
    CustomerResponse
)
from utils.security import security_service
from auth.jwt_handler import jwt_handler
from auth.permissions import permission_manager
from config import settings


class RefreshTokenRequest(BaseModel):
    """Request body for refresh token endpoint (Issue #1)"""
    refresh_token: str


router = APIRouter(prefix="/api/customer", tags=["Customer Auth"])

# Dependency functions for proper FastAPI injection
async def get_current_customer_dep(request: Request):
    """Dependency to get current customer"""
    return await permission_manager.get_current_customer(request)

async def check_customer_active_dep(request: Request):
    """Dependency to check customer is active"""
    current_customer = await permission_manager.get_current_customer(request)
    return await permission_manager.check_customer_active(current_customer)

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register_customer(user_data: CustomerRegister, response: Response):
    """
    Register a new customer
    - Stores access token in HTTP-only cookie (5 min)
    - Stores refresh token in database (10 min)
    """
    database = db.get_db()
    
    # Check if email exists
    existing = database.customers.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Get next customer_id
    last_customer = database.customers.find_one(sort=[("customer_id", -1)])
    next_id = (last_customer["customer_id"] + 1) if last_customer else 1
    
    # Hash password
    hashed_pw = security_service.hash_password(user_data.password)
    
    # Create customer document
    customer_doc = {
        "customer_id": next_id,
        "name": user_data.name,
        "email": user_data.email,
        "password": hashed_pw,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "last_login": None
    }
    
    database.customers.insert_one(customer_doc)
    
    # Create tokens
    access_token = jwt_handler.create_access_token(
        data={
            "sub": next_id, 
            "user_type": "customer", 
            "email": user_data.email
        }
    )
    
    refresh_token = jwt_handler.create_refresh_token(
        data={
            "sub": next_id, 
            "user_type": "customer", 
            "email": user_data.email
        }
    )
    
    # Store refresh token in database (Issue #9: expires_at removed – JWT exp is the source of truth)
    refresh_token_doc = {
        "user_id": next_id,
        "user_type": "customer",
        "token": refresh_token,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "revoked_at": None
    }
    database.refresh_tokens.insert_one(refresh_token_doc)
    
    # Set access token in HTTP-only cookie
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path=settings.COOKIE_PATH,
        domain=settings.COOKIE_DOMAIN,
        secure=settings.COOKIE_SECURE,
        httponly=settings.COOKIE_HTTPONLY,
        samesite=settings.COOKIE_SAMESITE
    )

    # Issue #2: store refresh token in HttpOnly cookie; do not expose it in the JSON body
    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        path=settings.COOKIE_PATH,
        domain=settings.COOKIE_DOMAIN,
        secure=settings.COOKIE_SECURE,
        httponly=True,
        samesite=settings.COOKIE_SAMESITE
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "customer_id": next_id,
            "name": user_data.name,
            "email": user_data.email,
            "is_active": True,
            "created_at": customer_doc["created_at"],
            "last_login": None
        }
    }

@router.post("/login", response_model=TokenResponse)
async def login_customer(credentials: CustomerLogin, response: Response):
    """
    Login customer
    - Stores access token in HTTP-only cookie (5 min)
    - Stores refresh token in database (10 min)
    """
    database = db.get_db()
    
    customer = database.customers.find_one({"email": credentials.email})
    
    if not customer or not security_service.verify_password(
        credentials.password, 
        customer["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not customer.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer account is inactive"
        )
    
    # Update last_login
    database.customers.update_one(
        {"customer_id": customer["customer_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )
    
    # Create tokens
    access_token = jwt_handler.create_access_token(
        data={
            "sub": customer["customer_id"], 
            "user_type": "customer", 
            "email": customer["email"]
        }
    )
    
    refresh_token = jwt_handler.create_refresh_token(
        data={
            "sub": customer["customer_id"], 
            "user_type": "customer", 
            "email": customer["email"]
        }
    )
    
    # Store refresh token in database (Issue #9: expires_at removed – JWT exp is the source of truth)
    refresh_token_doc = {
        "user_id": customer["customer_id"],
        "user_type": "customer",
        "token": refresh_token,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "revoked_at": None
    }
    database.refresh_tokens.insert_one(refresh_token_doc)
    
    # Set access token in HTTP-only cookie
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path=settings.COOKIE_PATH,
        domain=settings.COOKIE_DOMAIN,
        secure=settings.COOKIE_SECURE,
        httponly=settings.COOKIE_HTTPONLY,
        samesite=settings.COOKIE_SAMESITE
    )

    # Issue #2: store refresh token in HttpOnly cookie; do not expose it in the JSON body
    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        path=settings.COOKIE_PATH,
        domain=settings.COOKIE_DOMAIN,
        secure=settings.COOKIE_SECURE,
        httponly=True,
        samesite=settings.COOKIE_SAMESITE
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "customer_id": customer["customer_id"],
            "name": customer["name"],
            "email": customer["email"],
            "is_active": customer["is_active"],
            "created_at": customer["created_at"],
            "last_login": datetime.utcnow()
        }
    }

@router.get("/me", response_model=CustomerResponse)
async def get_current_customer(
    current_user=Depends(check_customer_active_dep)
):
    """Get current logged-in customer info"""
    database = db.get_db()
    customer = database.customers.find_one(
        {"customer_id": current_user["customer_id"]}
    )
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return {
        "customer_id": customer["customer_id"],
        "name": customer["name"],
        "email": customer["email"],
        "is_active": customer["is_active"],
        "created_at": customer["created_at"],
        "last_login": customer["last_login"]
    }

@router.post("/logout")
async def logout_customer(
    request: Request,
    response: Response,
    current_user=Depends(get_current_customer_dep)
):
    """
    Logout customer
    - Revoke refresh token
    - Clear access token cookie
    """
    database = db.get_db()
    
    # Revoke refresh tokens
    database.refresh_tokens.update_many(
        {
            "user_id": current_user["customer_id"],
            "user_type": "customer",
            "is_active": True
        },
        {
            "$set": {
                "is_active": False,
                "revoked_at": datetime.utcnow()
            }
        }
    )
    
    # Clear access token cookie
    response.delete_cookie(
        key=settings.COOKIE_NAME,
        path=settings.COOKIE_PATH,
        domain=settings.COOKIE_DOMAIN
    )

    # Issue #2: also clear the refresh token cookie
    response.delete_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        path=settings.COOKIE_PATH,
        domain=settings.COOKIE_DOMAIN
    )
    
    return {
        "message": "Logged out successfully",
        "status": "success"
    }

@router.post("/refresh")
async def refresh_access_token(
    request: Request,
    response: Response,
    refresh_request: RefreshTokenRequest = None
):
    """
    Refresh access token using the refresh token.
    - Reads refresh token from HttpOnly cookie (browser) or request body (API clients)
    - Issue #1:  token is never passed as a URL query parameter
    - Issue #3:  implements token rotation (old token invalidated, new one issued)
    - Issue #10: validates user_type == 'customer'
    """
    database = db.get_db()

    # Issue #1 & #2: prefer the HttpOnly cookie; fall back to the request body
    refresh_token = request.cookies.get(settings.REFRESH_COOKIE_NAME)
    if not refresh_token and refresh_request:
        refresh_token = refresh_request.refresh_token

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not provided"
        )

    # Verify refresh token signature and expiry
    payload = jwt_handler.verify_refresh_token(refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    user_id = payload.get("sub")
    user_type = payload.get("user_type")

    # Issue #10: enforce user_type on this endpoint
    if user_type != "customer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type. Expected 'customer' but got '{user_type}'"
        )

    # Issue #5: validate sub claim
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token - customer ID (sub) not found"
        )

    # Check if token is still active in database
    stored_token = database.refresh_tokens.find_one({
        "user_id": user_id,
        "user_type": "customer",
        "token": refresh_token,
        "is_active": True
    })

    if not stored_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is revoked or invalid"
        )

    # Issue #3: token rotation – invalidate the old token before issuing a new one
    database.refresh_tokens.update_one(
        {"_id": stored_token["_id"]},
        {"$set": {"is_active": False, "revoked_at": datetime.utcnow()}}
    )

    # Create new tokens
    new_access_token = jwt_handler.create_access_token(
        data={
            "sub": user_id,
            "user_type": "customer",
            "email": payload.get("email")
        }
    )
    new_refresh_token = jwt_handler.create_refresh_token(
        data={
            "sub": user_id,
            "user_type": "customer",
            "email": payload.get("email")
        }
    )

    # Persist new refresh token (Issue #9: no expires_at – JWT exp is the source of truth)
    database.refresh_tokens.insert_one({
        "user_id": user_id,
        "user_type": "customer",
        "token": new_refresh_token,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "revoked_at": None
    })

    # Set new access token cookie
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=new_access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path=settings.COOKIE_PATH,
        domain=settings.COOKIE_DOMAIN,
        secure=settings.COOKIE_SECURE,
        httponly=settings.COOKIE_HTTPONLY,
        samesite=settings.COOKIE_SAMESITE
    )

    # Issue #2: update refresh token cookie (HttpOnly, never exposed to JS)
    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=new_refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        path=settings.COOKIE_PATH,
        domain=settings.COOKIE_DOMAIN,
        secure=settings.COOKIE_SECURE,
        httponly=True,
        samesite=settings.COOKIE_SAMESITE
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

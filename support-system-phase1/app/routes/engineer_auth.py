# from fastapi import APIRouter, HTTPException, status, Depends
# from datetime import timedelta, datetime
# from app.database import db
# from app.schemas.support_engineer import (
#     EngineerRegister, 
#     EngineerLogin, 
#     EngineerTokenResponse
# )
# from app.utils.security import security_service
# from app.auth.jwt_handler import jwt_handler
# from app.auth.permissions import permission_manager, get_current_admin
# from app.config import settings

# router = APIRouter(prefix="/api/engineer", tags=["Engineer Auth"])

# @router.post("/register", response_model=EngineerTokenResponse, status_code=201)
# async def register_engineer(
#     engineer_data: EngineerRegister,
#     current_user=Depends(get_current_admin)
# ):
#     """Register new support engineer (admin only)"""
#     database = db.get_db()
    
#     # Check if email exists
#     existing = database.support_engineers.find_one({"email": engineer_data.email})
#     if existing:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email already registered"
#         )
    
#     # Get next support_id
#     last_engineer = database.support_engineers.find_one(
#         sort=[("support_id", -1)]
#     )
#     next_id = (last_engineer["support_id"] + 1) if last_engineer else 101
    
#     # Hash password
#     hashed_pw = security_service.hash_password(engineer_data.password)
    
#     # Create engineer document (default role 2 = support)
#     engineer_doc = {
#         "support_id": next_id,
#         "name": engineer_data.name,
#         "email": engineer_data.email,
#         "password": hashed_pw,
#         "role_id": 2,  # Default support role
#         "department": engineer_data.department,
#         "is_active": True,
#         "is_online": False,
#         "last_seen": datetime.utcnow(),
#         "created_at": datetime.utcnow()
#     }
    
#     database.support_engineers.insert_one(engineer_doc)
    
#     access_token = jwt_handler.create_access_token(
#         data={"sub": next_id, "type": "engineer", "email": engineer_data.email}
#     )
#     refresh_token = jwt_handler.create_refresh_token(
#         data={"sub": next_id, "type": "engineer"}
#     )
    
#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "token_type": "bearer",
#         "user": {
#             "support_id": next_id,
#             "name": engineer_data.name,
#             "email": engineer_data.email,
#             "role_id": 2,
#             "department": engineer_data.department,
#             "is_active": True,
#             "is_online": False,
#             "created_at": engineer_doc["created_at"],
#             "last_seen": engineer_doc["last_seen"]
#         }
#     }

# @router.post("/login", response_model=EngineerTokenResponse)
# async def login_engineer(credentials: EngineerLogin):
#     """Login support engineer"""
#     database = db.get_db()
    
#     engineer = database.support_engineers.find_one({"email": credentials.email})
    
#     if not engineer or not security_service.verify_password(
#         credentials.password, 
#         engineer["password"]
#     ):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid email or password"
#         )
    
#     if not engineer.get("is_active"):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Engineer account is inactive"
#         )
    
#     # Update last_seen and is_online
#     database.support_engineers.update_one(
#         {"support_id": engineer["support_id"]},
#         {
#             "$set": {
#                 "last_seen": datetime.utcnow(),
#                 "is_online": True
#             }
#         }
#     )
    
#     access_token = jwt_handler.create_access_token(
#         data={"sub": engineer["support_id"], "type": "engineer", "email": engineer["email"]}
#     )
#     refresh_token = jwt_handler.create_refresh_token(
#         data={"sub": engineer["support_id"], "type": "engineer"}
#     )
    
#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "token_type": "bearer",
#         "user": {
#             "support_id": engineer["support_id"],
#             "name": engineer["name"],
#             "email": engineer["email"],
#             "role_id": engineer["role_id"],
#             "department": engineer["department"],
#             "is_active": engineer["is_active"],
#             "is_online": True,
#             "created_at": engineer["created_at"],
#             "last_seen": datetime.utcnow()
#         }
#     }

# @router.get("/me")
# async def get_current_engineer(current_user=Depends(permission_manager.check_engineer_active)):
#     """Get current logged-in engineer"""
#     database = db.get_db()
#     engineer = database.support_engineers.find_one(
#         {"support_id": current_user["engineer_id"]}
#     )
    
#     if not engineer:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Engineer not found"
#         )
    
#     return {
#         "support_id": engineer["support_id"],
#         "name": engineer["name"],
#         "email": engineer["email"],
#         "role_id": engineer["role_id"],
#         "department": engineer["department"],
#         "is_active": engineer["is_active"],
#         "is_online": engineer["is_online"],
#         "created_at": engineer["created_at"],
#         "last_seen": engineer["last_seen"]
#     }



from fastapi import APIRouter, HTTPException, status, Depends, Response, Request
from datetime import datetime
from pydantic import BaseModel
from database import db
from schemas.support_engineer import (
    EngineerLogin, 
    EngineerTokenResponse,
    EngineerResponse
)
from utils.security import security_service
from auth.jwt_handler import jwt_handler
from auth.permissions import permission_manager
from config import settings


class RefreshTokenRequest(BaseModel):
    """Request body for refresh token endpoint (Issue #1)"""
    refresh_token: str


router = APIRouter(prefix="/api/engineer", tags=["Engineer Auth"])

# Dependency functions for proper FastAPI injection
async def get_current_engineer_dep(request: Request):
    """Dependency to get current engineer"""
    return await permission_manager.get_current_engineer(request)

async def check_engineer_active_dep(request: Request):
    """Dependency to check engineer is active"""
    current_engineer = await permission_manager.get_current_engineer(request)
    return await permission_manager.check_engineer_active(current_engineer)

@router.post("/login", response_model=EngineerTokenResponse)
async def login_engineer(credentials: EngineerLogin, response: Response):
    """
    Login support engineer
    - Stores access token in HTTP-only cookie (5 min)
    - Stores refresh token in database (10 min)
    """
    database = db.get_db()
    
    engineer = database.support_engineers.find_one({"email": credentials.email})
    
    if not engineer or not security_service.verify_password(
        credentials.password, 
        engineer["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not engineer.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Engineer account is inactive"
        )
    
    # Update last_seen and is_online
    database.support_engineers.update_one(
        {"support_id": engineer["support_id"]},
        {
            "$set": {
                "last_seen": datetime.utcnow(),
                "is_online": True
            }
        }
    )
    
    # Create tokens
    access_token = jwt_handler.create_access_token(
        data={
            "sub": engineer["support_id"], 
            "user_type": "engineer", 
            "email": engineer["email"],
            "role_id": engineer["role_id"]
        }
    )
    
    refresh_token = jwt_handler.create_refresh_token(
        data={
            "sub": engineer["support_id"], 
            "user_type": "engineer", 
            "email": engineer["email"]
        }
    )
    
    # Store refresh token in database (Issue #9: expires_at removed – JWT exp is the source of truth)
    refresh_token_doc = {
        "user_id": engineer["support_id"],
        "user_type": "engineer",
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
            "support_id": engineer["support_id"],
            "name": engineer["name"],
            "email": engineer["email"],
            "role_id": engineer["role_id"],
            "department": engineer["department"],
            "is_active": engineer["is_active"],
            "is_online": True,
            "created_at": engineer["created_at"],
            "last_seen": datetime.utcnow()
        }
    }

@router.get("/me", response_model=EngineerResponse)
async def get_current_engineer(
    current_user=Depends(check_engineer_active_dep)
):
    """Get current logged-in engineer info"""
    database = db.get_db()
    engineer = database.support_engineers.find_one(
        {"support_id": current_user["engineer_id"]}
    )
    
    if not engineer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engineer not found"
        )
    
    return {
        "support_id": engineer["support_id"],
        "name": engineer["name"],
        "email": engineer["email"],
        "role_id": engineer["role_id"],
        "department": engineer["department"],
        "is_active": engineer["is_active"],
        "is_online": engineer["is_online"],
        "created_at": engineer["created_at"],
        "last_seen": engineer["last_seen"]
    }

@router.post("/logout")
async def logout_engineer(
    request: Request,
    response: Response,
    current_user=Depends(get_current_engineer_dep)
):
    """
    Logout engineer
    - Set is_online to false
    - Revoke refresh tokens
    - Clear access token cookie
    """
    database = db.get_db()
    
    # Update is_online status
    database.support_engineers.update_one(
        {"support_id": current_user["engineer_id"]},
        {"$set": {"is_online": False, "last_seen": datetime.utcnow()}}
    )
    
    # Revoke refresh tokens
    database.refresh_tokens.update_many(
        {
            "user_id": current_user["engineer_id"],
            "user_type": "engineer",
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
    - Issue #10: validates user_type == 'engineer'
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
    if user_type != "engineer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type. Expected 'engineer' but got '{user_type}'"
        )

    # Issue #5: validate sub claim
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token - engineer ID (sub) not found"
        )

    # Check if token is still active in database
    stored_token = database.refresh_tokens.find_one({
        "user_id": user_id,
        "user_type": "engineer",
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
            "user_type": "engineer",
            "email": payload.get("email")
        }
    )
    new_refresh_token = jwt_handler.create_refresh_token(
        data={
            "sub": user_id,
            "user_type": "engineer",
            "email": payload.get("email")
        }
    )

    # Persist new refresh token (Issue #9: no expires_at – JWT exp is the source of truth)
    database.refresh_tokens.insert_one({
        "user_id": user_id,
        "user_type": "engineer",
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

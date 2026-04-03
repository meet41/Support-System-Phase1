# from fastapi import HTTPException, Depends, status, Header
# from app.auth.jwt_handler import jwt_handler
# from app.database import db
# from typing import Optional, Dict, Any

# async def extract_token_from_header(authorization: Optional[str] = Header(None)) -> str:
#     """Extract JWT token from Authorization header"""
#     if not authorization:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Missing Authorization header. Add header: Authorization: Bearer {token}",
#             headers={"WWW-Authenticate": "Bearer"}
#         )
    
#     # Authorization header should be: "Bearer {token}"
#     parts = authorization.split(" ")
    
#     if len(parts) != 2:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid Authorization header format. Use: Bearer {token}",
#             headers={"WWW-Authenticate": "Bearer"}
#         )
    
#     scheme, token = parts
    
#     if scheme.lower() != "bearer":
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=f"Invalid authentication scheme '{scheme}'. Expected 'Bearer'",
#             headers={"WWW-Authenticate": "Bearer"}
#         )
    
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Empty token provided",
#             headers={"WWW-Authenticate": "Bearer"}
#         )
    
#     return token

# class PermissionManager:
#     """Manage user permissions and authorization"""
    
#     @staticmethod
#     async def get_current_customer(authorization: Optional[str] = Header(None)):
#         """Extract and validate customer JWT token"""
#         # Extract token from Authorization header
#         token = await extract_token_from_header(authorization)
        
#         # Decode token
#         payload = jwt_handler.decode_token(token)
        
#         if not payload:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid or expired token. Token may have expired (tokens expire after 30 minutes). Please login again.",
#                 headers={"WWW-Authenticate": "Bearer"}
#             )
        
#         # Validate token type
#         if payload.get("type") != "customer":
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail=f"Invalid token type. Expected 'customer' but got '{payload.get('type')}'. Use /api/customer/login endpoint.",
#                 headers={"WWW-Authenticate": "Bearer"}
#             )
        
#         # Extract customer ID
#         customer_id = payload.get("sub")
#         if not customer_id:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid token - customer ID (sub) not found in token payload",
#                 headers={"WWW-Authenticate": "Bearer"}
#             )
        
#         return {"customer_id": customer_id, "payload": payload}

#     @staticmethod
#     async def get_current_engineer(authorization: Optional[str] = Header(None)):
#         """Extract and validate support engineer JWT token"""
#         # Extract token from Authorization header
#         token = await extract_token_from_header(authorization)
        
#         # Decode token
#         payload = jwt_handler.decode_token(token)
        
#         if not payload:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid or expired token. Token may have expired (tokens expire after 30 minutes). Please login again.",
#                 headers={"WWW-Authenticate": "Bearer"}
#             )
        
#         # Validate token type
#         if payload.get("type") != "engineer":
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail=f"Invalid token type. Expected 'engineer' but got '{payload.get('type')}'. Use /api/engineer/login endpoint.",
#                 headers={"WWW-Authenticate": "Bearer"}
#             )
        
#         # Extract engineer ID
#         engineer_id = payload.get("sub")
#         if not engineer_id:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid token - engineer ID (sub) not found in token payload",
#                 headers={"WWW-Authenticate": "Bearer"}
#             )
        
#         return {"engineer_id": engineer_id, "payload": payload}

#     @staticmethod
#     async def check_admin(current_engineer: dict):
#         """Check if engineer is admin"""
#         try:
#             database = db.get_db()
#             engineer_id = current_engineer.get("engineer_id")
            
#             if not engineer_id:
#                 raise HTTPException(
#                     status_code=status.HTTP_401_UNAUTHORIZED,
#                     detail="Engineer ID not found in token"
#                 )
            
#             engineer = database.support_engineers.find_one(
#                 {"support_id": engineer_id}
#             )
            
#             if not engineer:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND,
#                     detail=f"Engineer with ID {engineer_id} not found in database"
#                 )
            
#             role_id = engineer.get("role_id")
#             if role_id != 1:
#                 raise HTTPException(
#                     status_code=status.HTTP_403_FORBIDDEN,
#                     detail=f"Admin access required. Your role_id is {role_id}, admin role_id is 1"
#                 )
            
#             return current_engineer
#         except HTTPException:
#             raise
#         except Exception as e:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"Error checking admin status: {str(e)}"
#             )

#     @staticmethod
#     async def check_engineer_active(current_engineer: dict):
#         """Check if engineer account is active"""
#         database = db.get_db()
#         engineer = database.support_engineers.find_one(
#             {"support_id": current_engineer["engineer_id"]}
#         )
        
#         if not engineer:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Engineer not found"
#             )
        
#         if not engineer.get("is_active"):
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Engineer account is inactive"
#             )
        
#         return current_engineer

# permission_manager = PermissionManager()

# # Wrapper functions for chained dependencies
# async def get_current_admin(
#     authorization: Optional[str] = Header(None)
# ):
#     """Get current engineer and verify admin status"""
#     # Get the engineer (this validates token and type)
#     current_engineer = await permission_manager.get_current_engineer(authorization)
#     # Check if admin
#     return await permission_manager.check_admin(current_engineer)

# async def get_current_active_engineer(
#     authorization: Optional[str] = Header(None)
# ):
#     """Get current engineer and verify active status"""
#     # Get the engineer (this validates token and type)
#     current_engineer = await permission_manager.get_current_engineer(authorization)
#     # Check if active
#     return await permission_manager.check_engineer_active(current_engineer)




from fastapi import HTTPException, Depends, status, Request
from auth.jwt_handler import jwt_handler
from database import db
from config import settings
from typing import Optional, Dict, Any

class PermissionManager:
    """Manage user permissions and authorization with proper JWT verification"""
    
    def extract_token_from_cookies(self, request: Request) -> Optional[str]:
        """Extract access token from cookies"""
        return request.cookies.get(settings.COOKIE_NAME)

    async def get_current_customer(self, request: Request) -> Dict[str, Any]:
        """Extract and validate customer from cookies"""
        token = self.extract_token_from_cookies(request)
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token not found in cookies",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Verify access token (also checks type == "access" internally)
        payload = jwt_handler.verify_access_token(token)
        
        # Issue #6: verify_access_token already validates type; one check is enough
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired access token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        user_type = payload.get("user_type")
        if user_type != "customer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type for customer",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        customer_id = payload.get("sub")
        # Issue #5: validate sub claim is present
        if not customer_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token - customer ID (sub) not found in token payload",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return {"customer_id": customer_id, "payload": payload}

    async def get_current_engineer(self, request: Request) -> Dict[str, Any]:
        """Extract and validate engineer from cookies"""
        token = self.extract_token_from_cookies(request)
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token not found in cookies",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Verify access token (also checks type == "access" internally)
        payload = jwt_handler.verify_access_token(token)
        
        # Issue #6: verify_access_token already validates type; one check is enough
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired access token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        user_type = payload.get("user_type")
        if user_type != "engineer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type for engineer",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        engineer_id = payload.get("sub")
        # Issue #5: validate sub claim is present
        if not engineer_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token - engineer ID (sub) not found in token payload",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return {"engineer_id": engineer_id, "payload": payload}

    async def check_admin(self, current_engineer: dict):
        """Check if engineer is admin"""
        database = db.get_db()
        engineer = database.support_engineers.find_one(
            {"support_id": current_engineer["engineer_id"]}
        )
        
        if not engineer or engineer.get("role_id") != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        return current_engineer

    async def check_engineer_active(self, current_engineer: dict):
        """Check if engineer account is active"""
        database = db.get_db()
        engineer = database.support_engineers.find_one(
            {"support_id": current_engineer["engineer_id"]}
        )
        
        if not engineer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Engineer not found"
            )
        
        if not engineer.get("is_active"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Engineer account is inactive"
            )
        
        return current_engineer

    async def check_customer_active(self, current_customer: dict):
        """Check if customer account is active"""
        database = db.get_db()
        customer = database.customers.find_one(
            {"customer_id": current_customer["customer_id"]}
        )
        
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        if not customer.get("is_active"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Customer account is inactive"
            )
        
        return current_customer

permission_manager = PermissionManager()

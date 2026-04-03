# import jwt
# from datetime import datetime, timedelta
# from typing import Optional, Dict, Any
# from app.config import settings

# class JWTHandler:
#     """Handle JWT token creation and validation"""
    
#     @staticmethod
#     def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
#         """Create JWT access token"""
#         to_encode = data.copy()
        
#         if expires_delta:
#             expire = datetime.utcnow() + expires_delta
#         else:
#             expire = datetime.utcnow() + timedelta(
#                 minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
#             )
        
#         # Convert datetime to unix timestamp (seconds since epoch)
#         expire_timestamp = int(expire.timestamp())
#         iat_timestamp = int(datetime.utcnow().timestamp())
        
#         to_encode.update({"exp": expire_timestamp, "iat": iat_timestamp})
#         encoded_jwt = jwt.encode(
#             to_encode, 
#             settings.SECRET_KEY, 
#             algorithm=settings.ALGORITHM
#         )
#         return encoded_jwt

#     @staticmethod
#     def create_refresh_token(data: dict) -> str:
#         """Create JWT refresh token with longer expiry"""
#         to_encode = data.copy()
#         to_encode["type"] = "refresh"  # Override type to refresh
        
#         expire = datetime.utcnow() + timedelta(
#             days=settings.REFRESH_TOKEN_EXPIRE_DAYS
#         )
        
#         # Convert datetime to unix timestamp (seconds since epoch)
#         expire_timestamp = int(expire.timestamp())
#         iat_timestamp = int(datetime.utcnow().timestamp())
        
#         to_encode.update({"exp": expire_timestamp, "iat": iat_timestamp})
#         encoded_jwt = jwt.encode(
#             to_encode, 
#             settings.SECRET_KEY, 
#             algorithm=settings.ALGORITHM
#         )
#         return encoded_jwt

#     @staticmethod
#     def decode_token(token: str) -> Optional[Dict[str, Any]]:
#         """Decode and validate JWT token"""
#         try:
#             payload = jwt.decode(
#                 token, 
#                 settings.SECRET_KEY, 
#                 algorithms=[settings.ALGORITHM]
#             )
#             return payload
#         except jwt.ExpiredSignatureError:
#             return None
#         except jwt.InvalidTokenError:
#             return None

# jwt_handler = JWTHandler()




import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from config import settings

class JWTHandler:
    """Handle JWT token creation and validation"""
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token (short-lived, stored in cookie)"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        
        to_encode.update({
            "exp": int(expire.timestamp()), 
            "iat": int(datetime.utcnow().timestamp()),
            "type": "access"
        })
        
        # Issue #4: use a dedicated secret for access tokens
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.ACCESS_TOKEN_SECRET, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """Create JWT refresh token (long-lived, stored in DB)"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({
            "exp": int(expire.timestamp()), 
            "iat": int(datetime.utcnow().timestamp()),
            "type": "refresh"
        })
        
        # Issue #4: use a dedicated secret for refresh tokens
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.REFRESH_TOKEN_SECRET, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """Decode and validate JWT token using the correct per-type secret"""
        try:
            # Issue #4: select secret based on token type
            secret = (
                settings.ACCESS_TOKEN_SECRET
                if token_type == "access"
                else settings.REFRESH_TOKEN_SECRET
            )
            payload = jwt.decode(
                token, 
                secret, 
                algorithms=[settings.ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify access token specifically"""
        payload = JWTHandler.decode_token(token, token_type="access")
        if payload and payload.get("type") == "access":
            return payload
        return None

    @staticmethod
    def verify_refresh_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify refresh token specifically"""
        payload = JWTHandler.decode_token(token, token_type="refresh")
        if payload and payload.get("type") == "refresh":
            return payload
        return None

jwt_handler = JWTHandler()

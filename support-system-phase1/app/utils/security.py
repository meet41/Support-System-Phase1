import bcrypt
from typing import Tuple

class SecurityService:
    """Handle password hashing and verification"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt with 12 rounds"""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify plain password against bcrypt hash"""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False

security_service = SecurityService()
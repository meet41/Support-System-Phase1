# from pydantic import BaseModel, EmailStr, Field
# from typing import Optional
# from datetime import datetime

# class EngineerRegister(BaseModel):
#     """Support engineer registration schema"""
#     name: str = Field(..., min_length=2, max_length=100)
#     email: EmailStr
#     password: str = Field(..., min_length=8, max_length=100)
#     department: str = Field(..., min_length=2, max_length=50)

# class EngineerLogin(BaseModel):
#     """Support engineer login schema"""
#     email: EmailStr
#     password: str

# class EngineerResponse(BaseModel):
#     """Support engineer response schema"""
#     support_id: Optional[int]
#     name: str
#     email: str
#     role_id: int
#     department: str
#     is_active: bool
#     is_online: bool
#     created_at: datetime
#     last_seen: Optional[datetime]

#     class Config:
#         from_attributes = True

# class EngineerTokenResponse(BaseModel):
#     """Engineer token response schema"""
#     access_token: str
#     refresh_token: Optional[str] = None
#     token_type: str = "bearer"
#     user: EngineerResponse



from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class EngineerLogin(BaseModel):
    """Support engineer login schema"""
    email: EmailStr
    password: str

class EngineerResponse(BaseModel):
    """Support engineer response schema"""
    support_id: Optional[int]
    name: str
    email: str
    role_id: int
    department: str
    is_active: bool
    is_online: bool
    created_at: datetime
    last_seen: Optional[datetime]

    class Config:
        from_attributes = True

class EngineerTokenResponse(BaseModel):
    """Engineer token response schema"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    user: EngineerResponse

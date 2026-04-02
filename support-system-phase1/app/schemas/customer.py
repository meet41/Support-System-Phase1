# from pydantic import BaseModel, EmailStr, Field
# from typing import Optional
# from datetime import datetime

# class CustomerRegister(BaseModel):
#     """Customer registration schema"""
#     name: str = Field(..., min_length=2, max_length=100)
#     email: EmailStr
#     password: str = Field(..., min_length=8, max_length=100)

# class CustomerLogin(BaseModel):
#     """Customer login schema"""
#     email: EmailStr
#     password: str

# class CustomerResponse(BaseModel):
#     """Customer response schema"""
#     customer_id: Optional[int]
#     name: str
#     email: str
#     is_active: bool
#     created_at: datetime
#     last_login: Optional[datetime]

#     class Config:
#         from_attributes = True

# class TokenResponse(BaseModel):
#     """Token response schema"""
#     access_token: str
#     refresh_token: Optional[str] = None
#     token_type: str = "bearer"
#     user: CustomerResponse



from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class CustomerRegister(BaseModel):
    """Customer registration schema"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)

class CustomerLogin(BaseModel):
    """Customer login schema"""
    email: EmailStr
    password: str

class CustomerResponse(BaseModel):
    """Customer response schema"""
    customer_id: Optional[int]
    name: str
    email: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    user: CustomerResponse

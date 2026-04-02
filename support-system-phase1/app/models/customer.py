from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

class CustomerDB(BaseModel):
    """Customer database model"""
    customer_id: Optional[int] = None
    name: str
    email: EmailStr
    password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True
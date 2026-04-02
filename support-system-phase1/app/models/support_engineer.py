from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class SupportEngineerDB(BaseModel):
    """Support engineer database model"""
    support_id: Optional[int] = None
    name: str
    email: EmailStr
    password: str
    role_id: int
    department: str
    is_active: bool = True
    is_online: bool = False
    last_seen: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
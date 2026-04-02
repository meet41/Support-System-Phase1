from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class RoleDB(BaseModel):
    """Role database model"""
    role_id: int
    role_name: str
    permissions: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
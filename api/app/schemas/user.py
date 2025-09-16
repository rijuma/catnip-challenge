from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    uuid: Optional[UUID]
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str]
    address: Optional[str]


class UserRead(BaseModel):
    uuid: UUID
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str]
    address: Optional[str]
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

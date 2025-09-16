from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str]
    address: Optional[str]

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
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

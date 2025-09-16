from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class AccountCreate(BaseModel):
    uuid: Optional[UUID]
    user_uuid: UUID
    label: str
    balance: Decimal


class AccountRead(BaseModel):
    uuid: UUID
    user_uuid: UUID
    label: str
    balance: Decimal
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

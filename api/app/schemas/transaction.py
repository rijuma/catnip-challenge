from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.models.transaction import TransactionType


class TransactionCreate(BaseModel):
    type: TransactionType
    account_uuid: UUID
    target_account_uuid: Optional[UUID]
    amount: Decimal


class TransactionRead(BaseModel):
    type: TransactionType
    account_uuid: UUID
    target_account_uuid: UUID
    amount: Decimal
    created_at: datetime

    class Config:
        from_attributes = True

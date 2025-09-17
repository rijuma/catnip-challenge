from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.models.transaction import TransactionType
from app.models import Transaction


class TransactionCreate(BaseModel):
    type: TransactionType
    account_uuid: UUID
    target_account_uuid: Optional[UUID] = None
    label: Optional[str]
    amount: Decimal


class TransactionRead(BaseModel):
    type: TransactionType
    account_uuid: UUID
    target_account_uuid: Optional[UUID] = None
    label: Optional[str]
    amount: Decimal
    created_at: datetime

    @classmethod
    def from_transaction(cls, transaction: "Transaction") -> "TransactionRead":

        if not transaction.account:
            raise Exception(f"Inconsistent relation for account {transaction.uuid}. Missing Account.")

        if transaction.target_account_id and not transaction.target_account:
            raise Exception(f"Inconsistent relation for account {transaction.uuid}. Missing Target Account.")

        return cls(
            type=transaction.type,
            account_uuid=transaction.account.uuid,
            target_account_uuid=transaction.target_account.uuid if transaction.target_account else None,
            label=transaction.label,
            amount=transaction.amount,
            created_at=transaction.created_at,
        )

    class Config:
        from_attributes = True

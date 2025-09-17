from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel
from app.models import Account



class AccountCreate(BaseModel):
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

    @classmethod
    def from_account(cls, account: "Account") -> "AccountRead":

        if not account.user:
            raise Exception(f"Inconsistent relation for account {account.uuid}. Missing User.")

        return cls(
            uuid=account.uuid,
            label=account.label,
            balance=account.balance,
            user_uuid=account.user.uuid,
            created_at=account.created_at,
            updated_at=account.updated_at,
        )

    class Config:
        from_attributes = True
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel, text
from pydantic import field_validator


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: TransactionType
    account_id: int = Field(foreign_key="account.id", index=True)
    target_account_id: int | None = Field(foreign_key="account.id", index=True) # For transfers only
    amount: Decimal = Field(
        max_digits=12,
        decimal_places=2,
        gt=0, # A transaction needs to be greater than 0
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": text("now()")},
        nullable=False
    )

    @classmethod
    @field_validator("target_account_id")
    def validate_transaction(cls, v: int | None):
        """
        Validates that the target_account_id is set when the transaction type is "transfer",
        otherwise the target_account_id needs to be None.
        """
        if cls.type != TransactionType.TRANSFER.value:
            if v is not None:
                raise ValueError(f"target_account_id must be None if type is '{cls.type}'")
            return v

        if v is None:
            raise ValueError(f"target_account_id can't be None if type is '{cls.type}'")

        return v

from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4
from enum import Enum
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, text, Relationship
from pydantic import field_validator

# For type check only without importing the class (circular dependencies)
if TYPE_CHECKING:
    from .account import Account


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, unique=True, index=True)
    type: TransactionType
    account_id: int = Field(foreign_key="account.id", index=True)
    target_account_id: int | None = Field(
        foreign_key="account.id", index=True
    )  # For transfers only
    amount: Decimal = Field(
        max_digits=12,
        decimal_places=2,
        gt=0,  # A transaction needs to be greater than 0
    )
    account: Optional["Account"] = Relationship(
        back_populates="transactions",
        sa_relationship_kwargs={"foreign_keys": "[Transaction.account_id]"},
    )
    target_account: Optional["Account"] = Relationship(
        back_populates="incoming_transactions",
        sa_relationship_kwargs={"foreign_keys": "[Transaction.target_account_id]"},
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": text("TIMEZONE('utc', now())")},
        nullable=False,
    )

    @classmethod
    @field_validator("target_account_id")
    def validate_transaction(cls, target_account_id: int | None):
        """
        Validates that the target_account_id is set when the transaction type is "transfer",
        otherwise the target_account_id needs to be None.
        """
        if cls.type != TransactionType.TRANSFER.value:
            if target_account_id is not None:
                raise ValueError(
                    f"target_account_id must be None if type is '{cls.type}'"
                )
            return target_account_id

        if not target_account_id:
            raise ValueError(f"target_account_id can't be None if type is '{cls.type}'")

        if target_account_id == cls.account_id:
            raise ValueError("target_account_id can't be the same account as account_id")

        return target_account_id

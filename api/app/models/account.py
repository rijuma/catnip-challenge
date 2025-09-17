from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4
from typing import TYPE_CHECKING, Optional, List, cast
from sqlmodel import Field, SQLModel, Column, DateTime, text, Relationship
from sqlmodel.main import SQLModelConfig
from pydantic import ConfigDict

# For type check only without importing the class (circular dependencies)
if TYPE_CHECKING:
    from .user import User
    from .transaction import Transaction


class Account(SQLModel, table=True):
    # This enforces validations (??)
    model_config: SQLModelConfig = cast(SQLModelConfig, ConfigDict(
        validate_assignment=True,
        extra="forbid",
    ))
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, unique=True, index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    label: str
    balance: Decimal = Field(
        default=0.00,
        ge=0.0,  # A balance can't be negative
        max_digits=12,
        decimal_places=2,
        sa_column_kwargs={
            "server_default": "0.00"
        },  # This is passed down directly to the database schema.
    )
    user: "User" = Relationship(back_populates="accounts")
    transactions: List["Transaction"] = Relationship(
        back_populates="account",
        sa_relationship_kwargs={"foreign_keys": "[Transaction.account_id]"},
    )
    incoming_transactions: List["Transaction"] = Relationship(
        back_populates="target_account",
        sa_relationship_kwargs={"foreign_keys": "[Transaction.target_account_id]"},
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("TIMEZONE('utc', now())"),
            onupdate=lambda: datetime.now(timezone.utc),
            nullable=False,
        ),
    )

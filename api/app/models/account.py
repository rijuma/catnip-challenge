from datetime import datetime, timezone
from decimal import Decimal
from sqlmodel import Field, SQLModel
from typing import Optional
from uuid import UUID, uuid4


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(
        default_factory=uuid4,
        unique=True
    )
    user_id: int | None = Field(foreign_key="user.id", index=True)
    balance: Decimal = Field(
        default=0.00,
        ge=0, # A balance can't be negative
        max_digits=12,
        decimal_places=2,
        sa_column_kwargs={"server_default": "0.00"}, # This is passed down directly to the database schema.
    )
    label: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

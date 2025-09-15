from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, text


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(
        default_factory=uuid4,
        unique=True
    )
    email: str = Field(unique=True, index=True)
    tag: Optional[str] = Field(default=None, unique=True, index=True)
    first_name: str
    last_name: str
    phone: Optional[str]
    address: Optional[str]
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": text("now()")},
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={
            "server_default": text("now()"),
            "onupdate": lambda: datetime.now(timezone.utc)
        },
        nullable=False,
    )

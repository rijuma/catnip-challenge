from datetime import datetime, timezone
from typing import Optional, Annotated
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Column, DateTime, text

# Tags should start with @ and have only lowercase letters and numbers
# With at least 3 characters (besides the @).
TAG_PATTERN = r"^\@[a-z0-9]+$"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(
        default_factory=uuid4,
        unique=True,
        index=True
    )
    email: str = Field(unique=True, index=True)
    tag: Annotated[
            Optional[str],
            Field(
                regex=TAG_PATTERN,
                min_length=4,
                sa_column_kwargs={"unique": True},
                description="User handle, must start with @ and contain at least 3 lowercase letters or digits",
            )
        ]
    first_name: str
    last_name: str
    phone: Optional[str] = Field(default=None, nullable=True)
    address: Optional[str] = Field(default=None, nullable=True)
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

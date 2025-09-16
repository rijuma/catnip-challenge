from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.account import Account


@pytest.mark.asyncio
async def test_account_defaults(session: AsyncSession):
    acc = Account(label="Savings", user_id=123)
    session.add(acc)
    await session.commit()
    await session.refresh(acc)

    assert acc.id is not None
    assert isinstance(acc.uuid, UUID)
    assert acc.balance == Decimal("0.00")
    assert isinstance(acc.created_at, datetime)
    created_at: datetime = getattr(acc, "created_at")
    assert created_at.tzinfo == timezone.utc
    assert acc.label == "Savings"


@pytest.mark.asyncio
async def test_account_balance_cannot_be_negative(session: AsyncSession):
    with pytest.raises(Exception):  # DB constraint may raise IntegrityError
        acc = Account(label="Invalid", user_id=123, balance=Decimal("-10.00"))
        session.add(acc)
        await session.commit()


@pytest.mark.asyncio
async def test_account_custom_balance(session: AsyncSession):
    acc = Account(label="Checking", user_id=123, balance=Decimal("150.75"))
    session.add(acc)
    await session.commit()
    await session.refresh(acc)

    assert acc.balance == Decimal("150.75")


@pytest.mark.asyncio
async def test_account_created_at_is_timezone_aware(session: AsyncSession):
    acc = Account(label="Investment", user_id=123)
    session.add(acc)
    await session.commit()
    await session.refresh(acc)

    assert isinstance(acc.created_at, datetime)
    created_at: datetime = getattr(acc, "created_at")
    assert created_at.tzinfo == timezone.utc


@pytest.mark.asyncio
async def test_account_user_id_assignment(session: AsyncSession):
    acc = Account(label="Joint", user_id=123)
    session.add(acc)
    await session.commit()
    await session.refresh(acc)

    assert acc.user_id == 123


@pytest.mark.asyncio
async def test_account_uuid_uniqueness(session: AsyncSession):
    acc1 = Account(label="Wallet", user_id=123)
    acc2 = Account(label="Savings", user_id=456)

    session.add(acc1)
    session.add(acc2)
    await session.commit()
    await session.refresh(acc1)
    await session.refresh(acc2)

    assert acc1.uuid != acc2.uuid

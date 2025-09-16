from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Account, User

@pytest.fixture
async def user(session: AsyncSession):
    mock_user = User(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        tag="test"
    )
    session.add(mock_user)
    await session.commit()
    await session.refresh(mock_user)
    return mock_user

@pytest.mark.asyncio
async def test_account_defaults(session: AsyncSession, user: User):
    acc = Account(label="Savings", user_id=user.id)
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
async def test_account_balance_cannot_be_negative(session: AsyncSession, user: User):
    with pytest.raises(Exception):  # DB constraint may raise IntegrityError
        acc = Account(label="Invalid", user_id=user.id, balance=Decimal("-10.00"))
        session.add(acc)
        await session.commit()


@pytest.mark.asyncio
async def test_account_custom_balance(session: AsyncSession, user: User):
    acc = Account(label="Checking", user_id=user.id, balance=Decimal("150.75"))
    session.add(acc)
    await session.commit()
    await session.refresh(acc)

    assert acc.balance == Decimal("150.75")


@pytest.mark.asyncio
async def test_account_created_at_is_timezone_aware(session: AsyncSession, user: User):
    acc = Account(label="Investment", user_id=user.id)
    session.add(acc)
    await session.commit()
    await session.refresh(acc)

    assert isinstance(acc.created_at, datetime)
    created_at: datetime = getattr(acc, "created_at")
    assert created_at.tzinfo == timezone.utc


@pytest.mark.asyncio
async def test_account_user_id_assignment(session: AsyncSession, user: User):
    acc = Account(label="Joint", user_id=user.id)
    session.add(acc)
    await session.commit()
    await session.refresh(acc)

    assert acc.user_id == user.id


@pytest.mark.asyncio
async def test_account_uuid_uniqueness(session: AsyncSession, user: User):
    acc1 = Account(label="Wallet", user_id=user.id)
    acc2 = Account(label="Savings", user_id=user.id)

    session.add(acc1)
    session.add(acc2)
    await session.commit()
    await session.refresh(acc1)
    await session.refresh(acc2)

    assert acc1.uuid != acc2.uuid

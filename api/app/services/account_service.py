from typing import Optional, Sequence
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
from app.exceptions import NotFoundError, ValidationError
from app.models import Account
from app.schemas.account import AccountCreate
from app.services import user_service
from .utils.exceptions import catch_service_commit_exceptions

async def list_accounts(session: AsyncSession, offset: int, limit: int) -> Sequence[Account]:
    statement = select(Account).options(selectinload(Account.user)).offset(offset).limit(limit)  # type: ignore
    result = await session.execute(statement)
    accounts = result.scalars().all()

    return accounts

@catch_service_commit_exceptions
async def create_account(session: AsyncSession, account_data: AccountCreate) -> Account:
    user = await user_service.get_user_by_uuid(session, account_data.user_uuid)

    if not user:
        raise NotFoundError(f"User {account_data.user_uuid} not found")

    if account_data.balance < 0:
        raise ValidationError("[balance] can't be a negative value.")

    account_data_dict = account_data.model_dump(exclude_unset=True)
    account_data_dict.pop("user_uuid", None)   # The uuid is not part of the model
    account_data_dict["user_id"] = user.id

    account = Account(**account_data_dict)
    session.add(account)

    await session.commit()
    await session.refresh(account, attribute_names=["user"]) # It needs the user relation for the user_uuid

    return account

async def get_account_by_uuid(session: AsyncSession, account_uuid: UUID) -> Optional[Account]:
    statement = select(Account).options(selectinload(Account.user)).where(Account.uuid == account_uuid)  # type: ignore
    result = await session.execute(statement)
    return result.scalars().one_or_none()

async def get_user_accounts(
    session: AsyncSession, user_uuid: UUID, offset: int, limit: int
) -> Sequence[Account]:
    # Ensure the account exists
    user = await user_service.get_user_by_uuid(session, user_uuid)

    if not user:
        raise NotFoundError(f"user {user_uuid} not found")

    # Fetch related accounts
    statement = (
        select(Account)
        .options(selectinload(Account.user))  # type: ignore
        .where(Account.user_id == user.id)
        .offset(offset)
        .limit(limit)
    )

    result = await session.execute(statement)
    return result.scalars().all()

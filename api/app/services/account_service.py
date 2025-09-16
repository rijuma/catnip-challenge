from typing import Optional, Sequence
from uuid import UUID
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, or_, col
from app.exceptions import ValidationError, DatabaseError, NotFoundError
from app.models import Account, Transaction
from app.schemas.account import AccountCreate
from app.services import user_service


async def list_accounts(session: AsyncSession, offset: int, limit: int) -> Sequence[Account]:
    statement = select(Account).offset(offset).limit(limit)
    result = await session.execute(statement)
    return result.scalars().all()


async def create_account(session: AsyncSession, account_data: AccountCreate) -> Account:
    user = await user_service.get_user_by_uuid(session, account_data.user_uuid)

    if not user:
        raise NotFoundError(f"User {account_data.user_uuid} not found")

    account_data_dict = account_data.model_dump(exclude_unset=True)
    account_data_dict.pop("user_uuid", None)   # The uuid is not part of the model
    account_data_dict["user_id"] = user.id

    account = Account(**account_data_dict)
    session.add(account)

    try:
        await session.commit()
        await session.refresh(account)

        return account
    except IntegrityError as e:
        await session.rollback()
        raise ValidationError(f"Integrity error: {str(e.orig)}") from e
    except SQLAlchemyError as e:
        await session.rollback()
        raise DatabaseError("Database error") from e


async def get_account_by_uuid(session: AsyncSession, account_uuid: UUID) -> Optional[Account]:
    statement = select(Account).where(Account.uuid == account_uuid)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_transactions_for_account(
    session: AsyncSession, account_uuid: UUID, offset: int, limit: int
) -> Sequence[Transaction]:
    # Ensure the account exists
    account = await get_account_by_uuid(session, account_uuid)

    if not account:
        raise NotFoundError(f"Account {account_uuid} not found")

    # Fetch related transactions
    statement = (
        select(Transaction)
        .join(
            Account,
            or_(
                col(Transaction.account_id) == col(Account.id),
                col(Transaction.target_account_id) == col(Account.id),
            ),
        )
        .where(Account.uuid == account_uuid)
        .offset(offset)
        .limit(limit)
    )

    result = await session.execute(statement)
    return result.scalars().all()

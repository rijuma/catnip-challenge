from typing import Optional, Sequence, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, or_, col, func
from app.schemas.transaction import TransactionCreate
from app.models import Transaction, Account
from app.services import account_service
from app.exceptions import NotFoundError, ValidationError, UnexpectedError
from app.models.transaction import TransactionType
from .utils.exceptions import catch_service_commit_exceptions

async def list_transactions(session: AsyncSession, offset: int, limit: int) -> Tuple[Sequence[Transaction], int]:
    statement = (
        select(Transaction)
        .options(selectinload(Transaction.account))         # type: ignore
        .options(selectinload(Transaction.target_account))  # type: ignore
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(statement)
    transactions = result.scalars().all()

    count_stmt = select(func.count()).select_from(Transaction)  # pylint: disable=not-callable
    count = await session.scalar(count_stmt)
    count = int(count or 0)

    return transactions, count


@catch_service_commit_exceptions
async def create_transaction(
    session: AsyncSession,
    transaction_data: TransactionCreate
):
    amount = transaction_data.amount
    transaction_data_dict = transaction_data.model_dump(exclude_unset=True)

    account = await account_service.get_account_by_uuid(session, transaction_data.account_uuid)
    target_account = None

    if not account:
        raise NotFoundError(f"Account {transaction_data.account_uuid} not found")

    # Check if the transaction is a withdraw, or transfer, if the account has enough balance
    if transaction_data.type != TransactionType.DEPOSIT and account.balance < amount:
        raise ValidationError("Insufficient funds")

    # We need to convert the account_uuid reference to the actual id
    transaction_data_dict.pop("account_uuid", None)   # The uuid is not part of the model
    transaction_data_dict["account_id"] = account.id

    if transaction_data.type == TransactionType.TRANSFER:
        if not transaction_data.target_account_uuid:
            raise NotFoundError("Missing transfer destination account")

        target_account = await account_service.get_account_by_uuid(session, transaction_data.target_account_uuid)

        if not target_account:
            raise NotFoundError(f"Destination account {transaction_data.account_uuid} not found")

        transaction_data_dict["target_account_id"] = target_account.id

    # This one needs to go either way
    transaction_data_dict.pop("target_account_uuid", None)

    try:
        if transaction_data.type == TransactionType.DEPOSIT:
            account.balance += amount
        elif transaction_data.type == TransactionType.WITHDRAW:
            account.balance -= amount
        elif transaction_data.type == TransactionType.TRANSFER and target_account:
            account.balance -= amount
            target_account.balance += amount
        else:
            raise UnexpectedError("Transaction type has an unexpected value")

        session.add(account)  # Re-attach just in case

        if target_account:
            session.add(target_account)  # Re-attach just in case

        transaction = Transaction(**transaction_data_dict)
        session.add(transaction)

        await session.commit()
        # It needs the user relation for the account_uuid and target_account_uuid
        await session.refresh(transaction, attribute_names=["account", "target_account"])

    except Exception:
        await session.rollback()
        raise

    return transaction


async def get_transaction_by_uuid(session: AsyncSession, transaction_uuid: UUID) -> Optional[Transaction]:
    statement = (
        select(Transaction)
        .options(selectinload(Transaction.account))         # type: ignore
        .options(selectinload(Transaction.target_account))  # type: ignore
        .where(Transaction.uuid == transaction_uuid)
    )
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_account_transactions(
    session: AsyncSession, account_uuid: UUID, offset: int, limit: int
) ->  Tuple[Sequence[Transaction], int]:
    # Ensure the account exists
    account = await account_service.get_account_by_uuid(session, account_uuid)

    if not account:
        raise NotFoundError(f"Account {account_uuid} not found")

    # Fetch related transactions
    statement = (
        select(Transaction)
        .options(selectinload(Transaction.account))         # type: ignore
        .options(selectinload(Transaction.target_account))  # type: ignore
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
    transactions =  result.scalars().all()

    count_stmt = (
        select(func.count()).select_from(Transaction).join(  # pylint: disable=not-callable
            Account,
            or_(
                col(Transaction.account_id) == col(Account.id),
                col(Transaction.target_account_id) == col(Account.id),
            ),
        ).where(Account.uuid == account_uuid)
    )
    count = await session.scalar(count_stmt)
    count = int(count or 0)

    return transactions, count

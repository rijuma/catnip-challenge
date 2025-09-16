from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.transaction import TransactionCreate
from app.models import Transaction
from app.services import account_service
from app.exceptions import NotFoundError, ValidationError, DatabaseError
from app.models.transaction import TransactionType

async def create_transaction(
    session: AsyncSession,
    transaction_data: TransactionCreate
):
    account = await account_service.get_account_by_uuid(session, transaction_data.account_uuid)

    if account is None:
        raise NotFoundError(f"Account {transaction_data.account_uuid} not found")

    if transaction_data.type == TransactionType.TRANSFER:
        if transaction_data.target_account_uuid is None:
            raise NotFoundError("Missing transfer destination account")

        target_account = await account_service.get_account_by_uuid(session, transaction_data.target_account_uuid)

        if target_account is None:
            raise NotFoundError(f"Destination account {transaction_data.account_uuid} not found")

    transaction = Transaction(**transaction_data.model_dump())

    session.add(transaction)

    try:
        await session.commit()
        await session.refresh(transaction)
    except IntegrityError as e:
        await session.rollback()
        raise ValidationError(f"Integrity error: {str(e.orig)}") from e
    except SQLAlchemyError as e:
        await session.rollback()
        raise DatabaseError("Database error") from e

    return transaction

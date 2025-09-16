from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.transaction import TransactionCreate
from app.models import Transaction
from app.services import account_service
from app.exceptions import NotFoundError, ValidationError, DatabaseError, UnexpectedError
from app.models.transaction import TransactionType

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
        await session.refresh(transaction)

        return transaction
    except IntegrityError as e:
        await session.rollback()
        raise ValidationError(f"Integrity error: {str(e.orig)}") from e
    except SQLAlchemyError as e:
        await session.rollback()
        raise DatabaseError("Database error") from e

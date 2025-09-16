from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db import get_session
from app.models import Account, Transaction
from app.schemas.transaction import TransactionCreate, TransactionRead

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/transactions", response_model=TransactionRead, status_code=201)
async def create_transaction(
    transaction_data: TransactionCreate,
    session: AsyncSession = Depends(get_session),
):

    statement = select(Account).where(Account.uuid == transaction_data.account_uuid)
    result = await session.exec(statement)
    account = result.one_or_none()

    if not account:
        raise HTTPException(
            status_code=400,
            detail=f"account {transaction_data.account_uuid} does not exists",
        )

    transaction = Transaction(**transaction_data.model_dump(exclude_unset=True))

    session.add(transaction)

    try:
        await session.commit()
        await session.refresh(transaction)
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity error: {str(e.orig)}",
        ) from e
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error",
        ) from e

    return transaction

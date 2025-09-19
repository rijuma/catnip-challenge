from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import get_session
from app.services import transaction_service
from app.schemas.transaction import TransactionCreate, TransactionRead
from app.schemas.utils import PaginatedResponse
from .utils.exceptions import route_service_exceptions

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/", response_model=PaginatedResponse[TransactionRead], status_code=201)
@route_service_exceptions
async def list_transaction(
    session: AsyncSession = Depends(get_session),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),

):
    transactions, count = await transaction_service.list_transactions(session, offset, limit)
    transactions_read = [TransactionRead.from_transaction(trx) for trx in transactions]

    return  PaginatedResponse[TransactionRead](
        items=transactions_read,
        count=count,
    )

@router.post("/", response_model=TransactionRead, status_code=201)
@route_service_exceptions
async def create_transaction(
    transaction_data: TransactionCreate,
    session: AsyncSession = Depends(get_session),
):
    transaction = await transaction_service.create_transaction(session, transaction_data)

    return TransactionRead.from_transaction(transaction)

@router.get("/{transaction_uuid}", response_model=TransactionRead)
@route_service_exceptions
async def get_transaction(
    transaction_uuid: UUID = Path(..., description="UUID of the transaction to retrieve"),
    session: AsyncSession = Depends(get_session),
):
    transaction = await transaction_service.get_transaction_by_uuid(session, transaction_uuid)

    if not transaction:
        raise HTTPException(status_code=404, detail="Account not found")

    return TransactionRead.from_transaction(transaction)

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from sqlmodel.ext.asyncio.session import AsyncSession
from app.exceptions import ValidationError, DatabaseError, NotFoundError
from app.db import get_session
from app.schemas.account import AccountCreate, AccountRead
from app.schemas.transaction import TransactionRead
from app.services import account_service

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=List[AccountRead])
async def list_accounts(
    session: AsyncSession = Depends(get_session),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
):
    return await account_service.list_accounts(session, offset, limit)


@router.post("/", response_model=AccountRead)
async def create_account(account_data: AccountCreate, session: AsyncSession = Depends(get_session)):
    try:
        account = await account_service.create_account(session, account_data)

        return account
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e
    except DatabaseError as e:
        raise HTTPException(
            status_code=500,
            detail="Database error",
        ) from e


@router.get("/{account_uuid}", response_model=AccountRead)
async def get_account(
    account_uuid: UUID = Path(..., description="UUID of the account to retrieve"),
    session: AsyncSession = Depends(get_session),
):
    account = await account_service.get_account_by_uuid(session, account_uuid)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.get("/{account_uuid}/transactions", response_model=List[TransactionRead])
async def get_account_transactions(
    account_uuid: UUID = Path(..., description="UUID of the account to retrieve"),
    session: AsyncSession = Depends(get_session),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
):
    try:
        transactions = await account_service.get_transactions_for_account(session, account_uuid, offset, limit)

        return transactions
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
        ) from e



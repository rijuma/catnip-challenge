from typing import List
from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db import get_session
from app.models import Account
from app.schemas.account import AccountCreate, AccountRead

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/", response_model=List[AccountRead])
async def list_accounts(
    session: AsyncSession = Depends(get_session),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
):
    statement = select(Account).offset(offset).limit(limit)
    result = await session.exec(statement)
    accounts = result.all()
    return accounts

@router.post("/", response_model=AccountRead)
async def create_account(account_data: AccountCreate, session: AsyncSession = Depends(get_session)):
    account = Account(**account_data.model_dump())
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return account

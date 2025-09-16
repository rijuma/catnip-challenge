from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db import get_session
from app.models import Account
from typing import List
from app.schemas.account import AccountCreate, AccountRead

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/", response_model=List[AccountRead])
async def list_accounts(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Account))
    return result.all()

@router.post("/", response_model=AccountRead)
async def create_account(account_data: AccountCreate, session: AsyncSession = Depends(get_session)):
    account = Account(**account_data.model_dump())
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return account

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db import get_session
from app.models import Account

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/")
async def list_accounts(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Account))
    return result.all()
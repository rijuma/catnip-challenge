from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import ValidationError, DatabaseError, NotFoundError
from app.db import get_session
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.schemas.account import AccountRead
from app.schemas.utils import PaginatedResponse

from app.services import user_service, account_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=PaginatedResponse[UserRead])
async def list_users(
    session: AsyncSession = Depends(get_session),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
    q: Optional[str] = Query(None, description="Search string"),
):
    users, count = await user_service.list_users(session, offset, limit, q)
    user_reads = [UserRead.model_validate(user) for user in users]

    return PaginatedResponse[UserRead](
        items=user_reads,
        count=count,
    )



@router.post("/", response_model=UserRead)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    try:
        user = await user_service.create_user(session, user_data)

        return user
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


@router.get("/{user_uuid}", response_model=UserRead)
async def get_user(
    user_uuid: UUID = Path(..., description="ID of the user to retrieve"),
    session: AsyncSession = Depends(get_session),
):
    user = await user_service.get_user_by_uuid(session, user_uuid)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.post("/{user_uuid}", response_model=UserRead)
async def update_user(
    user_data: UserUpdate,
    user_uuid: UUID = Path(..., description="ID of the user to retrieve"),
    session: AsyncSession = Depends(get_session),
):
    try:
        user = await user_service.update_user(session, user_uuid, user_data)

        return user
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        ) from e
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

@router.get("/{user_uuid}/accounts", response_model=PaginatedResponse[AccountRead])
async def get_user_accounts(
    user_uuid: UUID = Path(..., description="ID of the user to retrieve"),
    session: AsyncSession = Depends(get_session),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
):
    accounts, count = await account_service.get_user_accounts(session, user_uuid, offset, limit)

    accounts_read = [AccountRead.from_account(acc) for acc in accounts]

    return PaginatedResponse[AccountRead](
        items=accounts_read,
        count=count,
    )

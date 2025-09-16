from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import ValidationError, DatabaseError
from app.db import get_session
from app.schemas.user import UserCreate, UserRead
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserRead])
async def list_users(
    session: AsyncSession = Depends(get_session),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
    q: Optional[str] = Query(None, description="Search string"),
):
    return await user_service.list_users(session, offset, limit, q)


@router.post("/", response_model=UserRead)
async def create_user(
    user_data: UserCreate, session: AsyncSession = Depends(get_session)
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


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int = Path(..., description="ID of the user to retrieve"),
    session: AsyncSession = Depends(get_session),
):
    user = await user_service.get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

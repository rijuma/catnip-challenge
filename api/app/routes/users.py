from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, or_
from app.db import get_session
from app.models import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserRead])
async def list_users(
    session: AsyncSession = Depends(get_session),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
    q: Optional[str] = Query(None, description="Search string"),
):
    statement = select(User)

    if q:
        # Split the query string into words and match them separately.
        # All words must match in any of the text fields for the row to be returned.
        words = q.split()
        for word in words:
            pattern = f"%{word}%"
            statement = statement.where(
                or_(
                    User.tag.ilike(pattern),            # type: ignore[attr-defined] pylint: disable=no-member
                    User.first_name.ilike(pattern),     # type: ignore[attr-defined]
                    User.last_name.ilike(pattern),      # type: ignore[attr-defined]
                    User.email.ilike(pattern),          # type: ignore[attr-defined] pylint: disable=no-member
                )
            )

    statement = statement.offset(offset).limit(limit)
    result = await session.exec(statement)
    users = result.all()
    return users


@router.post("/", response_model=UserRead)
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

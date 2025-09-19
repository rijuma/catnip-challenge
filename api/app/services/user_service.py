from typing import Any, Optional, Sequence, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, or_, func
from app.schemas.user import UserCreate, UserUpdate
from app.exceptions import NotFoundError
from app.models import User
from .utils.exceptions import catch_service_commit_exceptions


async def list_users(
    session: AsyncSession,
    offset: int,
    limit: int,
    q: Optional[str] = None,
) -> Tuple[Sequence[User], int]:
    filters: Any = []

    if q:
        # Split the query string into words and match them separately.
        words = q.split()
        for word in words:
            pattern = f"%{word}%"
            filters.append(or_(
                User.tag.ilike(pattern),         # type: ignore[attr-defined] pylint: disable=no-member
                User.first_name.ilike(pattern),  # type: ignore[attr-defined]
                User.last_name.ilike(pattern),   # type: ignore[attr-defined]
                User.email.ilike(pattern),       # type: ignore[attr-defined] pylint: disable=no-member
            ))

    users_statement = select(User).where(*filters).offset(offset).limit(limit)
    users_result = await session.execute(users_statement)
    users = users_result.scalars().all()

    count_stmt = select(func.count()).select_from(User).where(*filters)  # pylint: disable=not-callable
    count = await session.scalar(count_stmt)
    count = int(count or 0)

    return users, count

@catch_service_commit_exceptions
async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump(exclude_unset=True))



    session.add(user)

    try:
        await session.commit()
        await session.refresh(user)
    except Exception:
        await session.rollback()
        raise

    return user

async def update_user(session: AsyncSession, user_uuid: UUID, user_data: UserUpdate) -> User:
    user = await get_user_by_uuid(session, user_uuid)

    if not user:
        raise NotFoundError("User not found")

    update_data = user_data.model_dump(exclude_unset=True)
    update_data.pop("uuid", None) # We don't want to update the UUID by mistake

    for key, value in update_data.items():
        setattr(user, key, value)

    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except Exception:
        await session.rollback()
        raise

    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_user_by_uuid(session: AsyncSession, user_uuid: UUID) -> Optional[User]:
    statement = select(User).where(User.uuid == user_uuid)
    result = await session.execute(statement)
    return result.scalars().one_or_none()

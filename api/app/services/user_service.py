from typing import Optional, Sequence
from uuid import UUID
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, or_
from app.schemas.user import UserCreate, UserUpdate
from app.exceptions import NotFoundError, ValidationError, DatabaseError
from app.models import User
from .utils.exceptions import catch_service_commit_exceptions

async def list_users(
    session: AsyncSession,
    offset: int,
    limit: int,
    q: Optional[str] = None,
) -> Sequence[User]:
    statement = select(User)

    if q:
        # Split the query string into words and match them separately.
        words = q.split()
        for word in words:
            pattern = f"%{word}%"
            statement = statement.where(
                or_(
                    User.tag.ilike(pattern),         # type: ignore[attr-defined] pylint: disable=no-member
                    User.first_name.ilike(pattern),  # type: ignore[attr-defined]
                    User.last_name.ilike(pattern),   # type: ignore[attr-defined]
                    User.email.ilike(pattern),       # type: ignore[attr-defined] pylint: disable=no-member
                )
            )

    statement = statement.offset(offset).limit(limit)
    result = await session.execute(statement)
    return result.scalars().all()

@catch_service_commit_exceptions
async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump(exclude_unset=True))
    session.add(user)

    try:
        await session.commit()
        await session.refresh(user)

        return user
    except IntegrityError as e:
        await session.rollback()
        raise ValidationError(f"Integrity error: {str(e.orig)}") from e
    except SQLAlchemyError as e:
        await session.rollback()
        raise DatabaseError("Database error") from e

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

        return user
    except IntegrityError as e:
        await session.rollback()
        raise ValidationError(f"Integrity error: {str(e.orig)}") from e
    except SQLAlchemyError as e:
        await session.rollback()
        raise DatabaseError("Database error") from e


async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_user_by_uuid(session: AsyncSession, user_uuid: UUID) -> Optional[User]:
    statement = select(User).where(User.uuid == user_uuid)
    result = await session.execute(statement)
    return result.scalars().one_or_none()

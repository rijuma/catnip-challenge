from functools import wraps
from typing import Awaitable, Callable, TypeVar, ParamSpec, cast
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import ValidationError as PydanticValidationError
from sqlmodel.ext.asyncio.session import AsyncSession
from app.exceptions import ValidationError, DatabaseError

P = ParamSpec("P")
R = TypeVar("R")


def catch_service_commit_exceptions(
    func: Callable[P, Awaitable[R]]
) -> Callable[P, Awaitable[R]]:
    """
    Decorator for transforming uncatched exceptions on service methods that involve DB commits.
    """

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        session = cast(AsyncSession | None, kwargs.get("session"))
        if session is None:
            for arg in args:
                if isinstance(arg, AsyncSession):
                    session = arg
                    break

        try:
            return await func(*args, **kwargs)

        except PydanticValidationError as e:
            if session:
                await session.rollback()
            raise ValidationError("Invalid data") from e

        except (IntegrityError, SQLAlchemyError) as e:
            if session:
                await session.rollback()
            raise DatabaseError("Database error") from e

    return wrapper

from functools import wraps
from typing import Awaitable, Callable, TypeVar, ParamSpec
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import ValidationError as PydanticRequestValidationError
from fastapi.exceptions import RequestValidationError, ResponseValidationError
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
        try:
            return await func(*args, **kwargs)

        except (PydanticRequestValidationError, RequestValidationError, ResponseValidationError) as e:
            raise ValidationError(f"Invalid data: {e}") from e

        except (IntegrityError, SQLAlchemyError) as e:
            raise DatabaseError("Database error") from e

    return wrapper

from typing import Any, Awaitable, Callable, TypeVar
from functools import wraps
from fastapi import HTTPException
from app.exceptions import ValidationError, NotFoundError

T = TypeVar("T")

def route_service_exceptions(
    func: Callable[..., Awaitable[T]]
) -> Callable[..., Awaitable[T]]:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return await func(*args, **kwargs)
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Invalid data: {str(e)}") from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") from e
    return wrapper

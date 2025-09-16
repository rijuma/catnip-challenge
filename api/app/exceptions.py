class NotFoundError(Exception):
    """Raised when an entity is not found in the database."""


class UnexpectedError(Exception):
    """Raised when something that shouldn't happen, actually does happen..."""


class ValidationError(Exception):
    """Raised when an entity fails validation."""


class DatabaseError(Exception):
    """Raised when the database fails to read/write."""

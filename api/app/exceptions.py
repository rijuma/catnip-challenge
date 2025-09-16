class NotFoundError(Exception):
    """Raised when an entity is not found in the database."""


class ValidationError(Exception):
    """Raised when an entity fails validation."""


class DatabaseError(Exception):
    """Raised when the database fails to read/write."""

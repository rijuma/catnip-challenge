import asyncio
from logging.config import fileConfig

from typing import Any, Literal
from sqlmodel import SQLModel
from sqlmodel.sql.sqltypes import AutoString
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import Connection
from alembic import context
from alembic.autogenerate.api import AutogenContext
from alembic.config import Config
import app.models as _
from app.env import DATABASE_URL

SYNC_DATABASE_URL = DATABASE_URL.replace("+asyncpg", "")


# Alembic Config object
config: Config = context.config  # pylint: disable=no-member

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your models so SQLModel metadata is populated

target_metadata = SQLModel.metadata


# render AutoString as String
def render_item(
    type_: str,
    obj: Any,
    autogen_context: AutogenContext,
) -> str | Literal[False]:
    """Custom render hook to replace SQLModel's AutoString with sa.String."""
    if isinstance(obj, AutoString):
        return "sa.String()"
    return False


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(  # pylint: disable=no-member
        url=SYNC_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():  # pylint: disable=no-member
        context.run_migrations()  # pylint: disable=no-member


def do_run_migrations(connection: Connection) -> None:
    """Run migrations given a sync connection inside async run_sync()."""
    context.configure(  # pylint: disable=no-member
        connection=connection, target_metadata=target_metadata, render_item=render_item
    )  # pylint: disable=no-member
    with context.begin_transaction():  # pylint: disable=no-member
        context.run_migrations()  # pylint: disable=no-member


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode only, using async engine."""
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():  # pylint: disable=no-member
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())

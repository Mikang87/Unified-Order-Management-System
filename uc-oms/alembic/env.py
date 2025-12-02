from logging.config import fileConfig
import asyncio
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from app.models.channel import ChannelConfig
from app.core.database import Base
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def do_run_migrations(connection: AsyncConnection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    connectable_url = settings.DATABASE_URL
    connectable = create_async_engine(
        connectable_url,
        poolclass=pool.NullPool
    )
    
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)\
    
    await connectable.dispose()
    
def run_migration_online() -> None:
    asyncio.run(run_async_migrations())
    
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # Alembic.ini의 url이 주석 처리되었으므로 None이 될 수 있습니다.
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()
        
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migration_online()
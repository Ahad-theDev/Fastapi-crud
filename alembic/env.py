from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from app.models import Base
from app.config import settings

# Alembic Config object
config = context.config

# Build the database URL from settings
raw_url = settings.database_url if settings.database_url else (
    f"postgresql+psycopg://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

# Fix Render's postgres:// prefix → postgresql+psycopg://
if raw_url.startswith("postgres://"):
    db_url = raw_url.replace("postgres://", "postgresql+psycopg://", 1)
elif raw_url.startswith("postgresql://") and "+psycopg" not in raw_url:
    db_url = raw_url.replace("postgresql://", "postgresql+psycopg://", 1)
else:
    db_url = raw_url

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Your models metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # create_engine directly — NO engine_from_config, NO alembic.ini reading
    connectable = create_engine(db_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
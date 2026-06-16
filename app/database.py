from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

if settings.database_url:
    raw = settings.database_url
    # Render gives postgres:// or postgresql://, both need the psycopg driver specified
    if raw.startswith("postgres://"):
        SQL_URL = raw.replace("postgres://", "postgresql+psycopg://", 1)
    elif raw.startswith("postgresql://") and "+psycopg" not in raw:
        SQL_URL = raw.replace("postgresql://", "postgresql+psycopg://", 1)
    else:
        SQL_URL = raw
else:
    SQL_URL = (
        f"postgresql+psycopg://{settings.database_username}:"
        f"{settings.database_password}@{settings.database_hostname}:"
        f"{settings.database_port}/{settings.database_name}"
    )

engine = create_engine(SQL_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
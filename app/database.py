from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

if settings.database_url:
    # Render gives postgres://, SQLAlchemy needs postgresql+psycopg://
    SQL_URL = settings.database_url.replace(
        "postgres://", "postgresql+psycopg://", 1
    )
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
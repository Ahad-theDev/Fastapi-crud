from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

if settings.database_url:
    # Render gives postgresql:// but psycopg3 needs postgresql+psycopg://
    database_url = settings.database_url.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )
else:
    database_url = (
        f"postgresql+psycopg://"
        f"{settings.database_username}:"
        f"{settings.database_password}@"
        f"{settings.database_hostname}/"
        f"{settings.database_name}"
    )

engine = create_engine(database_url)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
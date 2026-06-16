from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

# database_url=f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"
if settings.database_url:
    database_url = settings.database_url
else:
    database_url = (
        f"postgresql+psycopg://"
        f"{settings.database_username}:"
        f"{settings.database_password}@"
        f"{settings.database_hostname}/"
        f"{settings.database_name}"
    )
# database_url = (
#     f"postgresql+psycopg://{settings.database_username}:"
#     f"{settings.database_password}@"
#     f"{settings.database_hostname}:"
#     f"{settings.database_port}/"
#     f"{settings.database_name}"
# )

engine = create_engine(database_url)

Base = declarative_base()

SessionLocal =  sessionmaker(
    bind=engine,
    autoflush=False
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
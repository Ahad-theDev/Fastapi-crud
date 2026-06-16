from fastapi import FastAPI
from .database import engine, Base
from . import models  # MUST come before create_all
from .routers import posts,users,auth,votes

app = FastAPI()

# try:
#     Base.metadata.create_all(bind=engine)
#     print("Tables created successfully")
# except Exception as e:
#     print("Table creation failed:", e)

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)
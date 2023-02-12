from fastapi import FastAPI
from . import models

app = FastAPI(title="E-hab")

from app.user import router as user_router
from app.auth import router as login_router

from app.utils import database

models.Base.metadata.create_all(database.engine)

app.include_router(user_router.router, tags=["User"])
app.include_router(login_router.router, tags=["Auth"])
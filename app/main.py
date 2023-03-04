from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from . import models

app = FastAPI(title="E-hab")

# from app.home import router as home_router
from app.user import router as user_router
from app.auth import router as login_router
from app.facilitator import router as facilitator_router
from app.support_groups import router as support_groups_router
from app.rehab_centres import router as rehab_centres_router

from app.webapp.router import auth as webapp_auth_router

from app.utils import database

models.Base.metadata.create_all(database.engine)

# app.include_router(home_router.router, tags=["Home"])
app.include_router(user_router.router, tags=["User"])
app.include_router(login_router.router, tags=["Auth"])
app.include_router(facilitator_router.router, tags=["Facilitator"])
app.include_router(support_groups_router.router, tags=["Support Groups"])
app.include_router(rehab_centres_router.router, tags=["Rehab Centres"])

app.include_router(webapp_auth_router.router)
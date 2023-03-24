from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.datastructures import URL
from app.utils.database import get_db
from app.utils import helpers
from app.search_entities import responseModels
from app.JWTtoken.token import SECRET_KEY, ALGORITHM
from app import models
from typing import List
import geocoder
from jose import jwt

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="app\\templates")
templates.env.globals['URL'] = URL

DIST = 2000


@router.get('/search-sg')
def search_sg(request: Request, db: Session = Depends(get_db)) -> List[responseModels.ShowEntity]:
    access_token = request.cookies.get("access_token")
    scheme, _, token = access_token.partition(" ")
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    email = payload.get("sub")
    user = db.query(models.Users).filter(models.Users.email == email).first()

    if not user:
        return templates.TemplateResponse("403.html", {"request": request})

    entities = []
    pos = geocoder.ip("me").latlng
    sg = db.query(models.SupportGroups).all()
    for entity in sg:
        if helpers.calc_dist(pos, (entity.latitude, entity.longitude)) < DIST:
            entities.append(entity)

    return templates.TemplateResponse("search.html", {"request": request, "entities": entities})


@router.get('/search-rc')
def search_rc(request: Request, db: Session = Depends(get_db)) -> List[responseModels.ShowEntity]:
    access_token = request.cookies.get("access_token")
    scheme, _, token = access_token.partition(" ")
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    email = payload.get("sub")
    user = db.query(models.Users).filter(models.Users.email == email).first()

    if not user:
        return templates.TemplateResponse("403.html", {"request": request})

    entities = []
    rc = db.query(models.RehabCentres).all()
    pos = geocoder.ip("me").latlng
    entities.extend(list(rc))
    for entity in rc:
        if helpers.calc_dist(pos, (entity.latitude, entity.longitude)) < DIST:
            entities.append(entity)

    return templates.TemplateResponse("search.html", {"request": request, "entities": entities})
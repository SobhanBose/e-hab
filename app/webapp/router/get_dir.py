from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.utils.database import get_db
from sqlalchemy.orm import Session
from app.models import Users
from app.search_entities.responseModels import ShowEntity
from app.JWTtoken.token import SECRET_KEY, ALGORITHM
from jose import jwt
import geocoder
import json

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="app\\templates")

@router.get('/get_dir/', response_class=HTMLResponse)
def get_direction(request: Request, entity: str, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    scheme, _, token = access_token.partition(" ")
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    email = payload.get("sub")
    user = db.query(Users).filter(Users.email == email).first()

    entity = json.loads(entity)
    pos = geocoder.ip("me").latlng
    
    response = templates.TemplateResponse("gmaps_search.html", {"request": request, "entity": entity, "pos": pos})
    return response

    # return RedirectResponse(f"https://www.google.com/maps/dir/?api=1&origin={pos[0]}%2C{pos[1]}&destination={float(entity['latitude'])}%2C{float(entity['longitude'])}")


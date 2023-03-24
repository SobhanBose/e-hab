from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from app.utils.database import get_db
from sqlalchemy.orm import Session
from app.models import Users
from app.JWTtoken.token import SECRET_KEY, ALGORITHM
from jose import jwt
import geocoder

router = APIRouter(include_in_schema=False)

@router.get('/get_dir/', response_class=HTMLResponse)
def get_direction(request: Request, lat: float | None = None, lng: float | None = None, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    scheme, _, token = access_token.partition(" ")
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    email = payload.get("sub")
    user = db.query(Users).filter(Users.email == email).first()

    pos = geocoder.ip("me").latlng

    return RedirectResponse(f"https://www.google.com/maps/dir/?api=1&origin={pos[0]}%2C{pos[1]}&destination={lat}%2C{lng}")


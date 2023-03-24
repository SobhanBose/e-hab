from fastapi import APIRouter, Request, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.user.responseModels import ShowUser
from app.JWTtoken.token import SECRET_KEY, ALGORITHM
from app.models import Users
from app.utils import database
from sqlalchemy.orm import Session
from jose import jwt
import requests, json

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="app\\templates")

@router.get('/post-login', response_class=HTMLResponse)
def post_login(request: Request, db: Session = Depends(database.get_db)):
    access_token = request.cookies.get("access_token")
    scheme, _, token = access_token.partition(" ")
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    email = payload.get("sub")
    user = db.query(Users).filter(Users.email == email).first()
    return templates.TemplateResponse("post-login.html", {"request": request, "user": user})


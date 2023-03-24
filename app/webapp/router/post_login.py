from fastapi import APIRouter, Request, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.user.responseModels import ShowUser
from app.JWTtoken.token import SECRET_KEY, ALGORITHM
from app.models import Users, Facilitators
from app.utils import database
from sqlalchemy.orm import Session
from jose import jwt
import requests, json
from starlette.datastructures import URL

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="app\\templates")

@router.get('/post-login', response_class=HTMLResponse)
def post_login(request: Request, db: Session = Depends(database.get_db)):
    access_token = request.cookies.get("access_token")
    scheme, _, token = access_token.partition(" ")
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    email = payload.get("sub")
    user = db.query(Users).filter(Users.email == email).first()

    if not user:
        return templates.TemplateResponse("403.html", {"request": request})
    
    return templates.TemplateResponse("post-login.html", {"request": request, "user": user})

@router.post('/reg-facilitator', response_class=HTMLResponse)
def reg_facilitator(request: Request, db: Session = Depends(database.get_db)):
    access_token = request.cookies.get("access_token")
    scheme, _, token = access_token.partition(" ")
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    email = payload.get("sub")
    user = db.query(Users).filter(Users.email == email).first()

    if not user:
        return templates.TemplateResponse("403.html", {"request": request})
    
    new_facilitator = Facilitators(username=user.username)
    db.add(new_facilitator)
    db.commit()
    db.refresh(new_facilitator)
    
    redirect_url = URL(request.url_for('post_login')).include_query_params()
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

    return response
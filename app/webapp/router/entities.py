from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses  import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.JWTtoken.token import SECRET_KEY, ALGORITHM
from app.utils import database
from app.models import Users, Facilitators, RehabCentres, SupportGroups
from jose import jwt
from fastapi.templating import Jinja2Templates
from starlette.datastructures import URL

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="app\\templates")

@router.get("/add-support_groups", response_class=HTMLResponse)
def add_support_grps(request: Request, db: Session = Depends(database.get_db)):
    access_token = request.cookies.get("access_token")
    scheme, _, token = access_token.partition(" ")
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    email = payload.get("sub")
    user = db.query(Users).filter(Users.email == email).first()
    if user:
        return templates.TemplateResponse("add_sg.html", {"request": request})
    

@router.get("/add-rehab_center", response_class=HTMLResponse)
def add_rehab_center(request: Request, db: Session = Depends(database.get_db)):
    access_token = request.cookies.get("access_token")
    scheme, _, token = access_token.partition(" ")
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    email = payload.get("sub")
    user = db.query(Users).filter(Users.email == email).first()
    if user:
        return templates.TemplateResponse("add_rc.html", {"request": request})


@router.post("/add-support_groups", response_class=HTMLResponse)
async def add_support_grps(request: Request, db: Session = Depends(database.get_db)):
    access_token = request.cookies.get("access_token")
    scheme, _, token = access_token.partition(" ")
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    email = payload.get("sub")
    user = db.query(Users).filter(Users.email == email).first()
    facilitator = db.query(Facilitators).filter(Facilitators.username == user.username).first()

    form = await request.form()

    new_sg = SupportGroups(name=form.get("name"), contact_email=form.get("email"), contact_no=form.get("contact_no"), facilitator=facilitator.username)
    db.add(new_sg)
    db.commit()
    db.refresh(new_sg)

    redirect_url = URL(request.url_for('post_login')).include_query_params()
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

    return response


@router.post("/add-rehab_center", response_class=HTMLResponse)
async def add_rehab_center(request: Request, db: Session = Depends(database.get_db)):
    access_token = request.cookies.get("access_token")
    scheme, _, token = access_token.partition(" ")
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    email = payload.get("sub")
    user = db.query(Users).filter(Users.email == email).first()
    facilitator = db.query(Facilitators).filter(Facilitators.username == user.username).first()

    form = await request.form()

    new_sg = RehabCentres(name=form.get("name"), contact_email=form.get("email"), contact_no=form.get("contact_no"), facilitator=facilitator.username)
    db.add(new_sg)
    db.commit()
    db.refresh(new_sg)

    redirect_url = URL(request.url_for('post_login')).include_query_params()
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

    return response


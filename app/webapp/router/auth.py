from fastapi import APIRouter, Request, Response, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.utils.hash import Hash
from app.models import Users as UserModel
from app.JWTtoken.token import create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt
from starlette.datastructures import URL

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="app\\templates")


@router.get("/login", response_class=HTMLResponse)
def login(request: Request, msg: str or None = None, db: Session=Depends(get_db)):
    try:
        access_token = request.cookies.get("access_token")
        scheme, _, token = access_token.partition(" ")
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        email = payload.get("sub")
        user = db.query(UserModel).filter(UserModel.email == email).first()

        if not user:
            return templates.TemplateResponse("login.html", {"request": request})
        
        return RedirectResponse("post-login.html", {"request": request})
    except:
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.post("/login")
async def login(request: Request, response: Response, db: Session=Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    errors = []
    try:
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            errors.append("Username or passwords is incorrect")
            return templates.TemplateResponse("login.html", {"request": request, "errors": errors})
        if Hash.verify_hash(user.password, password):
            data = {"sub": email}
            jwt_token = create_access_token(data)
            msg = "Login successful"
            redirect_url = URL(request.url_for('post_login')).include_query_params()
            response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
            # response = templates.TemplateResponse("post-login.html", {"request": request, "msg": msg, "user": user})
            response.set_cookie(key="access_token", value=f"Bearer {jwt_token}", httponly=True)
            
            return response
        else:
            errors.append("Username or password is incorrect")
            return templates.TemplateResponse("login.html", {"request": request, "errors": errors})
    except:
        errors.append("Something's wrong")
        return templates.TemplateResponse("login.html", {"request": request, "errors": errors})


@router.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.post("/register")
async def register(request: Request, response: Response, db: Session=Depends(get_db)):
    form = await request.form()
    errors = []
    if not (form.get("email") and form.get("password") and form.get("username") and form.get("name") and form.get("contact_no")):
        errors.append("Please enter all details")
        return templates.TemplateResponse("user_reg.html", {"request": request, "errors": errors})
    try:
        user = UserModel(username=form.get("username"), email=form.get("email"), password=Hash.hash_pswd(form.get("password")), name=form.get("name"), contact_no=form.get("contact_no"))
        # print("Created")
        db.add(user)
        # print("Added")
        db.commit()
        # print("Commited")
        db.refresh(user)
        # print("Refreshed")
        
        return RedirectResponse("/login?msg=Registration successful", status_code=status.HTTP_302_FOUND)
    except:
        errors.append("Something went wrong")
        return templates.TemplateResponse("user_reg.html", {"request": request, "errors": errors})
    

@router.get("/logout")
async def logout(request: Request, response: Response, db: Session=Depends(get_db)):
    access_token = request.cookies.get("access_token")
    scheme, _, token = access_token.partition(" ")
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    email = payload.get("sub")
    user = db.query(UserModel).filter(UserModel.email == email).first()

    if not user:
        return templates.TemplateResponse("403.html", {"request": request})
    
    response = templates.TemplateResponse("login.html", {"request": request})
    response.delete_cookie("access_token")
    return response


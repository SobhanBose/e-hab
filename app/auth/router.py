from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app import models
from app.auth import schemas
from app.utils.database import get_db
from app.utils.hash import Hash
from app.JWTtoken import token, responseModels


router = APIRouter()

@router.post("/login/token", response_model=responseModels.ShowToken)
def login_access_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid credentials")
    
    if not Hash.verify_hash(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid credentials")
    
    #create JWT token
    access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/forgot_password", response_model=responseModels.ShowToken)
def generate_password_reset_token(request: schemas.ForgotPassword, db: Session = Depends(get_db)) -> responseModels.ShowToken:
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid credentials")
    
    #create JWT token
    access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/reset_password", status_code=status.HTTP_202_ACCEPTED)
def reset_password(request: schemas.ResetPassword, db: Session = Depends(get_db)) -> dict:
    if not request.password or not request.token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="please enter both password and token")
    
    user = token.verify_access_token(request.token, db, HTTPException(status_code=status.HTTP_401_UNAUTHORIZED), get_user_instance = False)
    user.update({"password": Hash.hash_pswd(request.password)}, synchronize_session=False)
    db.commit()
    return {"detail": "password reset successfully"}
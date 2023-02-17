from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import datetime
import json
from typing import List
from app import models
from app.utils.database import get_db
from app.utils.hash import Hash
from app.user import responseModels, schemas
from app.OAuth2 import oauth2

router = APIRouter()

@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=responseModels.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)) -> responseModels.ShowUser:
    new_user = models.Users(username=request.username, password=Hash.hash_pswd(request.password), name=request.name, email=request.email, contact_no=request.contact_no, location=json.dumps(request.location))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/user/{username}", status_code=status.HTTP_200_OK)
def delete_user(username: str, db: Session = Depends(get_db)) -> dict:
    user = db.query(models.Users).filter(models.Users.username == username)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user{username} not found")
    
    user.delete(synchronize_session=False)
    db.commit()
    return {"detail": f"user {username} was deleted"}


@router.put("/user/update", status_code=status.HTTP_202_ACCEPTED)
def update_user(request: schemas.UpdateUser, current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)) -> dict:
    user = db.query(models.Users).filter(models.Users.username == current_user.username)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {current_user.username} was not found") 
    
    user.update(request.dict(), synchronize_session=False)
    db.commit()
    return {"detail": f"User {current_user.username} was updated"}


@router.get("/user", status_code=status.HTTP_302_FOUND, response_model=List[responseModels.ShowUser])
def get_users(db: Session = Depends(get_db)) -> List[responseModels.ShowUser]:
    users = db.query(models.Users).all()
    return users


@router.get("/user/me", status_code=status.HTTP_302_FOUND, response_model=responseModels.ShowUser)
def get_current_user(user: schemas.User = Depends(oauth2.get_current_user)) -> responseModels.ShowUser:
    return user


@router.get("/user/{username}", status_code=status.HTTP_302_FOUND, response_model=responseModels.ShowUser)
def get_user_by_username(username: str, db: Session = Depends(get_db)) -> responseModels.ShowUser:
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {username} not found")
    return user
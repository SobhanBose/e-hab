from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.utils.database import get_db
from app.facilitator import responseModels
from app.user import schemas
from app.OAuth2 import oauth2

router = APIRouter()

@router.get("/facilitator")
def facilitator_home():
    return {"data": "facilitator home"}


@router.post("/facilitator/register", status_code=status.HTTP_201_CREATED, response_model=responseModels.showFacilitator)
def register_facilitator(current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)) -> responseModels.showFacilitator:
    new_facilitator = models.Facilitators(username=current_user.username)
    db.add(new_facilitator)
    db.commit()
    db.refresh(new_facilitator)
    return new_facilitator


@router.get("/facilitator/isFacilitator")
def is_facilitator(current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)) -> bool:
    facilitator = db.query(models.Facilitators).filter(models.Facilitators.username == current_user.username).first()
    if facilitator:
        return True
    return False
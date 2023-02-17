from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.support_groups import schemas, responseModels
from app.user import schemas as userSchemas
from app.utils.database import get_db
from app.OAuth2 import oauth2
from app import models

router = APIRouter()

@router.get("/supportgroups")
def support_groups_home():
    return {"data": "support groups home"}


@router.post("/supportgroups/create", status_code=status.HTTP_201_CREATED, response_model=responseModels.showSupportGroups)
def create_support_groups(request: schemas.supportGroups, current_user: userSchemas.User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)) -> responseModels.showSupportGroups:
    facilitator = db.query(models.Facilitators).filter(models.Facilitators.username == current_user.username).first()
    if not facilitator:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{current_user.username} is not a facilitator")
    new_sg = models.SupportGroups(name=request.name, contact_email=request.contact_email, contact_no=request.contact_no, location=request.location, facilitator=facilitator.username)
    db.add(new_sg)
    db.commit()
    db.refresh(new_sg)
    return new_sg


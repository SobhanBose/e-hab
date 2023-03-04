from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.rehab_centres import schemas, responseModels
from app.user import schemas as userSchemas
from app.utils.database import get_db
from app.OAuth2 import oauth2
from app import models

router = APIRouter()

@router.get("/rehabcentres")
def rehab_centres_home():
    return {"data": "support centres home"}


@router.post("/rehabcentres/create", status_code=status.HTTP_201_CREATED, response_model=responseModels.showRehabCentres)
def create_rehab_centres(request: schemas.rehabCentres, current_user: userSchemas.User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)) -> responseModels.showRehabCentres:
    facilitator = db.query(models.Facilitators).filter(models.Facilitators.username == current_user.username).first()
    if not facilitator:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{current_user.username} is not a facilitator")
    new_sg = models.RehabCentres(name=request.name, contact_email=request.contact_email, contact_no=request.contact_no, facilitator=facilitator.username)
    db.add(new_sg)
    db.commit()
    db.refresh(new_sg)
    return new_sg
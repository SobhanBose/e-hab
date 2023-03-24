from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.search_entities import responseModels
from app.user import schemas as userSchemas
from app.utils.database import get_db
from app.OAuth2 import oauth2
from app import models

router = APIRouter()

@router.get("/get_entities", response_model=List[responseModels.ShowEntity])
def get_entities(db: Session = Depends(get_db)) -> List[responseModels.ShowEntity]:
    entities = []
    rc = db.query(models.RehabCentres).all()
    entities.extend(list(rc))
    sg = db.query(models.SupportGroups).all()
    entities.extend(list(sg))

    return entities


@router.get("/get_sg", response_model=List[responseModels.ShowEntity])
def get_entities(db: Session = Depends(get_db)) -> List[responseModels.ShowEntity]:
    entities = []
    sg = db.query(models.SupportGroups).all()
    entities.extend(list(sg))

    return entities


@router.get("/get_rc", response_model=List[responseModels.ShowEntity])
def get_entities(db: Session = Depends(get_db)) -> List[responseModels.ShowEntity]:
    entities = []
    rc = db.query(models.RehabCentres).all()
    entities.extend(list(rc))

    return entities
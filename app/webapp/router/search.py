from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import requests, json


router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="app\\templates")


@router.get('/search-all')
def search_all(request: Request):
    entities = requests.get("http://localhost:8000/get_entities")
    return templates.TemplateResponse("search.html", {"request": request, "entities": entities.json()})


@router.get('/search-sg')
def search_sg(request: Request):
    entities = requests.get("http://localhost:8000/get_sg")
    return templates.TemplateResponse("search.html", {"request": request, "entities": entities.json()})


@router.get('/search-rc')
def search_rc(request: Request):
    entities = requests.get("http://localhost:8000/get_rc")
    return templates.TemplateResponse("search.html", {"request": request, "entities": entities.json()})
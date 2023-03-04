from app.rehab_centres.schemas import rehabCentres

class showRehabCentres(rehabCentres):
    name: str
    facilitator: str
    latitude: float
    longitude: float

    class Config():
        orm_mode = True
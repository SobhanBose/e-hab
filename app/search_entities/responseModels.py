from pydantic import BaseModel

class ShowEntity(BaseModel):
    name: str
    contact_email: str
    contact_no: int
    latitude: float
    longitude: float

    class Config():
        orm_mode = True
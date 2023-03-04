from pydantic import BaseModel

class ShowUser(BaseModel):
    username: str
    name: str
    email: str
    contact_no: int
    latitude: float
    longitude: float

    class Config():
        orm_mode = True
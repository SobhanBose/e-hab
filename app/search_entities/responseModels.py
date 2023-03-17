from pydantic import BaseModel

class ShowEntity(BaseModel):
    name: str
    contact_email: str
    contact_no: int

    class Config():
        orm_mode = True
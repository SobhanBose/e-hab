from pydantic import BaseModel

class ShowUser(BaseModel):
    username: str
    name: str
    email: str
    contact_no: int
    pic: str

    class Config():
        orm_mode = True
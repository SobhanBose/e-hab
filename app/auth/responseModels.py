from pydantic import BaseModel

class ShowLogin(BaseModel):
    username: str

    class Config():
        orm_mode = True
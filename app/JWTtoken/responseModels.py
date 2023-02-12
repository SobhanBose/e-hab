from app.JWTtoken.schemas import Token

class ShowToken(Token):
    class Config():
        orm_mode = True
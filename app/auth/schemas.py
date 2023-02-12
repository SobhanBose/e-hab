from pydantic import BaseModel, Field, EmailStr

class Login(BaseModel):
    username: str = Field(...)
    password: str = Field(...)


class ForgotPassword(BaseModel):
    email: EmailStr = Field(...)


class ResetPassword(BaseModel):
    token: str = Field(...)
    password: str = Field(...)
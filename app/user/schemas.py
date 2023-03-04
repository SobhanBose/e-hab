from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    contact_no: int = Field(..., ge=1000000000, le=9999999999)

class UpdateUser(BaseModel):
    name: str = Field(...)
from pydantic import BaseModel, Field, EmailStr

class supportGroups(BaseModel):
    name: str = Field(...)
    contact_email: EmailStr = Field(...)
    contact_no: int = Field(..., ge=1000000000, le=9999999999)
    location: str = Field(...)

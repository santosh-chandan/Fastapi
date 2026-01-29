from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=4)

class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    level: Optional[int] = None

class GetUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    level: int

    model_config = ConfigDict(from_attributes=True)

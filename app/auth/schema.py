# app/auth/schema.py
from pydantic import BaseModel, EmailStr


class CreateLogin(BaseModel):
    email: EmailStr
    password: str

class SendToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'

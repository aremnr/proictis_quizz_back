from pydantic import BaseModel, EmailStr, ConfigDict
import uuid

class AdminSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | uuid.UUID
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class RegistrationSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    referral_token: str
from datetime import timedelta, datetime, timezone
from pydantic import EmailStr
from sqlalchemy.orm import Session
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.exceptions import HTTPException
from fastapi import FastAPI, Depends, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from database.database import get_db
import admin_side.schemas as schemas
import admin_side.crud as crud
import random
import string


contx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_password(plain_password, hashed_password):
    return contx.verify(plain_password, hashed_password)

def get_password_hash(password):
    return contx.hash(password)

def create_referral_token():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(20))

def authenticate_admin(password: str, username: str = None, email: EmailStr = None,
                       db: Session = Depends(get_db)) -> bool | schemas.AdminSchema:
    admin = crud.get_admin(db=db, username=username, email=email)
    if not admin:
        return False
    if not verify_password(password, admin.password):
        return False
    return admin

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"expire": str(expire)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

async def get_current_admin(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("name")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    admin = crud.get_admin(db=db, username=token_data.username)
    if admin is None:
        raise credentials_exception
    return admin
from datetime import timedelta
from sqlalchemy.orm import Session
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from typing import Annotated
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from database.database import get_db
import admin_side.schemas as schemas
import admin_side.crud as crud
import admin_side.admin_func as admin_func


router = APIRouter()


@router.post("/login", tags=["auth"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> schemas.Token:
    user = admin_func.authenticate_admin(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = admin_func.create_access_token(
        data={"name": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

@router.post("/register", tags=["auth"])
async def register_admin(
        admin: schemas.RegistrationSchema,
        db: Session = Depends(get_db),
):
    is_ref_true: bool = crud.check_referral(token=admin.referral_token)
    if is_ref_true:
        crud.add_admin(db=db, username=admin.username, email=admin.email, password=admin_func.get_password_hash(admin.password))
        return {"status": "Registration Successful"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect referral token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/create_referral", tags=["auth"])
def create_referral(admin: Annotated[schemas.AdminSchema, Depends(admin_func.get_current_admin)]):
    ref_token = admin_func.create_referral_token()
    crud.referral(key=admin.username, text=ref_token)
    return {"referral": admin.username+ '_' + ref_token}


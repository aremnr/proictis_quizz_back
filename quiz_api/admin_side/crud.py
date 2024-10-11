import uuid

from pydantic import EmailStr
from sqlalchemy.orm import Session
import admin_side.models as models
import admin_side.schemas as schemas
from cache.redis_main import cache

def get_admin(db: Session, username: str | None = None, email: EmailStr | None = None):
    if username:
        admin = schemas.AdminSchema.model_validate(
            db.query(models.AdminModel).filter(models.AdminModel.username == username).one(),
            from_attributes=True
        )
    if email:
        admin = schemas.AdminSchema.model_validate(
            db.query(models.AdminModel).filter(models.AdminModel.email == email).one(),
            from_attributes=True
        )
    return admin

def referral(key: str, text: str):
    cache.add_cache(key=key, text=text, time = 900)
    return True

def check_referral(token: str):
    received_token = cache.check_cache(key=token.split('_')[0])
    #return received_token == token.split('_')[1]
    return received_token if not received_token else received_token == token.split('_')[1]

def add_admin(db: Session, username: str | None = None, email: EmailStr | None = None, password: str | None = None):
    admin_db = models.AdminModel(id=uuid.uuid4(), username=username, email=str(email), password=password)
    db.add(admin_db)
    db.flush()
    db.commit()
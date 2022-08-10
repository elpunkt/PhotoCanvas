import os
from typing import Optional, List

from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder

from . import models, schemas
from .security import get_password_hash, verify_password



def user_get(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def user_get_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def user_get_multi(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def user_create(db: Session, *, obj_in: schemas.UserCreate) -> models.User:
    db_obj = models.User(
        email=obj_in.email,
        hashed_password=get_password_hash(obj_in.password),
        is_superuser=obj_in.is_superuser,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def user_remove(db: Session, uid: int) -> models.User:
    user = db.query(models.User).get(uid)
    db.delete(user)
    db.commit()
    return user


def user_authenticate(db: Session, *, email: str, password: str) -> Optional[models.User]:
    user = user_get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def user_get_all_superusers(db: Session) -> List[models.User]:
    return db.query(models.User).filter_by(is_superuser=True).all()


def user_is_active(user: models.User) -> bool:
    return user.is_active


def user_is_superuser(user: models.User) -> bool:
    return user.is_superuser


def get_photos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Photo).offset(skip).limit(limit).order_by(models.Photo.upload_date.desc()).all()


def create_photo(db: Session, photo: schemas.PhotoCreate):
    db_photo = models.Photo(**jsonable_encoder(photo))
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

def delete_photo(db: Session, pid: int):
    obj = db.query(models.Photo).get(pid)
    filename = obj.filename
    db.delete(obj)
    db.commit()
    os.remove(f"frontend/public/uploaded/{filename}")
    return obj

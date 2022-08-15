from datetime import timedelta
import time
import random
import math
from typing import Any

from PIL import Image, UnidentifiedImageError, ImageOps
from sqlalchemy.orm import Session
from typing import List

from fastapi import (APIRouter, HTTPException,
                     UploadFile, Form, BackgroundTasks, Depends)
from fastapi.security import OAuth2PasswordRequestForm

from . import security, models, deps
from .schemas import Message, Photo, Token, User, UserCreate
from .settings import settings
from .crud import (photo_get, user_get, user_create, create_photo, get_photos, delete_photo, user_authenticate, user_is_active, user_get_multi, user_get_by_email, user_remove, user_get_all_superusers)
from .websocket import ws_manager
api_router = APIRouter()


async def process_image(imgin, title, db):
    img = ImageOps.exif_transpose(imgin)
    img_name = f"{math.floor(time.time())}_{random.randint(10000,99999)}.{img.format}"
    img.thumbnail((settings.MAX_IMG_WIDTH, settings.MAX_IMG_HEIGHT))
    img.save(f"{settings.IMG_SAVE_PATH}{img_name}",
             quality=settings.IMG_QUALITY,
             optimize=settings.OPTIMIZE_IMGS,
             format=imgin.format)
    photo_meta = {"title":title, "filename": img_name, "upload_date": time.time()}
    create_photo(db, photo_meta)
    await ws_manager.broadcast_photo_action({'action': 'add', 'photo': photo_meta})


@api_router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    elif not user_is_active(user):
        raise HTTPException(status_code=401, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@api_router.get("/users/me", response_model=User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    return current_user


@api_router.get("/users", response_model=List[User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    users = user_get_multi(db, skip=skip, limit=limit)
    return users

@api_router.post("/users", response_model=User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    user = user_get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this username already exists in the system.",
        )
    user = user_create(db, obj_in=user_in)
    return user

@api_router.delete("/users/{id}", response_model=Message)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a User.
    """
    user = user_get(db, id)
    if not user:
        return Message(state="success", message="Deleted")
    if user.is_superuser:
        alladmins = user_get_all_superusers(db)
        if len(alladmins) == 1:
            raise HTTPException(
                status_code=400,
                detail="It's not allowed to remove the last remaining superuser.",
            )
    user = user_remove(db=db, uid=id)
    return Message(state="success", message="Deleted")


@api_router.post('/upload', response_model=Message)
def upload_photo(background_tasks: BackgroundTasks,
                 photo: UploadFile,
                 title: str = Form(),
                 db: Session = Depends(deps.get_db)):
    if not photo:
        return {"state":"error", "message":"No upload file sent"}
    try:
        image = Image.open(photo.file)
    except UnidentifiedImageError:
        return {"state":"error", "message": "Dieses Dateiformat wird leider nicht unterstützt."}
    background_tasks.add_task(process_image, image, title, db)
    return Message(state="success", message="File is beeing processed.")


@api_router.get('/photos', response_model=List[Photo])
def get_all_photos(db: Session = Depends(deps.get_db),
                   current_user: models.User = Depends(deps.get_current_active_user)):
    return get_photos(db, skip=None, limit=None)


@api_router.delete('/photos/{pid}', response_model=Message)
async def delete_photo_by_id(pid: int,
                             db: Session = Depends(deps.get_db),
                             current_user: models.User = Depends(deps.get_current_active_superuser)):
    deleted_photo = delete_photo(db, pid)
    await ws_manager.broadcast_photo_action({'action': 'delete', 'photo': deleted_photo})
    return Message(state="success", message="Photo deleted.")


@api_router.get('/photos/{pid}/rotate', response_model=Message)
def rotate_photo(pid: int,
                 db: Session = Depends(deps.get_db),
                 current_user: models.User = Depends(deps.get_current_active_superuser)):
    photo = photo_get(db=db, pid=pid)
    if not photo:
        return {"state":"error", "message":"No photo with this id."}
    img = Image.open(f"{settings.IMG_SAVE_PATH}{photo.filename}")
    out = img.rotate(90, expand=True)
    out.save(f"{settings.IMG_SAVE_PATH}{photo.filename}",
                quality=settings.IMG_QUALITY,
                optimize=settings.OPTIMIZE_IMGS,
                format=img.format)
    return Message(state="success", message="Photo rotated")

from datetime import timedelta
import time
import random
import math
from typing import Any

from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session
from typing import List

from fastapi import (APIRouter, HTTPException,
                     UploadFile, Form, BackgroundTasks, Depends)
from fastapi.security import OAuth2PasswordRequestForm

from . import security, models, deps
from .schemas import Message, Photo, Token, User
from .settings import settings
from .crud import (create_photo, get_photos, delete_photo, user_authenticate, user_is_active)
from .websocket import ws_manager
api_router = APIRouter()

async def process_image(img, title, db):
    img_name = f"{math.floor(time.time())}_{random.randint(10000,99999)}.{img.format}"
    img.thumbnail((settings.MAX_IMG_WIDTH, settings.MAX_IMG_HEIGHT))
    img.save(f"{settings.IMAGE_SAVE_PATH}{img_name}",
             quality=settings.IMG_QUALITY,
             optimize=settings.OPTIMIZE_IMGS)
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
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user_is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
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

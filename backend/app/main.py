from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .crud import user_get_by_email, user_create
from .settings import settings
from .schemas import UserCreate
from . import models
from .database import engine
from .deps import get_db
from .api import api_router
from .websocket import websocket_router



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(websocket_router, prefix='/ws')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "https://maurer-rautenberg.de"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    first_superuser = user_get_by_email(db=db, email=settings.FIRST_SUPERUSER)
    if not first_superuser:
        user_create(db=db, obj_in=UserCreate(email=settings.FIRST_SUPERUSER,
                                             password=settings.FIRST_SUPERUSER_PASSWORD,
                                             is_superuser=True))

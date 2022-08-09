import secrets
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECRET_KEY: str = secrets.token_urlsafe(32)

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    POSTGRES_DB: str = None
    POSTGRES_SERVER: str = None
    POSTGRES_PW: str = None
    POSTGRES_USER: str = None

    MAX_IMG_WIDTH: int = 1080
    MAX_IMG_HEIGHT: int = 1080
    OPTIMIZE_IMGS: bool = True
    IMG_QUALITY: int = 90

    class Config:
        env_file = ".env"

settings = Settings()

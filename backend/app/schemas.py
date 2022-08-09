from typing import Optional

from pydantic import BaseModel


class PhotoBase(BaseModel):
    title: Optional[str]


class PhotoCreate(PhotoBase):
    filename: str
    upload_date: int
    pass


class Photo(PhotoBase):
    id: int
    filename: str
    upload_date: int



    class Config:
        orm_mode = True





class UserBase(BaseModel):
    email: str
    is_superuser: bool = False



class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class Message(BaseModel):
    state: str
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None

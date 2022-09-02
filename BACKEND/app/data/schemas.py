from typing import Any
from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str


class Comment(CommentBase):
    id: int
    user_id: int
    post_id: int
    user_name: str
    username: str
    user_pic: str
    date_created: Any

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    heading: str
    content: str
    image: str


class Post(PostBase):
    id: int
    user_name: str
    user_id: int
    username: str
    user_pic: str
    date_created: Any

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    email: str
    password: str


class UserBase(BaseModel):
    name: str
    username: str
    email: str
    about: str
    sex: str
    pronouns: str
    profile_picture: str
    cover_photo: str


class UserCreate(UserBase):
    password: str
    confirm_password: str


class User(UserBase):
    id: int
    date_joined: Any

    class Config:
        orm_mode = True


class AdminAuth(BaseModel):
    email: str
    password: str


class AdminBase(BaseModel):
    admin_name: str
    email: str


class AdminCreate(AdminBase):
    password: str
    confirm_password: str


class Admin(AdminBase):
    id: int
    date_joined: Any

    class Config:
        orm_mode = True

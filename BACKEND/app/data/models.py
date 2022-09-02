from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.data.database import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    admin_name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    date_joined = Column(String, default=datetime.now().strftime("%d/%m/%Y"))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    about = Column(String)
    sex = Column(String)
    pronouns = Column(String)
    profile_picture = Column(String)
    cover_photo = Column(String)
    password = Column(String)
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    date_joined = Column(String, default=datetime.now().strftime("%d/%m/%Y"))


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    heading = Column(String, index=True)
    content = Column(String, index=True)
    image = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    username = Column(String, index=True)
    user_name = Column(String, index=True)
    user_pic = Column(String, index=True)
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    date_created = Column(String, default=datetime.now().strftime("%d/%m/%Y"))


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    username = Column(String, index=True)
    user_name = Column(String, index=True)
    user_pic = Column(String, index=True)
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    date_created = Column(String, default=datetime.now().strftime("%d/%m/%Y"))

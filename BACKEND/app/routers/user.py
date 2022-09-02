from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError
import bcrypt
from fastapi_jwt_auth import AuthJWT
from ..data import models, schemas
from ..utils import DryFunc
from pydantic import BaseModel

user = APIRouter(prefix="/user")


class Settings(BaseModel):
    authjwt_secret_key: str = '7a1fd21e19813b07264649b20a621a548b32bf1c6053d5bac1f114794c63470c'


@AuthJWT.load_config
def get_config():
    return Settings()


@user.post("/register", status_code=201)
def register(reg_user: schemas.UserCreate, db: Session = Depends(DryFunc.get_db)):
    username = reg_user.username
    email = reg_user.email
    password = reg_user.password
    name = reg_user.name
    cover_photo = reg_user.cover_photo or \
                  "https://res.cloudinary.com/de49puo0s/image/upload/v1661913718/pdhhvl1bjqwaotapv9n5.jpg"
    profile_picture = reg_user.profile_picture or \
                      "https://res.cloudinary.com/de49puo0s/image/upload/v1661913695/qozghybwzswy6dimxpxt.jpg"

    same_username = DryFunc.filter_one(db, models.User, models.User.username, username)
    same_email = DryFunc.filter_one(db, models.User, models.User.email, email)

    if len(name) < 3:
        raise HTTPException(status_code=400, detail="Name must be at least 3 characters!")
    if len(username) < 5:
        raise HTTPException(status_code=400, detail="Username must be at least 5 characters!")
    if len(username.split("@")) < 2:
        raise HTTPException(status_code=400, detail="Username must start with '@'!")
    if len(username.split("@")) > 2:
        raise HTTPException(status_code=400, detail="Username must contain only one '@'!")
    if not username.split("@")[1].isalnum():
        raise HTTPException(status_code=400, detail="Username can only contain '@', alphabets and numbers!")
    if same_username:
        raise HTTPException(status_code=409, detail="Username already exists!")
    try:
        email = validate_email(email).email
    except EmailNotValidError:
        raise HTTPException(status_code=400, detail="Please enter a valid email!")
    if same_email:
        raise HTTPException(status_code=409, detail="Email already exists!")
    if len(password) < 7:
        raise HTTPException(status_code=400, detail="Password must be at least 7 characters!")
    if not password.isalnum():
        raise HTTPException(status_code=400, detail="Password must be alphanumeric!")
    if password != reg_user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords don't match!")

    password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())

    new_user = models.User(name=name, username=username, email=email, password=password,
                           about=reg_user.about, sex=reg_user.sex, pronouns=reg_user.pronouns,
                           profile_picture=profile_picture, cover_photo=cover_photo)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"detail": "User created!"}


@user.post("/login", status_code=200)
def login(log_user: schemas.UserAuth, authorize: AuthJWT = Depends(), db: Session = Depends(DryFunc.get_db)):
    email = log_user.email
    password = log_user.password

    auth_user1 = DryFunc.filter_one(db, models.User, models.User.email, email)
    auth_user2 = DryFunc.filter_one(db, models.User, models.User.username, email)

    auth_user = auth_user1 or auth_user2

    if not auth_user:
        raise HTTPException(status_code=400, detail="Invalid login details!")
    if not bcrypt.checkpw(password.encode("UTF-8"), auth_user.password):
        raise HTTPException(status_code=400, detail="Invalid login details!")

    access_token = authorize.create_access_token(subject=auth_user.id)
    refresh_token = authorize.create_refresh_token(subject=auth_user.id)

    return {"detail": "Login successful!", "user": auth_user, "access_token": access_token,
            "refresh_token": refresh_token}


@user.get('/current', status_code=200, response_model=schemas.User)
def get(authorize: AuthJWT = Depends(), db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    current_user = authorize.get_jwt_subject()
    cur_user = DryFunc.filter_one(db, models.User, models.User.id,  int(current_user))

    if not cur_user:
        raise HTTPException(status_code=400, detail="Invalid user!")

    return cur_user


@user.get('/all/{page}', status_code=200)
def get(page, db: Session = Depends(DryFunc.get_db)):
    all_users = DryFunc.get_all(db, models.User)

    page_users = DryFunc.paginate(page, all_users)

    return page_users


@user.get('/posts/all/{user_id}/{page}', status_code=200)
def get(user_id, page, db: Session = Depends(DryFunc.get_db)):
    cur_user = DryFunc.filter_one(db, models.User, models.User.id, int(user_id))

    user_post = DryFunc.paginate(page, cur_user.posts)

    return user_post


@user.get('/comments/all/{user_id}/{page}', status_code=200)
def get(user_id, page, db: Session = Depends(DryFunc.get_db)):
    cur_user = DryFunc.filter_one(db, models.User, models.User.id, int(user_id))

    user_comment = DryFunc.paginate(page, cur_user.comments)

    return user_comment


@user.get('/{index}', status_code=200, response_model=schemas.User)
def get(index, db: Session = Depends(DryFunc.get_db)):
    get_user = DryFunc.filter_one(db, models.User, models.User.id, int(index))

    if not get_user:
        raise HTTPException(status_code=400, detail="Invalid user!")

    return get_user


@user.put('/update', status_code=200)
def update(up_user: schemas.UserBase, authorize: AuthJWT = Depends(), db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    username = up_user.username
    email = up_user.email
    name = up_user.name
    cover_photo = up_user.cover_photo or \
                  "https://res.cloudinary.com/de49puo0s/image/upload/v1661913718/pdhhvl1bjqwaotapv9n5.jpg"
    profile_picture = up_user.profile_picture or \
                      "https://res.cloudinary.com/de49puo0s/image/upload/v1661913695/qozghybwzswy6dimxpxt.jpg"

    current_user = authorize.get_jwt_subject()
    cur_user = DryFunc.filter_one(db, models.User, models.User.id,  int(current_user))
    same_username = DryFunc.filter_one(db, models.User, models.User.username, username)
    same_email = DryFunc.filter_one(db, models.User, models.User.email, email)

    if not cur_user:
        raise HTTPException(status_code=400, detail="Invalid user!")
    if len(name) < 3:
        raise HTTPException(status_code=400, detail="Name must be at least 3 characters!")
    if len(username) < 5:
        raise HTTPException(status_code=400, detail="Username must be at least 5 characters!")
    if len(username.split("@")) < 2:
        raise HTTPException(status_code=400, detail="Username must start with '@'!")
    if len(username.split("@")) > 2:
        raise HTTPException(status_code=400, detail="Username must contain only one '@'!")
    if not username.split("@")[1].isalnum():
        raise HTTPException(status_code=400, detail="Username can only contain '@', alphabets and numbers!")
    if same_username and same_username != cur_user:
        raise HTTPException(status_code=409, detail="Username already exists!")
    try:
        email = validate_email(email).email
    except EmailNotValidError:
        raise HTTPException(status_code=400, detail="Please enter a valid email!")
    if same_email and same_email != cur_user:
        raise HTTPException(status_code=409, detail="Email already exists!")

    cur_user.name = name
    cur_user.username = username
    cur_user.email = email
    cur_user.about = up_user.about
    cur_user.sex = up_user.sex
    cur_user.pronouns = up_user.pronouns
    cur_user.profile_picture = profile_picture
    cur_user.cover_photo = cover_photo

    DryFunc.update_many(db, models.Post, models.Post.user_id, cur_user.id,
                        models.Post.user_name, name)
    DryFunc.update_many(db, models.Post, models.Post.user_id, cur_user.id,
                        models.Post.username, username)
    DryFunc.update_many(db, models.Post, models.Post.user_id, cur_user.id,
                        models.Post.user_pic, profile_picture)
    DryFunc.update_many(db, models.Comment, models.Comment.user_id, cur_user.id,
                        models.Comment.user_name, name)
    DryFunc.update_many(db, models.Comment, models.Comment.user_id, cur_user.id,
                        models.Comment.username, username)
    DryFunc.update_many(db, models.Comment, models.Comment.user_id, cur_user.id,
                        models.Post.user_pic, profile_picture)

    db.commit()
    db.refresh(cur_user)

    return {"detail": "Update successful, log in to continue!"}


@user.delete('/delete', status_code=200)
def delete(authorize: AuthJWT = Depends(), db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    current_user = authorize.get_jwt_subject()
    cur_user = DryFunc.filter_one(db, models.User, models.User.id,  int(current_user))

    if not cur_user:
        raise HTTPException(status_code=400, detail="Invalid user!")

    db.delete(cur_user)
    db.commit()

    return {"detail": "Account deleted!"}


@user.post('/refresh')
def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()

    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}

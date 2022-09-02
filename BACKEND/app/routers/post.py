from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from ..data import models, schemas
from ..utils import DryFunc

post = APIRouter(prefix="/post")


@post.post("/create", status_code=201)
def create(create_post: schemas.PostBase, authorize: AuthJWT = Depends(), db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    cur_user = authorize.get_jwt_subject()
    heading = create_post.heading
    content = create_post.content

    post_user = DryFunc.filter_one(db, models.User, models.User.id, int(cur_user))

    if not post_user:
        raise HTTPException(status_code=400, detail="Invalid user!")
    if len(heading) < 1:
        raise HTTPException(status_code=400, detail="Heading must be at least 10 characters!")
    if len(content) < 1:
        raise HTTPException(status_code=400, detail="Content must be at least 50 characters!")

    new_post = models.Post(heading=heading, content=content, image=create_post.image, user_id=post_user.id,
                           username=post_user.username, user_name=post_user.name,
                           user_pic=post_user.profile_picture)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"detail": "Post created!"}


@post.get('/all/{page}', status_code=200)
def get(page, db: Session = Depends(DryFunc.get_db)):
    all_posts = DryFunc.get_all(db, models.Post)

    page_posts = DryFunc.paginate(page, all_posts)

    return page_posts


@post.get('/comments/all/{post_id}/{page}', status_code=200)
def get(post_id, page, db: Session = Depends(DryFunc.get_db)):
    cur_post = DryFunc.filter_one(db, models.Post, models.Post.id, int(post_id))

    post_comment = DryFunc.paginate(page, cur_post.comments)

    return post_comment


@post.get('/{index}', status_code=200, response_model=schemas.Post)
def get(index, db: Session = Depends(DryFunc.get_db)):
    get_post = DryFunc.filter_one(db, models.Post, models.Post.id, int(index))

    if not get_post:
        raise HTTPException(status_code=400, detail="Invalid post!")

    return get_post


@post.put('/update/{index}', status_code=200)
def update(index, up_post: schemas.PostBase, authorize: AuthJWT = Depends(),
           db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    heading = up_post.heading
    content = up_post.content
    cur_user = authorize.get_jwt_subject()

    cur_post = DryFunc.filter_one(db, models.Post, models.Post.id, int(index))

    if not cur_post:
        raise HTTPException(status_code=400, detail="Invalid post!")
    if cur_post.user_id != int(cur_user):
        raise HTTPException(status_code=400, detail="Action not allowed!")
    if len(heading) < 10:
        raise HTTPException(status_code=400, detail="Heading must be at least 10 characters!")
    if len(content) < 50:
        raise HTTPException(status_code=400, detail="Content must be at least 50 characters!")

    cur_post.heading = heading
    cur_post.content = content
    cur_post.image = up_post.image

    db.commit()
    db.refresh(cur_post)

    return {"detail": "Update successful!"}


@post.delete('/delete/{index}', status_code=200)
def delete(index, authorize: AuthJWT = Depends(), db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    cur_user = authorize.get_jwt_subject()

    del_post = DryFunc.filter_one(db, models.Post, models.Post.id, int(index))

    if not del_post:
        raise HTTPException(status_code=400, detail="Invalid post!")
    if del_post.user_id != int(cur_user):
        raise HTTPException(status_code=400, detail="Action not allowed!")

    db.delete(del_post)
    db.commit()

    return {"detail": "Delete successful!"}

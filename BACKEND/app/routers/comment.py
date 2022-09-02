from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from ..data import models, schemas
from ..utils import DryFunc

comment = APIRouter(prefix="/comment")


@comment.post("/create/{index}", status_code=201)
def create(index, create_comment: schemas.CommentBase, authorize: AuthJWT = Depends(),
           db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    cur_user = authorize.get_jwt_subject()
    content = create_comment.content

    comment_user = DryFunc.filter_one(db, models.User, models.User.id, int(cur_user))
    comment_post = DryFunc.filter_one(db, models.Post, models.Post.id, int(index))

    if not comment_user:
        raise HTTPException(status_code=400, detail="Invalid user!")
    if not comment_post:
        raise HTTPException(status_code=400, detail="Invalid post!")
    if len(content) < 1:
        raise HTTPException(status_code=400, detail="Content cannot be empty!")

    new_comment = models.Comment(content=content, user_id=comment_user.id, post_id=comment_post.id,
                                 username=comment_user.username, user_name=comment_user.name,
                                 user_pic=comment_user.profile_picture)

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {"detail": "Comment created!"}


@comment.get('/all/{page}', status_code=200)
def get(page, db: Session = Depends(DryFunc.get_db)):
    all_comments = DryFunc.get_all(db, models.Comment)

    page_comments = DryFunc.paginate(page, all_comments)

    return page_comments


@comment.get('/{index}', status_code=200, response_model=schemas.Comment)
def get(index, db: Session = Depends(DryFunc.get_db)):
    get_comment = DryFunc.filter_one(db, models.Comment, models.Comment.id, int(index))

    if not get_comment:
        raise HTTPException(status_code=400, detail="Invalid comment!")

    return get_comment


@comment.put('/update/{index}/{com_id}', status_code=200)
def update(index, com_id, up_comment: schemas.CommentBase, authorize: AuthJWT = Depends(),
           db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    content = up_comment.content
    cur_user = authorize.get_jwt_subject()

    cur_comment = DryFunc.filter_one(db, models.Comment, models.Comment.id, int(com_id))

    if not cur_comment:
        raise HTTPException(status_code=400, detail="Invalid comment!")
    if cur_comment.user_id != int(cur_user):
        raise HTTPException(status_code=400, detail="Action not allowed!")
    if cur_comment.post_id != int(index):
        raise HTTPException(status_code=400, detail="Invalid post!")
    if len(content) < 1:
        raise HTTPException(status_code=400, detail="Content cannot be empty!")

    cur_comment.content = content

    db.commit()
    db.refresh(cur_comment)

    return {"detail": "Update successful!"}


@comment.delete('/delete/{index}/{com_id}', status_code=200)
def delete(index, com_id, authorize: AuthJWT = Depends(), db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    cur_user = authorize.get_jwt_subject()

    del_comment = DryFunc.filter_one(db, models.Comment, models.Comment.id, int(com_id))

    if not del_comment:
        raise HTTPException(status_code=400, detail="Invalid comment!")
    if del_comment.user_id != int(cur_user):
        raise HTTPException(status_code=400, detail="Action not allowed!")
    if del_comment.post_id != int(index):
        raise HTTPException(status_code=400, detail="Invalid post!")

    db.delete(del_comment)
    db.commit()

    return {"detail": "Delete successful!"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError
import bcrypt
from fastapi_jwt_auth import AuthJWT
from ..data import models, schemas
from ..utils import DryFunc

admin = APIRouter(prefix="/admin")


@admin.post("/register", status_code=201)
def register(reg_admin: schemas.AdminCreate, db: Session = Depends(DryFunc.get_db)):
    admin_name = reg_admin.admin_name
    email = reg_admin.email
    password = reg_admin.password
    confirm_password = reg_admin.confirm_password

    same_admin_name = DryFunc.filter_one(db, models.Admin, models.Admin.admin_name, admin_name)
    same_email = DryFunc.filter_one(db, models.Admin, models.Admin.email, email)

    if len(admin_name) < 5:
        raise HTTPException(status_code=400, detail={"msg": "Admin name must be at least 5 characters!",
                                                     "success": False})
    if not admin_name.isalnum():
        raise HTTPException(status_code=400, detail={"msg": "Admin name must be alphanumeric!",
                                                     "success": False})
    if same_admin_name:
        raise HTTPException(status_code=409, detail={"msg": "Admin name already exists!",
                                                     "success": False})
    try:
        email = validate_email(email).email
    except EmailNotValidError:
        raise HTTPException(status_code=400, detail={"msg": "Email not valid!",
                                                     "success": False})
    if same_email:
        raise HTTPException(status_code=409, detail={"msg": "Email already exists!",
                                                     "success": False})
    if len(password) < 7:
        raise HTTPException(status_code=400, detail={"msg": "Password must be at least 7 characters!",
                                                     "success": False})
    if not password.isalnum():
        raise HTTPException(status_code=400, detail={"msg": "Password must be alphanumeric!",
                                                     "success": False})
    if password != confirm_password:
        raise HTTPException(status_code=400, detail={"msg": "Passwords don't match!",
                                                     "success": False})

    password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())

    new_admin = models.Admin(admin_name=admin_name, email=email, password=password)

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {"detail": {"msg": "Admin created!", "success": True}}


@admin.post("/login", status_code=200)
def login(log_admin: schemas.AdminAuth, db: Session = Depends(DryFunc.get_db), authorize: AuthJWT = Depends()):
    email = log_admin.email
    password = log_admin.password

    auth_admin = DryFunc.filter_one(db, models.Admin, models.Admin.email, email)

    if not auth_admin:
        raise HTTPException(status_code=400, detail={"msg": "Invalid login details!",
                                                     "success": False})
    if not bcrypt.checkpw(password.encode("UTF-8"), auth_admin.password):
        raise HTTPException(status_code=400, detail={"msg": "Invalid login details!",
                                                     "success": False})

    access_token = authorize.create_access_token(subject=auth_admin.id)
    refresh_token = authorize.create_refresh_token(subject=auth_admin.id)

    return {"detail": {"msg": "Login successful!", "access": access_token, "refresh": refresh_token,
                       "success": True}}


@admin.get('/current', status_code=200, response_model=schemas.Admin)
def get(authorize: AuthJWT = Depends(), db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    current_user = authorize.get_jwt_subject()
    cur_admin = DryFunc.filter_one(db, models.Admin, models.Admin.id, int(current_user))

    if not cur_admin:
        raise HTTPException(status_code=400, detail="Invalid admin!")

    return cur_admin


@admin.get('/all/{page}', status_code=200)
def get(page, authorize: AuthJWT = Depends(), db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    all_admins = DryFunc.get_all(db, models.Admin)

    page_admins = DryFunc.paginate(page, all_admins)

    return page_admins


@admin.get('/{index}', status_code=200, response_model=schemas.Admin)
def get(index, authorize: AuthJWT = Depends(), db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    get_admin = DryFunc.filter_one(db, models.Admin, models.Admin.id, int(index))

    if not get_admin:
        raise HTTPException(status_code=400, detail="Invalid admin!")

    return get_admin


@admin.put('/update', status_code=200)
def update(up_admin: schemas.AdminBase, authorize: AuthJWT = Depends(), db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    admin_name = up_admin.admin_name
    email = up_admin.email

    current_user = authorize.get_jwt_subject()
    cur_admin = DryFunc.filter_one(db, models.Admin, models.Admin.id,  int(current_user))
    same_admin_name = DryFunc.filter_one(db, models.Admin, models.Admin.admin_name, admin_name)
    same_email = DryFunc.filter_one(db, models.Admin, models.Admin.email, email)

    if not cur_admin:
        raise HTTPException(status_code=400, detail={"msg": "Invalid admin!",
                                                     "success": False})
    if len(admin_name) < 5:
        raise HTTPException(status_code=400, detail={"msg": "Admin name must be at least 5 characters!",
                                                     "success": False})
    if not admin_name.isalnum():
        raise HTTPException(status_code=400, detail={"msg": "Admin name must be alphanumeric!",
                                                     "success": False})
    if same_admin_name and same_admin_name != cur_admin:
        raise HTTPException(status_code=409, detail={"msg": "Admin name already exists!",
                                                     "success": False})
    try:
        email = validate_email(email).email
    except EmailNotValidError:
        raise HTTPException(status_code=400, detail={"msg": "Email not valid!",
                                                     "success": False})
    if same_email and same_email != cur_admin:
        raise HTTPException(status_code=409, detail={"msg": "Email already exists!",
                                                     "success": False})

    cur_admin.admin_name = admin_name
    cur_admin.email = email

    db.commit()
    db.refresh(cur_admin)

    return {"detail": {"msg": "Update successful!", "success": True}}


@admin.delete('/delete', status_code=200)
def delete(authorize: AuthJWT = Depends(), db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    current_user = authorize.get_jwt_subject()
    cur_admin = DryFunc.filter_one(db, models.Admin, models.Admin.id,  int(current_user))

    if not cur_admin:
        raise HTTPException(status_code=400, detail={"msg": "Invalid admin!",
                                                     "success": False})

    db.delete(cur_admin)
    db.commit()

    return {"detail": {"msg": "Delete successful!", "success": True}}


@admin.delete('/user/delete/{index}', status_code=204)
def delete(index, authorize: AuthJWT = Depends(), db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    del_user = DryFunc.filter_one(db, models.User, models.User.id, int(index))

    if not del_user:
        raise HTTPException(status_code=400, detail="Invalid user!")

    db.delete(del_user)
    db.commit()

    return {"detail": "Delete successful!"}


@admin.delete('/post/delete/{index}', status_code=204)
def delete(index, authorize: AuthJWT = Depends(), db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    del_post = DryFunc.filter_one(db, models.Post, models.Post.id, int(index))

    if not del_post:
        raise HTTPException(status_code=400, detail="Invalid post!")

    db.delete(del_post)
    db.commit()

    return {"detail": "Delete successful!"}


@admin.delete('/comment/delete/{index}', status_code=204)
def delete(index, authorize: AuthJWT = Depends(), db: Session = Depends(DryFunc.get_db)):
    DryFunc.authenticate(authorize)

    del_comment = DryFunc.filter_one(db, models.Post, models.Post.id, int(index))

    if not del_comment:
        raise HTTPException(status_code=400, detail="Invalid comment!")

    db.delete(del_comment)
    db.commit()

    return {"detail": "Delete successful!"}


@admin.post('/refresh')
def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()

    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}

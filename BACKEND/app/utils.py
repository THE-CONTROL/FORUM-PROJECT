from math import ceil
from .data.database import SessionLocal
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import HTTPException


class DryFunc:
    @staticmethod
    def get_all(db, model):
        return db.query(model).all()

    @staticmethod
    def filter_one(db, model, value, checker):
        return db.query(model).filter(value == checker).first()

    @staticmethod
    def update_many(db, model, value, checker, to_be_updated, updating_value):
        db.query(model).filter(value == checker).\
            update({to_be_updated: updating_value}, synchronize_session=False)

    @staticmethod
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    def authenticate(auth):
        try:
            auth.jwt_required()
        except AuthJWTException:
            raise HTTPException(status_code=400, detail="Not authenticated!")

    @staticmethod
    def paginate(page, items):
        items.reverse()
        page = int(page)
        page_size = 5
        start = (page - 1) * page_size
        if len(items) > start + page_size:
            end = start + page_size
        else:
            end = len(items)
        pages = ceil((len(items) / page_size))
        if page - 1 > 0:
            prev_page = page - 1
        else:
            prev_page = None
        if page + 1 > pages:
            next_page = None
        else:
            next_page = page + 1

        meta = {"page": page, "next_page": next_page, "prev_page": prev_page, "pages": list((range(1, pages+1))),
                "num_items": len(items), "last_item": end}

        new_items = items[start:end]

        info = {"meta": meta, "items": new_items}

        return info

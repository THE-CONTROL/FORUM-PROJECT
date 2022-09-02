from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import admin, user, post, comment
from app.data import models, database


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.admin)
app.include_router(user.user)
app.include_router(post.post)
app.include_router(comment.comment)


models.Base.metadata.create_all(bind=database.engine)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

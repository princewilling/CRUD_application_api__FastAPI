from fastapi import FastAPI, Depends
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import user, post, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine) we now have alembic 

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)        

app.include_router(post.router)

app.include_router(user.router)

app.include_router(auth.router)

app.include_router(vote.router)

@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}

@app.get("/")
async def root():
    return{"message": "welcome to my api"}





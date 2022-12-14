from ..schema import schemas
from ..db import models
from .. import utils
from fastapi import Body, FastAPI, Depends, Response, status, HTTPException, APIRouter
from ..db.database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    user_exp = db.query(models.User).filter(models.User.email == user.email).first()
    
    if user_exp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email already exist, kindly login"
        )
    
    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(
        **user.dict()
    )
    # post = models.Post(
    #     title=post.title, content=post.content, published=post.published
    # )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    
    return user
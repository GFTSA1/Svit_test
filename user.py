from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
import models, utils, schemas
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    user_dict = user.model_dump()

    user_dict.pop("password")
    user_dict["hashed_password"] = hashed_password
    new_user = models.User(**user_dict)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

from fastapi import FastAPI, status, HTTPException, Depends, APIRouter, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import models, utils, oath2

router = APIRouter(
    prefix="/login",
    tags=["Authentication"],
)


@router.post("/")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.username == user_credentials.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )
    if not utils.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Credentials"
        )
    access_token = oath2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

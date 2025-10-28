from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import SessionLocal

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

# @router.post("/signup")
# def create_user(email: str,password: str,name: str, db: Session = Depends(SessionLocal)):
#     # hash the password here before storing it
#     hashed_password = hash_password(password)
#     db_user = db.query(models.User).filter(models.User.email == email).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     new_user = models.User(email=email, hashed_password=password, name=name)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


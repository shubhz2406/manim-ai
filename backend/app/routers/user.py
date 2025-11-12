from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import SessionLocal

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


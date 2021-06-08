from sqlalchemy.orm import Session
from utils import models
#from . import schemas


def get_user(db: Session, user_token: str):
    return db.query(models.User).filter(models.User.user_token == user_token).first()


def get_user_by_name(db: Session, users_name: str):
    return db.query(models.User).filter(models.User.users_name == users_name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = utils.models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
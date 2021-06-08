from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from utils.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    users_name = Column(String, unique=True, index=True)
    user_token = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    sms = relationship("SMS", backref='sms', cascade='all,delete-orphan')

class SMS(Base):
    __tablename__ = "sms"
    id_sms = Column(String, primary_key=True, index=True)
    from_sms = Column(String)
    to_sms = Column(String)
    body_sms = Column(String)
    id_user = Column(Integer, ForeignKey("users.id"))
    #owner = relationship("User", back_populates="sms")
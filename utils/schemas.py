from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    users_name: str


class UserCreate(UserBase):
    password: str

class SMSBase(BaseModel):
    from_sms: str
    to_sms: str
    body_sms: str

class SMS(SMSBase):
    id: int
    owner_id: int

class SMS(BaseModel):
    id_sms: str
    from_sms: str
    to_sms: str
    body_sms: str

class User(UserBase):
    id: int
    users_name: str
    user_token: str
    hashed_password: str
    is_active: bool
    sms: List[SMS] = []

    class Config:
        orm_mode = True
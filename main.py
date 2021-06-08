from fastapi import Security, Depends, FastAPI, HTTPException, Header, Response, status
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from pydantic import BaseModel

import os
import hmac
import hashlib
import base64
import json
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse, PlainTextResponse

from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

import crud
import models
import schemas

from database import SessionLocal, Base, engine

from typing import Optional

Base.metadata.create_all(bind=engine)

API_TOKEN_KEY = "1234567asdfgh"
API_TOKEN_NAME = "X-Api-Token"
API_SIG_NAME = "X-App-Access-Sig"
COOKIE_DOMAIN = "127.0.0.1"

api_key_header_token = APIKeyHeader(name=API_TOKEN_NAME, auto_error=False)


async def get_api_key(
    api_key_header_token: str = Security(api_key_header_token),
):
    if api_key_header_token == API_TOKEN_KEY:
        return api_key_header_token
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except OperationalError as err:
        print(err.detail)
    finally:
        db.close()

@app.get("/")
async def homepage():
    return "Welcome to the security test!"


#@app.get("/logout")
#async def route_logout_and_remove_cookie():
#    response = RedirectResponse(url="/")
#    response.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
#    return response


@app.get("/openapi.json", tags=["documentation"])
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
    )
    return response


@app.get("/documentation", tags=["documentation"])
async def get_documentation(api_key: APIKey = Depends(get_api_key)):
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    response.set_cookie(
        API_TOKEN_NAME,
        value=api_key,
        domain=COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response

@app.get("/secure_endpoint", tags=["test"])
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = "Защищенный режим..."
    return response

@app.get("/users/{user_token}", response_model=schemas.User)
def read_user(user_token: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_token=user_token)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/post", response_model=schemas.SMS, tags=["Save SMS message"], status_code=status.HTTP_201_CREATED)
async def create_sms(sms: schemas.SMS, request: Request, db: Session = Depends(get_db)):
    user = crud.get_user(db, request.headers['x-api-token']);
    data = str(request.headers['x-app-access-ts']).encode('utf-8') + user.hashed_password.encode('utf-8') + json.dumps(sms.dict()).encode('utf-8');
    hm = hmac.new(bytes(user.hashed_password, 'UTF-8'), data, hashlib.sha256).hexdigest();
    if (hm == request.headers['x-app-access-sig']) and (user.is_active):
        db_SMS = models.SMS(id_sms=sms.id_sms, from_sms=sms.from_sms, to_sms=sms.to_sms, body_sms=sms.body_sms, id_user=user.id)
        #db.add(db_SMS)
        #db.commit()
        #db.refresh(db_SMS)
        #return sms
        return sms
    raise HTTPException(status_code=401)
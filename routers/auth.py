from fastapi import FastAPI, Body, status, HTTPException,Depends,APIRouter
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Optional
from datetime import date,datetime
import json
import random
from passlib.context import CryptContext
from database import engine, SessionLocal, get_db
import tables
import schema
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from routers import inventory,users
import oauth2
import utilities
from utilities import hash_password,verify_password


newapp = APIRouter(tags=["auth"])


@newapp.post("/verifyuser")
async def verifylogin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(tables.users).filter(tables.users.email == form_data.username).first()
    if user and utilities.verify_password(form_data.password, user.password):
        access_token = oauth2.create_access_token(data={"user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials")
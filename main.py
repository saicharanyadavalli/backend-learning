from fastapi import FastAPI, Body, status, HTTPException,Depends
from fastapi.responses import JSONResponse
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
from routers import inventory,users,auth

tables.Base.metadata.create_all(engine)

today = date.today()
date_str = today.strftime("%d-%m-%y")
time = today.strftime("%H:%M:%S")

try:
    connection = psycopg2.connect(user="postgres",
                                  password="password",
                                  host="localhost",
                                  port="5432",
                                  database="fastapi",
                                cursor_factory=RealDictCursor)
    cursor = connection.cursor()
    print("database connection is succesfull")
except Exception as error:
    print("database connection is not succesfull and failed")
    print(error)

app = FastAPI()

app.include_router(inventory.router_inventory)
app.include_router(users.router_user)
app.include_router(auth.newapp)


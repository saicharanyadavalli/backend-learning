from fastapi import FastAPI, Body, status, HTTPException,Depends,APIRouter
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

router_user = APIRouter(prefix="/users", tags=["users"])

passlib = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router_user.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.userout)
async def createuser(post : schema.userout, db: Session = Depends(get_db)):
    hashed_password = passlib.hash(post.password)
    post.password = hashed_password
    user = tables.users(
        email = post.email,
        password = post.password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router_user.get("/{id}",response_model=schema.userout,status_code=status.HTTP_200_OK)
async def get_user( id : int ,db: Session = Depends(get_db)):
    users = db.query(tables.users).filter(tables.users.id == id).first()
    if users:
        return users
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
@router_user.delete("/delete/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_item(id : int, db: Session = Depends(get_db)):
    product = db.query(tables.users).filter(tables.users.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{id}' not found"
        )
    
    db.delete(product)
    db.commit()
    return {"message": f"Product '{id}' deleted successfully"}
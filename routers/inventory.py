from fastapi import FastAPI, Body, status, HTTPException,Depends,APIRouter
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import date,datetime
import json
import random
from passlib.context import CryptContext
from database import engine, SessionLocal, get_db
import tables
import oauth2
import schema
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

router_inventory = APIRouter(prefix="/inventory", tags=["inventory"])

@router_inventory.get("/")
async def get_inventory(db: Session = Depends(get_db),user_id = Depends(oauth2.get_current_user)):
    products = db.query(tables.Inventory).all()
    return(products)

@router_inventory.get("/{item}",response_model=schema.replyback)
async def get_inventory(item : str,db: Session = Depends(get_db),user_id = Depends(oauth2.get_current_user)):
    product = db.query(tables.Inventory).filter(tables.Inventory.productname == item).first()
    if product:
        return product
    else:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

@router_inventory.post("/add", status_code=status.HTTP_201_CREATED, response_model=schema.replyback)
async def add_product(post: schema.InventorySchema, db: Session = Depends(get_db),user_id = Depends(oauth2.get_current_user)):
    new_product = tables.Inventory(
        orderdate=post.orderdate,
        productname=post.productname,
        productdesc=post.productdesc,
        cost=post.cost,
        quantity=post.quantity,
        payment=post.payment,
        seller=post.seller,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return JSONResponse(content={"message": "Product added"}, status_code=status.HTTP_201_CREATED)

@router_inventory.delete("/delete/{item}", status_code=status.HTTP_200_OK)
async def delete_item(item: str, db: Session = Depends(get_db),user_id = Depends(oauth2.get_current_user)):
    product = db.query(tables.Inventory).filter(tables.Inventory.productname == item).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{item}' not found"
        )
    
    db.delete(product)
    db.commit()
    return {"message": f"Product '{item}' deleted successfully"}

@router_inventory.patch("/update/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_item(id: int, updates: dict = Body(...), db: Session = Depends(get_db),user_id = Depends(oauth2.get_current_user)):
    product = db.query(tables.Inventory).filter(tables.Inventory.ordernumber == id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found"
        )

    for key, value in updates.items():
        if hasattr(product, key):
            setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return {"message": "Product updated successfully", "updated_product": product}
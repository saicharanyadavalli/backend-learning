from fastapi import FastAPI, Body, status, HTTPException,Depends
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
from datetime import date,datetime
import json
import random
from passlib.context import CryptContext
from database import engine, SessionLocal, get_db
import models
import database
import schema
from pydantic import Field, constr
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

models.Base.metadata.create_all(engine)
passlib = CryptContext(schemes=["bcrypt"], deprecated="auto")


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



products = []

@app.get("/test")
def testposts(db: Session = Depends(get_db)):
    return{"status" : "success"}


@app.get("/sqlinventory",response_model=schema.replyback)
async def get_inventory(db: Session = Depends(get_db)):
    products = db.query(models.Inventory).all()
    return(products)

from typing import List
@app.get("/inventory")
async def get_inventory():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    products = [dict(product) for product in products]

    return JSONResponse(
        content=json.loads(json.dumps(products, indent=4))  # pretty format
    )

#@app.get("/inventory/names")
#async def get_inventory_names():   
#    cursor.execute("""SELECT productname FROM products""")
#    products = cursor.fetchall() 
#    return {"product_names": products}

@app.get("/inventory/{item}")
async def get_inventory_item(item: str):
    cursor.execute("""SELECT * FROM products WHERE productname = %s""", (item,))
    product = cursor.fetchone()
    if product:
        return product
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

@app.post("/sqladd")
async def add_product(post: schema.InventorySchema, db: Session = Depends(get_db)):

    new_product = models.Inventory(
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

@app.post("/add")
async def add_product(text: dict = Body(...)):
    cursor.execute("""
        INSERT INTO products (orderdate, productname, productdesc, cost, quantity, payment, seller)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        date_str,
        text["productname"],
        text["productdesc"],
        text["cost"],
        text["quantity"],
        text["payment"],
        text["seller"]
    ))
    connection.commit()


    return JSONResponse(content={"message": "Product added"}, status_code=status.HTTP_201_CREATED)

@app.delete("/sqldelete/{item}", status_code=status.HTTP_200_OK)
async def delete_item(item: str, db: Session = Depends(get_db)):
    product = db.query(models.Inventory).filter(models.Inventory.productname == item).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{item}' not found"
        )
    
    db.delete(product)
    db.commit()
    return {"message": f"Product '{item}' deleted successfully"}

@app.delete("/delete/{item}")
async def delete_item(item: str):
    try:
        cursor.execute("""DELETE FROM products WHERE productname = %s""", (item,))
        connection.commit()
        return JSONResponse(content={"message": "Product deleted"}, status_code=status.HTTP_200_OK)
    
    except Exception as error:
        return JSONResponse(content={"message": "Product not found"}, status_code=status.HTTP_404_NOT_FOUND)
        print(error)

@app.patch("/sqlupdate/{id}", status_code=status.HTTP_200_OK)
async def update_item(id: int, updates: dict = Body(...), db: Session = Depends(get_db)):
    product = db.query(models.Inventory).filter(models.Inventory.ordernumber == id).first()

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

@app.patch("/update/{id}")
async def update_item(id: int, updates: dict = Body(...)):
    try:
        for key, value in updates.items():
            cursor.execute(f"UPDATE products SET {key} = %s WHERE ordernumber = %s", (value, id))
        connection.commit()
        return JSONResponse(content={"message": "Product edited"}, status_code=status.HTTP_200_OK)

    except Exception as error:
        connection.rollback()
        return JSONResponse(content={"message": str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

@app.post("/user",status_code=status.HTTP_201_CREATED,response_model=schema.userout)
async def createuser(post : schema.userout, db: Session = Depends(get_db)):
    hashed_password = passlib.hash(post.password)
    post.password = hashed_password
    user = models.users(
        email = post.email,
        password = post.password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
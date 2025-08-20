from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class Inventory(Base):
    __tablename__ = "products"

    ordernumber = Column(Integer, primary_key=True, nullable=False)   
    orderdate = Column(String, nullable=False)
    productname = Column(String, nullable=False)
    productdesc = Column(String, nullable=True)
    cost = Column(Integer, nullable=False)  
    quantity = Column(Integer, nullable=False)  
    payment = Column(Boolean, default=False,server_default='TRUE')   
    seller = Column(String, nullable=False)
    dateandtime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class users(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())



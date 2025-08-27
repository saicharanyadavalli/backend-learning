from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime
from pydantic import Field  
class InventorySchema(BaseModel):
    ordernumber: Optional[int] = None
    orderdate: str
    productname: str
    productdesc: str
    cost: int = Field(gt=0)
    quantity: int = Field(gt=0)
    payment: Optional[bool] = False
    seller: str
    dateandtime: Optional[datetime] = None 

    class Config:
        from_attributes = True

class replyback(BaseModel):
    productname: str
    productdesc: str
    cost: int
    quantity: int
    class Config:
        from_attributes = True

class userout(BaseModel):
    email : EmailStr
    password : str
    created_at : Optional[datetime] = None
    class Config:
        from_attributes = True

class verify(BaseModel):
    email : EmailStr
    password : str
    class Config:
        from_attributes = True

class verifyout(BaseModel):
    email : EmailStr
    class Config:
        from_attributes = True

class token(BaseModel):
    access_token : str
    token_type : str

class tokendata(BaseModel):
    user_id : Optional[int] = None
    email : Optional[EmailStr] = None
    class Config:
        from_attributes = True


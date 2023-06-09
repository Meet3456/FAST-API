from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):              # Backend sends the message to frontend that what the data should look like i.e {datatype of data} , What user should send the input in:
    title : str
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id :int
    created_at : datetime
    owner_id : int


    class Config:
        orm_mode = True

class UserCreate(BaseModel):

    email : EmailStr
    password : str

    
class Userout(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):

    access_token = str
    token_type = str

class TokenData(BaseModel):

    id : Optional[str] = None
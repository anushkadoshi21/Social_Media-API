from datetime import datetime
from pydantic import BaseModel
from pydantic.networks import EmailStr
from sqlalchemy import orm
from sqlalchemy.sql.sqltypes import Integer
from typing import Optional

class Post(BaseModel):
    title:str
    content:str 
    is_published:bool=True
    #rating:Optional[int]=None

class User_out(BaseModel):
    id:int
    email:EmailStr 
    created_at:datetime
    class Config:
        orm_mode=True


class response_post(BaseModel):
    title:str
    content:str 
    is_published:bool=True 
    user_id:int
    id:int
    created_at:datetime
    owner:User_out
    class Config:
        orm_mode=True

class Post_out(BaseModel):
    Post:response_post
    Votes:int 
    class Config:
        orm_mode=True

class User(BaseModel):
    email:EmailStr
    password:str 

class Token(BaseModel):
    access_token:str
    token_type:str="Bearer"

class TokenData(BaseModel):
    id:Optional[int]=None

class Postid(BaseModel):
    id:int 
    class Config:
        orm_mode=True
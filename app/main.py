from typing import Optional,List
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.datastructures import Default
from fastapi.params import Body
from pydantic import BaseModel
from sqlalchemy.sql.functions import mode
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from app.routers.votes import vote
from . import schema
from . import  models,utils
from sqlalchemy.orm import Session
from .database import  engine,get_db
from .routers import posts,users,auth,votes
models.Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message":"Hey Wyd"}

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(votes.router)
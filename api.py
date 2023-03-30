from tkinter import NONE
from typing import Optional
from fastapi import FastAPI , Response , status , HTTPException , Depends
from fastapi.params import Body
from pydantic import BaseModel,DictError
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas , utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .router import posts,users,auth

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# CONNECTING TO A DATABASE


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='Fastapi', user='postgres', password='Meet0987',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break

    except Exception as error:
        print("Connection to database failed")
        print("Error:",error)
        time.sleep(3)


my_posts = [{"title":"title of post 1" , "content": "content of post 1" , "id":1},{"title":"My favorite food" , "content":"fire pizza" , "id":2}]


def find_posts(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_posts(id):
    for i , p in enumerate(my_posts):
        if p['id'] == id:
            return i
        
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

# Request - get , path (url) : "/"
@app.get("/")
def root():
    return {"message": "Hello , Welcome to my server!!!!"}














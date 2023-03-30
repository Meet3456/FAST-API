from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,utils,oauth2
from .. database import get_db
from typing import List
from tkinter import NONE


router = APIRouter(
    prefix="/posts",
    tags=['POSTS']
)


# RETREVING ALL POSTS:


@router.get("/" , response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


# CREATING A NEW_POST:(BY CONNECTING TO A DATABASE)


@router.post("/", status_code=status.HTTP_201_CREATED , response_model=schemas.Post)
def create_posts(posts : schemas.PostCreate,db: Session = Depends(get_db),current_user: int= Depends(oauth2.get_current_user) ):                # storing the class "Post" in variable posts:
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(posts.title,posts.content,posts.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id = current_user.id , **posts.dict()) # type: ignore

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post 


# GETTING A INDIVIDUAL POST WITH PARTICULAR ID:(BY CONNECTING TO A DATABASE)


@router.get("/{id}" , response_model=schemas.Post)
def get_post(id: int , db: Session = Depends(get_db),user_id: int= Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
     
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail={'message': f"post with id {id} not found"})

    return post


# DELETING A POST:(BY CONNECTING TO A DATABASE)


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_posts(id: int , db: Session = Depends(get_db) , user_id: int= Depends(oauth2.get_current_user)):    

    # index = cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)),)
    # conn.commit()
  
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == NONE:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id : {id} does not exist ")
    
    post.delete(synchronize_session=False)
    db.commit()

    return {'message':'post was suucessfully deleted!'}


# UPDATING A POST:


@router.put("/{id}")
def update_posts(id:int , updated_post: schemas.Post , db: Session = Depends(get_db) , user_id: int= Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    post_query.update(**updated_post.dict() , synchronize_session=False)

    db.commit()
from re import L
from unittest import result
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import oauth2
from app.oauth2 import get_current_user
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts" ,
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                  Limit: int = 10, skip:int = 0, search: Optional[str] = ""):

    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
   
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter= True).group_by(models.Post.id
                                                                                                                                                                         ).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    
    return posts

# @router.get("/me", response_model=List[schemas.Post])
# def get_my_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
#                  Limit: int = 10, skip:int = 0, search: Optional[str] = ""):

#     posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).limit(Limit).all()

#     for item in posts:
#         if item.owner_id != current_user.id:
#             raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail='You can only see your posts!')
#     # cursor.execute("""SELECT * FROM posts """)
#     # posts = cursor.fetchall()
#     return posts

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id= current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @router.get("/me/{id}", response_model=schemas.Post)
# def get_user_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

#     post = db.query(models.Post).filter(models.Post.id == id).first()
    
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    
#     if post.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail='Not authorized to perform requested action')


#     return post

@router.get("/{id}", response_model=schemas.PostOut)
def get_all_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id==id).first()

    post =  db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter= True).group_by(models.Post.id
                                                ).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail='Not authorized to perform requested action')


    return post



@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   
    post_query = db.query(models.Post).filter(models.Post.id == id)
  
    post= post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id {id} doesnt exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action')

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)) )
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id {id} doesnt exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action')

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

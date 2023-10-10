from fastapi import FastAPI, HTTPException, status, Response, Depends
from pydantic import BaseModel
import time

import psycopg2
from sqlalchemy.orm import session
from . import models
from .database import engine, get_db

# Create database table
models.Base.metadata.create_all(bind=engine)

# Create app
app = FastAPI()


@app.get("/sqlalchemy")
def get_post(db: session = Depends(get_db)):
    return {"Status": "Successfull Connection!!!"}

#========================================================
#   """ USING PSYCOPG LIBRARY """
# connect to database
while(True):
    try:
        conn = psycopg2.connect(database="fastapi", user="postgres", password="Smileok21")
        cursor = conn.cursor()
        print("Success connection")
        break
    except Exception as error:
        print("Connect failed")
        print(f"Error: {error}")
        time.sleep(2)




# define model
class Post(BaseModel):
    title: str
    content: str | None
    published: bool = True


@app.get("/posts")
def get_posts():
    cursor.execute("""
                   SELECT * FROM posts;
                   """)
    posts = cursor.fetchall()
    return {"Posts": posts}


@app.get("/post/lastest")
def get_last_post():
    cursor.execute("""
                   SELECT * FROM  posts;
                   """)
    lastest_post = cursor.fetchall()[-1]
    return {"Lastest post": lastest_post}


@app.get('/post/{id}')
def get_post(id: int):
    cursor.execute("""
                   SELECT * FROM posts
                   WHERE id = %s;""", str(id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Not found post {id}")
    return {"post": post}


@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""
                   INSERT INTO posts (title, content, published) 
                   VALUES (%s, %s, %s) RETURNING *;""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return new_post


@app.put("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_post(id: int, post: Post):
    cursor.execute("""
                   UPDATE posts
                   SET title = %s, content = %s, published = %s
                   WHERE id = %s 
                   RETURNING *;""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Not found post {id}")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/post/{id}")
def delete_post(id: int):
    cursor.execute("""
                   DELETE FROM posts
                   WHERE id = %s RETURNING *;""", str(id))
    deleted_post = cursor.fetchone() 
    conn.commit()   

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not found post {id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# # ====================================================


# def find_post(id: int) -> Post:
#     for post in my_posts:
#         if post['id'] == id:
#             return post
#     return None
        

# def find_index_post(id: int) -> int:
#     for i, post in enumerate(my_posts):
#         if post['id'] == id:
#             return i
#     return None




# @app.post("/post") 
# def create_post(paras: Data):
#     return f"Title: {paras.title}, Content: {paras.content}, Pushlish: {paras.pushlish}, Number: {paras.number}"

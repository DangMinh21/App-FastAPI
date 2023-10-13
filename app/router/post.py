from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db

router = APIRouter()


@router.post("/post", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(post: schemas.PostIn, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db)):
    all_post = db.query(models.Post).all()
    return all_post


@router.get("/post/lastest", response_model=schemas.PostOut)
def get_last_post(db: Session = Depends(get_db)):
    print("debub")
    lastest_post = db.query(models.Post).all()[-1]
    return lastest_post


@router.get('/post/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post {id} not found")
    return post


@router.put("/post/{id}", response_model=schemas.PostOut)
def update_post(id: int, post: schemas.PostIn, db: Session = Depends(get_db)):
    query_post = db.query(models.Post).filter(models.Post.id == id)

    if not query_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Not found post {id}")
    
    query_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return query_post.first()
    

@router.delete("/post/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first(): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not found post {id}")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
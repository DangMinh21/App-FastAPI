from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from ..database import get_db

router = APIRouter()

@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):

    # hash password
    user.password = utils.hash_password(user.password)

    # save user in the database
    new_user = models.User(**(user.model_dump()))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 

@router.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    got_user = db.query(models.User).filter(models.User.id == id).first()

    if not got_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'this user {id} does not exist')
    
    return got_user
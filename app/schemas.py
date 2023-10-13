from pydantic import BaseModel, EmailStr

from datetime import datetime



# define post schema
class BasePost(BaseModel):
    title: str
    content: str | None
    published: bool = True # optional

class PostIn(BasePost):
    pass

class PostOut(BasePost):
    id: int
    create_at: datetime

    class Config:
        from_attributes = True

# define user schema
class BaseUser(BaseModel):
    email: EmailStr
    
class UserIn(BaseUser):
    password: str

class UserOut(BaseUser):
    id: int
    created_at: datetime

    class Congif:
        from_attributes = True

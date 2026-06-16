from typing import Literal, Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime
class PostBase(BaseModel):
    content:str
    title:str
    published:bool = True
class PostsCreate(PostBase):
    pass

class Post(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:"UserOut"

class PostOut(Post):
    pass

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id:Optional[int] = None

class Vote(BaseModel):
    post_id:int
    dir:Literal[0,1]

class PostOut(BaseModel):
    Post: Post
    votes:int
    
    model_config = {"from_attributes":True}


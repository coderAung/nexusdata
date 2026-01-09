from datetime import datetime
from typing import Generic, TypeVar
from pydantic import BaseModel


class AccountInfo(BaseModel):
    id:int
    name:str
    email:str
    role:str

class AuthenticationResult(BaseModel):
    access_token:str
    access_type:str = "Bearer"
    account_info:AccountInfo

class SignInForm(BaseModel):
    email:str
    password:str

class SignUpForm(BaseModel):
    name:str
    email:str
    password:str

I = TypeVar("I")
class ModificationResult(BaseModel, Generic[I]):
    id:I

class PostForm(BaseModel):
    content:str

class PostItem(BaseModel):
    id:int
    content:str
    created_at:datetime
    account_name:str
    comments:int

class CommentForm(BaseModel):
    content:str
    post_id:int

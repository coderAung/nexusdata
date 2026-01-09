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

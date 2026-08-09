from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class UserCreate(SQLModel): 
    email: EmailStr 
    pwd: str 

class UserPreview(SQLModel): 
    id: int 
    email: EmailStr 

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    password_hash: str = Field() 
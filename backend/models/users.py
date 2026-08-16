from sqlmodel import SQLModel, Field
from pydantic import EmailStr
import uuid
from datetime import datetime

class UserCreate(SQLModel): 
    email: EmailStr 
    pwd: str 

class UserPreview(SQLModel): 
    id: int 
    email: EmailStr 

class User(SQLModel, table=True):
    __tablename__ = "users"

    # doing int | None makes it generate automatically
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    password_hash: str = Field() 

class UserSession(SQLModel, table=True): 
    __tablename__ = "sessions"
    # generates a random id thats unique
    session_id: int | None = Field(default=None, primary_key=True)
    access_token: str = Field(default_factory=lambda: uuid.uuid4().hex, unique=True, index=True)
    user_id: int = Field(foreign_key="users.id")
    session_start: datetime = Field(default_factory=datetime.now)
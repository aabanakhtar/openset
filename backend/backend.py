from fastapi import Depends, HTTPException, Query, FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session 
import sqlalchemy
from sqlmodel import select
from contextlib import asynccontextmanager
from typing import Annotated
import bcrypt

from db import *
from models import (
    User, 
    UserCreate, 
    UserPreview
)

production = False
allowed_origins = ["http://localhost:3000"]
if production: 
    allowed_origins = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    pass

# the session where sqlite stages everything
SessionDep = Annotated[Session, Depends(get_session_lazy)]

app = FastAPI(lifespan=lifespan)
# allows requests from certain origins (i guess so people dont use ur api mailicously)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins, 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

def hash_user_pwd(pwd: str) -> str:
    bytes = pwd.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes, salt)
    return hashed.decode()

@app.post("/users")
def create_user(user_data: UserCreate, session: SessionDep) -> UserPreview:
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user: 
        raise HTTPException(status_code=409, detail="User already found!")

    user = User(
        email=user_data.email, 
        password_hash=hash_user_pwd(user_data.pwd)
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return UserPreview(email=user.email, id=user.id)

@app.get("/users")
def get_users(session: SessionDep) -> list[UserPreview]:
    users = session.exec(select(User)).all()
    return [
        UserPreview(email=user.email, id=user.id) for user in users
    ]


@app.get("/health")
def root():
    return {"status": "happy birthday"}
from fastapi import (
    APIRouter,
    HTTPException
)
from models import (
    User, UserCreate, UserPreview
)
from db import (
    SessionDep
)
from sqlmodel import (
    select
)

import bcrypt

# tags for docs
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

def hash_user_pwd(pwd: str) -> str:
    '''Hashes a user password'''

    bytes = pwd.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes, salt)
    return hashed.decode()

@router.post("/create")
def create_user(user_data: UserCreate, session: SessionDep) -> UserPreview:
    '''Creates a user using data from the frontend'''

    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    # If the user exists, it's not the one to make
    if existing_user: 
        raise HTTPException(status_code=409, detail="User already found!")

    # Create and commit user
    user = User(
        email=user_data.email, 
        password_hash=hash_user_pwd(user_data.pwd)
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return UserPreview(email=user.email, id=user.id)
from fastapi import Depends, APIRouter, HTTPException, Response 
from models.users import User, UserCreate, UserPreview, UserSession
from sqlmodel import select
from typing import Annotated
# We use this primarily to handle the token bearing for us
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
import bcrypt, db 


# tags for docs
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

'''
Utilities for authentication
Hashing related stuff
'''

def hash_user_pwd(pwd: str) -> str:
    '''Hashes a user password'''
    bytes = pwd.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes, salt)
    return hashed.decode()

def check_pwd(pwd: str, hashed_pwd: str) -> str: 
    '''Returns True if the password is correct'''
    return bcrypt.checkpw(pwd.encode('utf-8'), hashed_pwd.encode('utf-8'))

'''
Authentication related routes
'''
@router.post("/create")
def create_user(user_data: UserCreate, session: db.SessionDep) -> UserPreview:
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


@router.post("/login")
def login_user(db: db.SessionDep, login_values: OAuth2PasswordRequestForm = Depends()): 
    '''Logs in the user using OAuth2 features and returns a session token'''
    user: User = db.exec(select(User).where(User.email == login_values.username)).first()
    # ensure the user exists or the form is correct password
    if not user or not check_pwd(login_values.password, user.password_hash):
        raise HTTPException(401, detail="Unable to login user: incorrect email or password.") 

    session = UserSession(user_id=user.id)
    db.add(session)
    db.commit()
    db.refresh(session)

    # access token return according to OAuth2 spec so we can use the fastapi tester stuff
    return {
        "access_token": session.access_token, 
        "token_type": "bearer"
    }

# how we get the token out
bearer_scheme = HTTPBearer()

def get_current_user(token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)], db: db.SessionDep) -> User: 
    '''Allows us to reference authenticated users in other routes'''
    session = db.exec(select(UserSession).where(UserSession.access_token == token.credentials)).first()
    if not session: 
        raise HTTPException(
            401, "Not authenticated"
        ) 

    # get the user referenced in the session
    user = db.exec(select(User).where(User.id == session.user_id)).first()
    if not user: 
        raise HTTPException(
            401, "Not authenticated"
        )

    return user

@router.delete("/signout", status_code=204)
def signout(db: db.SessionDep, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    '''Signs out the user and deletes their session via token'''
    # extract the session token and relevant columns
    token = credentials.credentials
    session: UserSession = db.exec(select(UserSession).where(UserSession.access_token == token)).first()
    # we don't care then.
    if not session:
        return None

    db.delete(session)
    db.commit()
    # nothing to return really
    return None

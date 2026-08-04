from fastapi import Depends, HTTPException, Query, FastAPI 
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy.orm import sessionmaker, Session 
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import Annotated

production = False

allowed_origins = ["http://localhost:3000"]


if production: 
    allowed_origins = []


sqlite_file_name = "test.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# use the same sqlite db in different threads (one request can use more than one thread)
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

class User(SQLModel, table=True):
    email: str = Field(primary_key=True, unique=True)
    password_hash: str = Field() 

def create_db_and_tables(): 
    SQLModel.metadata.create_all(engine)

def get_session_lazy():
    with Session(engine) as session:
        yield session


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

@app.post("/users")
def create_user(user: User, session: SessionDep) -> User:
    try: 
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, detail="Couldn't create user")

@app.get("/users")
def get_users(session: SessionDep,) -> list[User]:
    users = session.execute(select(User)).scalars()
    return users


@app.get("/health")
def root():
    return {"status": "happy birthday"}

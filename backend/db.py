from sqlmodel import (
    Session, 
    SQLModel, 
    create_engine
)

from typing import (
    Annotated
)
from fastapi import (
    Depends
)

DATABASE_LOCATION = "databse.db"
sqlite_url = f"sqlite:///{DATABASE_LOCATION}"


# use the same sqlite db in different threads (one request can use more than one thread)
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)
# the session where sqlite stages everything


def create_db_and_tables(): 
    SQLModel.metadata.create_all(engine)

def get_session_lazy():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session_lazy)]
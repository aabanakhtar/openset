from sqlmodel import Session, SQLModel, create_engine

DATABASE_LOCATION = "test.db"
sqlite_url = f"sqlite:///{DATABASE_LOCATION}"


# use the same sqlite db in different threads (one request can use more than one thread)
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables(): 
    SQLModel.metadata.create_all(engine)

def get_session_lazy():
    with Session(engine) as session:
        yield session
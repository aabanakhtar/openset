
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from db import (
    create_db_and_tables
) 
from models.users import (
    User, 
    UserCreate, 
    UserPreview
)
from routers import (
    auth, 
    users,
    requests
)


production = False
allowed_origins = ["http://localhost:5173"]
if production: 
    allowed_origins = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    pass

app = FastAPI(lifespan=lifespan)
# allows requests from certain origins (i guess so people dont use ur api mailicously)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins, 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(requests.router)


@app.get("/health")
def root():
    return {"status": "happy birthday"}
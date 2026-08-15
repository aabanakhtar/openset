from fastapi import (
    APIRouter
)
from db import (
    SessionDep
)
from models import (
    User, 
    UserPreview
)
from sqlmodel import (
    select
)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/list")
def get_users(session: SessionDep) -> list[UserPreview]:
    users = session.exec(select(User)).all()
    return [
        UserPreview(email=user.email, id=user.id) for user in users
    ]

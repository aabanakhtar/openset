from fastapi import APIRouter
from models.users import User, UserPreview
from sqlmodel import select
import db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/list")
def get_users(session: db.SessionDep) -> list[UserPreview]:
    users = session.exec(select(User)).all()
    return [
        UserPreview(email=user.email, id=user.id) for user in users
    ]

from routers.auth import get_current_user 
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from models.users import User
from sqlmodel import select 
from models.requests import RecommendationRequestBase, RecommendationRequest, RequestStatus, RecommendationType
import db


router = APIRouter(prefix="/requests", tags=["requests"])

@router.post("/", status_code=200)
def create_request(request: RecommendationRequestBase, db: db.SessionDep, current_user: Annotated[User, Depends(get_current_user)]): 
    '''Creates a recommendation letter request'''

    new_request = RecommendationRequest(
        purpose=request.purpose,
        recommender_name=request.recommender_name, 
        recommender_email=request.recommender_email, 
        user_id=current_user.id 
    )

    # add the rec request
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

@router.get("/")
def get_request_list(db: db.SessionDep, current_user: Annotated[User, Depends(get_current_user)]) -> list[RecommendationRequestBase]:
    '''Gets the list of recommendation requests the user has made'''
    request_list = db.exec(select(RecommendationRequest).
                           where(RecommendationRequest.user_id == current_user.id)).all()

    if not request_list:
        return Response(status_code=204)

    return [
        x for x in request_list
    ]

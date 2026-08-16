from enum import Enum
from sqlmodel import Field, SQLModel
from datetime import datetime
from pydantic import EmailStr
import uuid

class RecommendationType(str, Enum): 
    job = "work"
    academic = "academic"
    scholarship = "scholarship"
    general = "general"

class RequestStatus(str, Enum): 
    pending = "pending"
    drafting = "drafting"
    submitted = "submitted"

class RecommendationRequestBase(SQLModel): 
    '''Base class for all recommendation requests'''
    purpose: RecommendationType 
    recommender_name: str 
    recommender_email: EmailStr 


class RecommendationRequest(RecommendationRequestBase, table=True): 
    __tablename__ = "requests"
    # unique id
    id: int | None = Field(default=None, primary_key=True)
    status: RequestStatus = Field(
        default=RequestStatus.pending, 
        description="Must be RequestStatus"
    )
    # foreign key connects this to the user who made the request
    user_id: int = Field(foreign_key="users.id", index=True)
    # purpose of the rec letter 
    # SUPERCLASS stuff
    purpose: RecommendationType = Field(
        default=RecommendationType.general, 
        description="Must be either work, academic, scholarship, or general" # meta data for fastapi
    )
    # recommender details 
    recommender_name: str = Field() 
    recommender_email: str = Field()

    access_token: str = Field(default_factory=lambda: uuid.uuid4().hex, unique=True)
    # auto generate the time of the request
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
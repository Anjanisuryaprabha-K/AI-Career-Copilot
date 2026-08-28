from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ApplicationCreate(BaseModel):
    company: str
    role: str
    job_url: Optional[str] = ""
    location: Optional[str] = "Remote / On-site"
    salary: Optional[str] = ""
    status: Optional[str] = "Applied" # Wishlist, Applied, Online Assessment, Interview, Offer, Rejected
    application_date: Optional[str] = None
    deadline: Optional[str] = ""
    notes: Optional[str] = ""
    match_score: Optional[int] = 85

class ApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    job_url: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[str] = None
    notes: Optional[str] = None
    match_score: Optional[int] = None

class StageUpdateRequest(BaseModel):
    app_id: str
    new_stage: str

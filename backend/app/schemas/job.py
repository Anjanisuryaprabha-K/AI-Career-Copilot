from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ReadinessCalcRequest(BaseModel):
    resume_score: Optional[float] = 85.0
    coding_score: Optional[float] = 80.0
    interview_score: Optional[float] = 85.0
    github_score: Optional[float] = 80.0

class SalaryPredictRequest(BaseModel):
    target_role: str = "Full Stack Developer"
    skills: Optional[List[str]] = ["Python", "React"]
    experience: Optional[str] = "Fresher (0-2 years)"
    location: Optional[str] = "India"
    company_name: Optional[str] = None

class SaveJobRequest(BaseModel):
    job_id: str
    saved: bool = True

class MatchJobsRequest(BaseModel):
    target_role: Optional[str] = "Full Stack Developer"
    skills: Optional[List[str]] = None
    location: Optional[str] = "India"
    experience_level: Optional[str] = "All"
    remote_type: Optional[str] = "All"  # "All", "Remote", "Hybrid", "On-Site"
    min_salary: Optional[float] = 0.0
    required_skill: Optional[str] = "All"
    sort_by: Optional[str] = "match_score"  # "match_score", "relevance"

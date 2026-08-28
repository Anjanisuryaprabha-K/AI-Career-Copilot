from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from app.services.resume_export_service import ResumeExportService

router = APIRouter(prefix="/api/v1/resume-export", tags=["ATS Resume Exporter"])

class ExportRequest(BaseModel):
    user_name: Optional[str] = "Preetham V"
    email: Optional[str] = "preetham@placement.edu"
    skills: Optional[List[str]] = ["Python", "FastAPI", "React", "MongoDB", "Data Structures"]

@router.post("/generate-latex")
async def export_latex(req: ExportRequest):
    return {"status": "success", "data": ResumeExportService.generate_latex_resume(req.user_name or "Preetham V", req.email or "preetham@placement.edu", req.skills)}

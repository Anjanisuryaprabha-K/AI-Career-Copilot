from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Dict, Any
from app.schemas.job import ReadinessCalcRequest, SalaryPredictRequest, SaveJobRequest
from app.services.google_search_service import GoogleSearchService
from app.repositories.job_repository import job_repository
from app.dependencies.auth import get_optional_user, resolve_user_id

router = APIRouter(prefix="/api/v1/jobs", tags=["Jobs & Readiness"])

@router.get("/roles")
async def get_roles():
    return {
        "status": "success",
        "roles": [
            "Full Stack Developer",
            "Backend Developer",
            "Frontend Developer",
            "Software Engineer",
            "AI/ML Engineer",
            "Data Engineer",
            "Cloud / DevOps Engineer"
        ]
    }

@router.get("/readiness")
async def get_job_readiness(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = resolve_user_id(user)
    from app.services.job_readiness_service import JobReadinessService
    return await JobReadinessService.compute_user_readiness(user_id)

@router.post("/calculate-readiness")
async def calculate_readiness(payload: ReadinessCalcRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = resolve_user_id(user)
    from app.services.job_readiness_service import JobReadinessService
    
    # Compute central dynamic readiness score
    readiness_data = await JobReadinessService.compute_user_readiness(user_id)
    
    # If payload contains custom overrides, adjust
    if payload.resume_score is not None or payload.coding_score is not None:
        r_score = payload.resume_score if payload.resume_score is not None else readiness_data["weighting_breakdown"]["resume_score"]["score"]
        c_score = payload.coding_score if payload.coding_score is not None else readiness_data["weighting_breakdown"]["coding_score"]["score"]
        i_score = payload.interview_score if payload.interview_score is not None else readiness_data["weighting_breakdown"]["interview_score"]["score"]
        g_score = payload.github_score if payload.github_score is not None else readiness_data["weighting_breakdown"]["profile_score"]["score"]
        
        overall = round((r_score * 0.35) + (c_score * 0.30) + (i_score * 0.20) + (g_score * 0.15), 1)
        readiness_data["overall_readiness_score"] = overall
        readiness_data["overall_readiness_index"] = overall
        readiness_data["tier"] = "Tier-1 / Dream Company Ready" if overall >= 85 else "Placement Ready"

    return readiness_data

@router.post("/predict-salary")
async def predict_salary(payload: SalaryPredictRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = resolve_user_id(user)
    prediction = await GoogleSearchService.predict_salary_range(
        role=payload.target_role,
        skills=payload.skills or [],
        experience=payload.experience or "Fresher",
        location=payload.location or "India",
        company=payload.company_name
    )
    await job_repository.save_salary_prediction(
        user_id=user_id,
        payload=payload.dict(),
        prediction=prediction,
        sources=prediction.get("data_sources", [])
    )
    return prediction

@router.get("/recommendations")
async def get_job_recommendations(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = resolve_user_id(user)
    
    # Retrieve user's latest resume analysis & profile data from MongoDB
    from app.repositories.resume_repository import resume_repository
    from app.services.job_matching_service import JobMatchingService

    latest_scan = await resume_repository.get_latest_user_scan(user_id)
    
    user_skills = []
    if user and user.get("skills"):
        user_skills.extend(user.get("skills"))
    if latest_scan:
        user_skills.extend(latest_scan.get("matched_keywords", []))
        struct_skills = latest_scan.get("structured_extraction", {}).get("skills", {})
        if isinstance(struct_skills, dict):
            user_skills.extend(struct_skills.get("technical", []))
            user_skills.extend(struct_skills.get("tools", []))
    
    if not user_skills:
        user_skills = ["Python", "FastAPI", "React", "MongoDB", "Data Structures", "REST APIs"]
    user_skills = list(dict.fromkeys(user_skills))

    user_edu = latest_scan.get("structured_extraction", {}).get("education", []) if latest_scan else []
    user_exp = latest_scan.get("structured_extraction", {}).get("experience", []) if latest_scan else []
    user_proj = latest_scan.get("structured_extraction", {}).get("projects", []) if latest_scan else []
    
    experience_level = "Intermediate"
    if user and user.get("profile"):
        experience_level = user.get("profile", {}).get("experienceLevel", "Intermediate")

    target_role = user.get("target_role", "Software Engineer") if user else "Software Engineer"

    search_res = await GoogleSearchService.search(f"{target_role} hiring Bangalore Hyderabad remote 2026", search_type="jobs", limit=8)
    raw_listings = search_res.get("results", [])

    formatted_jobs = []
    for idx, j in enumerate(raw_listings):
        meta = j.get("metadata", {})
        job_item = {
            "id": f"job_{idx + 1}",
            "_id": f"job_{idx + 1}",
            "title": j.get("title", f"{target_role} - Tech Enterprise"),
            "company": meta.get("company", "Top Tech Enterprise"),
            "location": meta.get("location", "Hyderabad / Bengaluru / Remote"),
            "salary": meta.get("salary", "₹16 - ₹24 LPA"),
            "experience": meta.get("experience", "0-2 Years"),
            "skills": meta.get("skills", ["Python", "React", "FastAPI", "MongoDB"]),
            "url": j.get("url", "https://careers.google.com"),
            "source": j.get("source", "Company Careers Portal"),
            "snippet": j.get("snippet", ""),
            "saved": False
        }
        matched = JobMatchingService.calculate_job_match(
            job=job_item,
            user_skills=user_skills,
            target_role=target_role,
            user_education=user_edu,
            user_experience=user_exp,
            user_projects=user_proj,
            experience_level=experience_level
        )
        formatted_jobs.append(matched)

    formatted_jobs.sort(key=lambda item: item["match_score"], reverse=True)
    await job_repository.save_user_job_matches(user_id, formatted_jobs)
    return {"status": "success", "jobs": formatted_jobs}

@router.post("/save-job")
async def save_job(payload: SaveJobRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = resolve_user_id(user)
    await job_repository.toggle_save_job(user_id, payload.job_id, payload.saved)
    return {"status": "success", "message": f"Job saved status updated to {payload.saved} in MongoDB."}

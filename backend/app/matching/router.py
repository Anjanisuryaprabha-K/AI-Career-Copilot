from fastapi import APIRouter, Depends
from typing import Optional, List, Dict, Any
from app.schemas.job import MatchJobsRequest
from app.services.google_search_service import GoogleSearchService, DOMAIN_KNOWLEDGE_BASE
from app.services.job_matching_service import JobMatchingService
from app.repositories.job_repository import job_repository
from app.repositories.resume_repository import resume_repository
from app.dependencies.auth import get_optional_user

router = APIRouter(prefix="/api/v1/matching", tags=["Job Matching AI"])

@router.post("/match-jobs")
async def match_jobs(payload: MatchJobsRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    
    # 1. Retrieve user's latest resume analysis & profile data from MongoDB
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
    if payload.skills:
        user_skills.extend(payload.skills)
    
    # Fallback default skills if no profile/resume skills exist
    if not user_skills:
        user_skills = ["Python", "FastAPI", "React", "MongoDB", "Data Structures", "REST APIs"]
    
    user_skills = list(dict.fromkeys(user_skills))

    user_edu = latest_scan.get("structured_extraction", {}).get("education", []) if latest_scan else []
    user_exp = latest_scan.get("structured_extraction", {}).get("experience", []) if latest_scan else []
    user_proj = latest_scan.get("structured_extraction", {}).get("projects", []) if latest_scan else []
    
    experience_level = "Intermediate"
    if user and user.get("profile"):
        experience_level = user.get("profile", {}).get("experienceLevel", "Intermediate")

    role = payload.target_role or (user.get("target_role") if user else "Software Engineer")
    loc = payload.location or "India"

    # 2. Search real listings via GoogleSearchService & Domain knowledge base
    search_data = await GoogleSearchService.search(f"{role} jobs {loc} 2026", search_type="jobs", limit=10)
    raw_listings = search_data.get("results", [])

    raw_jobs = []
    for idx, item in enumerate(raw_listings):
        meta = item.get("metadata", {})
        raw_jobs.append({
            "id": f"match_{idx + 1}",
            "_id": f"match_{idx + 1}",
            "title": item.get("title", f"{role} Opportunity"),
            "company": meta.get("company", "Tech Enterprise"),
            "location": meta.get("location", loc),
            "salary": meta.get("salary", "₹18 - ₹26 LPA"),
            "experience": meta.get("experience", "0-2 Years"),
            "skills": meta.get("skills", ["Python", "React", "FastAPI", "MongoDB", "SQL"]),
            "url": item.get("url", "https://careers.google.com"),
            "source": item.get("source", "Verified Careers Portal"),
            "snippet": item.get("snippet", "")
        })

    # If search produced few results, supplement with domain knowledge base jobs
    if len(raw_jobs) < 5:
        for cat in DOMAIN_KNOWLEDGE_BASE["jobs"]:
            for idx, listing in enumerate(cat["listings"]):
                raw_jobs.append({
                    "id": f"domain_job_{idx + 1}",
                    "_id": f"domain_job_{idx + 1}",
                    "title": f"{listing['title']} - {listing['company']}",
                    "company": listing["company"],
                    "location": listing["location"],
                    "salary": listing["salary"],
                    "experience": listing["experience"],
                    "skills": listing["skills"],
                    "url": listing["url"],
                    "source": listing["source"],
                    "snippet": listing["snippet"]
                })

    # Deduplicate jobs by title & company
    seen = set()
    unique_jobs = []
    for j in raw_jobs:
        key = (j["title"].lower(), j["company"].lower())
        if key not in seen:
            seen.add(key)
            unique_jobs.append(j)

    # 3. Calculate personalized match metrics for each job
    computed_matches = []
    for job in unique_jobs:
        match_obj = JobMatchingService.calculate_job_match(
            job=job,
            user_skills=user_skills,
            target_role=role,
            user_education=user_edu,
            user_experience=user_exp,
            user_projects=user_proj,
            experience_level=experience_level
        )
        computed_matches.append(match_obj)

    # 4. Filter and sort matched jobs based on user payload options
    final_matches = JobMatchingService.filter_and_sort_jobs(
        matched_jobs=computed_matches,
        role_filter=payload.target_role,
        location_filter=payload.location,
        remote_filter=payload.remote_type,
        experience_filter=payload.experience_level,
        min_salary_filter=payload.min_salary,
        required_skill_filter=payload.required_skill,
        sort_by=payload.sort_by or "match_score"
    )

    # 5. Persist matched jobs to MongoDB for user
    await job_repository.save_user_job_matches(user_id, final_matches)

    return {
        "status": "success",
        "target_role": role,
        "total_matched": len(final_matches),
        "user_context_used": {
            "user_id": user_id,
            "skills_count": len(user_skills),
            "experience_level": experience_level,
            "resume_education_found": len(user_edu) > 0,
            "resume_projects_found": len(user_proj)
        },
        "scoring_weights": {
            "skills_match": "35%",
            "role_alignment": "25%",
            "experience_match": "15%",
            "education_match": "15%",
            "projects_depth": "10%"
        },
        "matched_jobs": final_matches
    }

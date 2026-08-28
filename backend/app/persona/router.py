import re
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.repositories.user_repository import user_repository
from app.dependencies.auth import get_optional_user

router = APIRouter(prefix="/api/v1/persona", tags=["Persona & Role Classifier"])

class DetectRoleRequest(BaseModel):
    resume_text: str
    target_role_override: Optional[str] = None

class UpdateRoleOverrideRequest(BaseModel):
    role_name: str
    track_id: Optional[str] = None

ROLE_TAXONOMY = {
    "Python Backend Engineer": {
        "track_id": "backend",
        "keywords": ["python", "fastapi", "django", "flask", "postgresql", "mysql", "redis", "docker", "rest api", "microservices", "asyncio", "sqlalchemy"],
        "standard_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis", "REST APIs", "Microservices", "Git"]
    },
    "MERN Specialist": {
        "track_id": "mern",
        "keywords": ["react", "node.js", "express", "mongodb", "javascript", "typescript", "redux", "tailwind", "next.js", "jwt"],
        "standard_skills": ["React", "Node.js", "Express", "MongoDB", "JavaScript", "TypeScript", "Tailwind CSS", "REST APIs"]
    },
    "Full Stack Developer": {
        "track_id": "mern",
        "keywords": ["full stack", "react", "node.js", "python", "fastapi", "sql", "mongodb", "docker", "javascript", "html", "css"],
        "standard_skills": ["React", "FastAPI", "Node.js", "MongoDB", "PostgreSQL", "JavaScript", "Python", "Docker"]
    },
    "Frontend Developer": {
        "track_id": "mern",
        "keywords": ["react", "javascript", "typescript", "html5", "css3", "tailwind", "redux", "next.js", "ui/ux", "vite", "webpack"],
        "standard_skills": ["React", "JavaScript", "TypeScript", "Tailwind CSS", "HTML5", "CSS3", "Redux", "REST APIs"]
    },
    "AI/ML Engineer": {
        "track_id": "backend",
        "keywords": ["pytorch", "tensorflow", "machine learning", "deep learning", "nlp", "llm", "pandas", "numpy", "scikit-learn", "python", "transformers"],
        "standard_skills": ["Python", "PyTorch", "TensorFlow", "Scikit-Learn", "NLP", "Pandas", "NumPy", "FastAPI"]
    },
    "DevOps / Cloud Engineer": {
        "track_id": "backend",
        "keywords": ["docker", "kubernetes", "aws", "ci/cd", "terraform", "linux", "github actions", "prometheus", "grafana", "bash", "ansible"],
        "standard_skills": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux", "Terraform", "GitHub Actions", "Python"]
    },
    "Software Engineer (DSA Focus)": {
        "track_id": "dsa",
        "keywords": ["data structures", "algorithms", "c++", "java", "python", "dynamic programming", "graphs", "trees", "sorting"],
        "standard_skills": ["Data Structures", "Algorithms", "C++", "Java", "Python", "System Design", "SQL", "Git"]
    }
}

def classify_persona(resume_text: str, override_role: Optional[str] = None) -> Dict[str, Any]:
    text_lower = resume_text.lower()

    if override_role and override_role in ROLE_TAXONOMY:
        best_role = override_role
        best_info = ROLE_TAXONOMY[override_role]
        score = 100
    else:
        # Score each role against resume text
        role_scores = {}
        for role, data in ROLE_TAXONOMY.items():
            matches = 0
            for kw in data["keywords"]:
                if re.search(r"\b" + re.escape(kw) + r"\b", text_lower):
                    matches += 1
            role_scores[role] = matches

        best_role = max(role_scores, key=role_scores.get)
        best_matches = role_scores[best_role]
        if best_matches == 0:
            best_role = "Full Stack Developer"
            best_info = ROLE_TAXONOMY["Full Stack Developer"]
            score = 65
        else:
            best_info = ROLE_TAXONOMY[best_role]
            score = min(98, round((best_matches / max(1, len(best_info["keywords"]))) * 100) + 40)

    # Extract detected top skills
    top_skills = []
    for skill in best_info["standard_skills"]:
        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text_lower):
            top_skills.append(skill)
    if not top_skills:
        top_skills = best_info["standard_skills"][:4]

    # Identify missing skill gaps
    skill_gaps = [s for s in best_info["standard_skills"] if s not in top_skills]
    if not skill_gaps:
        skill_gaps = ["System Design", "Distributed Caching", "CI/CD Pipelines"]

    # Determine seniority level
    years_match = re.search(r"(\d+)\+?\s*years?\s*(of)?\s*experience", text_lower)
    experience_level = "Intermediate"
    if years_match:
        yrs = int(years_match.group(1))
        if yrs >= 5: experience_level = "Advanced"
        elif yrs <= 1: experience_level = "Beginner"
    elif "senior" in text_lower or "lead" in text_lower or "architect" in text_lower:
        experience_level = "Advanced"
    elif "intern" in text_lower or "student" in text_lower or "fresh" in text_lower:
        experience_level = "Beginner"

    return {
        "detectedRole": best_role,
        "experienceLevel": experience_level,
        "topSkills": top_skills,
        "skillGaps": skill_gaps,
        "recommendedTrack": best_info["track_id"],
        "confidenceScore": score,
        "isInitialized": True,
        "updatedAt": datetime.utcnow().isoformat()
    }

@router.post("/detect-role")
async def detect_role(payload: DetectRoleRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    email = user.get("email", "") if user else ""

    profile_data = classify_persona(payload.resume_text, payload.target_role_override)
    target = email or user_id
    
    updated_user = await user_repository.update(target, {"profile": profile_data, "target_role": profile_data["detectedRole"]})
    
    return {
        "status": "success",
        "message": f"Candidate classified as '{profile_data['detectedRole']}' with {profile_data['confidenceScore']}% confidence.",
        "profile": profile_data,
        "user": updated_user
    }

@router.post("/update-role")
async def update_role_override(payload: UpdateRoleOverrideRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    email = user.get("email", "") if user else ""

    existing_profile = user.get("profile", {}) if user else {}
    target_track = payload.track_id or ROLE_TAXONOMY.get(payload.role_name, {}).get("track_id", "mern")

    updated_profile = {
        **existing_profile,
        "detectedRole": payload.role_name,
        "recommendedTrack": target_track,
        "isInitialized": True,
        "updatedAt": datetime.utcnow().isoformat()
    }

    target = email or user_id
    updated_user = await user_repository.update(target, {"profile": updated_profile, "target_role": payload.role_name})

    return {
        "status": "success",
        "message": f"Target persona updated to '{payload.role_name}'.",
        "profile": updated_profile,
        "user": updated_user
    }

@router.get("/me")
async def get_my_persona(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    if not user:
        return {"status": "uninitialized", "profile": {"isInitialized": False}}
    
    profile = user.get("profile")
    if not profile or not profile.get("isInitialized"):
        return {
            "status": "uninitialized",
            "profile": {
                "detectedRole": user.get("target_role", "Software Engineer"),
                "experienceLevel": "Not Analyzed",
                "topSkills": user.get("skills", []),
                "skillGaps": [],
                "recommendedTrack": "dsa",
                "isInitialized": False
            }
        }

    return {
        "status": "success",
        "profile": profile
    }


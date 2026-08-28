from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List, Dict, Any
from app.schemas.user import UserCreate, UserLogin, ProfileUpdateRequest, UserSettingsUpdate
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    is_valid_email_format
)
from app.repositories.user_repository import user_repository
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication & Profile"])

@router.post("/register")
async def register(payload: UserCreate):
    email_clean = payload.email.strip().lower()
    if not is_valid_email_format(email_clean):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format. Please check your email address."
        )
    
    if len(payload.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long."
        )
    
    existing = await user_repository.get_by_email(email_clean)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists. Please sign in."
        )
    
    hashed_pwd = hash_password(payload.password)
    user_doc = {
        "name": payload.name.strip(),
        "email": email_clean,
        "hashed_password": hashed_pwd,
        "target_role": payload.target_role or "Software Engineer",
        "readiness_score": 80.0,
        "skills": ["Python", "FastAPI", "React", "MongoDB", "Data Structures"],
        "location": "India",
        "experience": "Student / Fresh Graduate",
        "education": "B.Tech Computer Science",
        "github": "",
        "linkedin": "",
        "portfolio": ""
    }
    
    saved_user = await user_repository.create(user_doc)
    user_id = str(saved_user.get("_id", saved_user.get("id", "")))
    
    token = create_access_token(data={"sub": user_id, "email": email_clean})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "name": saved_user["name"],
            "email": saved_user["email"],
            "target_role": saved_user["target_role"],
            "readiness_score": saved_user["readiness_score"],
            "skills": saved_user["skills"],
            "location": saved_user.get("location", ""),
            "experience": saved_user.get("experience", ""),
            "education": saved_user.get("education", ""),
            "github": saved_user.get("github", ""),
            "linkedin": saved_user.get("linkedin", ""),
            "portfolio": saved_user.get("portfolio", ""),
            "created_at": saved_user.get("created_at", "")
        }
    }

@router.post("/login")
async def login(payload: UserLogin):
    email_clean = payload.email.strip().lower()
    if not is_valid_email_format(email_clean):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format. Please check your email and password."
        )
    
    user = await user_repository.get_by_email(email_clean)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account found with this email. Please register first."
        )
    
    if not verify_password(payload.password, user.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials. Please verify your email and password."
        )
    
    user_id = str(user.get("_id", user.get("id", "")))
    token = create_access_token(data={"sub": user_id, "email": email_clean})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "name": user["name"],
            "email": user["email"],
            "target_role": user.get("target_role", "Software Engineer"),
            "readiness_score": user.get("readiness_score", 80.0),
            "skills": user.get("skills", []),
            "location": user.get("location", ""),
            "experience": user.get("experience", ""),
            "education": user.get("education", ""),
            "github": user.get("github", ""),
            "linkedin": user.get("linkedin", ""),
            "portfolio": user.get("portfolio", ""),
            "settings": user.get("settings", {})
        }
    }

@router.get("/me")
async def get_me(user: Dict[str, Any] = Depends(get_current_user)):
    user_id = str(user.get("_id", user.get("id", "")))
    return {
        "status": "success",
        "user": {
            "id": user_id,
            "name": user.get("name", "User"),
            "email": user.get("email", ""),
            "target_role": user.get("target_role", "Software Engineer"),
            "readiness_score": user.get("readiness_score", 80.0),
            "skills": user.get("skills", []),
            "location": user.get("location", ""),
            "experience": user.get("experience", ""),
            "education": user.get("education", ""),
            "github": user.get("github", ""),
            "linkedin": user.get("linkedin", ""),
            "portfolio": user.get("portfolio", ""),
            "settings": user.get("settings", {}),
            "created_at": user.get("created_at", "")
        }
    }

@router.put("/profile")
async def update_user_profile(payload: ProfileUpdateRequest, user: Dict[str, Any] = Depends(get_current_user)):
    user_id = str(user.get("_id", user.get("id", "")))
    email = user.get("email", "")
    
    updates = {}
    if payload.name is not None:
        updates["name"] = payload.name.strip()
    if payload.target_role is not None:
        updates["target_role"] = payload.target_role.strip()
    if payload.skills is not None:
        updates["skills"] = payload.skills
    if payload.location is not None:
        updates["location"] = payload.location.strip()
    if payload.experience is not None:
        updates["experience"] = payload.experience.strip()
    if payload.education is not None:
        updates["education"] = payload.education.strip()
    if payload.github is not None:
        updates["github"] = payload.github.strip()
    if payload.linkedin is not None:
        updates["linkedin"] = payload.linkedin.strip()
    if payload.portfolio is not None:
        updates["portfolio"] = payload.portfolio.strip()
    if payload.readiness_score is not None:
        updates["readiness_score"] = payload.readiness_score
        
    updated = await user_repository.update(email or user_id, updates) or user
    return {
        "status": "success",
        "message": "Profile updated successfully in MongoDB.",
        "user": {
            "id": str(updated.get("_id", user_id)),
            "name": updated.get("name", ""),
            "email": updated.get("email", ""),
            "target_role": updated.get("target_role", ""),
            "readiness_score": updated.get("readiness_score", 80.0),
            "skills": updated.get("skills", []),
            "location": updated.get("location", ""),
            "experience": updated.get("experience", ""),
            "education": updated.get("education", ""),
            "github": updated.get("github", ""),
            "linkedin": updated.get("linkedin", ""),
            "portfolio": updated.get("portfolio", "")
        }
    }

@router.get("/settings")
async def get_user_settings(user: Dict[str, Any] = Depends(get_current_user)):
    return {
        "status": "success",
        "settings": user.get("settings", {
            "theme": "dark",
            "notifications": True,
            "target_roles": [user.get("target_role", "Software Engineer")],
            "preferred_locations": ["Remote", "Bengaluru", "Hyderabad"],
            "remote_preference": True
        })
    }

@router.put("/settings")
async def update_user_settings(payload: UserSettingsUpdate, user: Dict[str, Any] = Depends(get_current_user)):
    user_id = str(user.get("_id", user.get("id", "")))
    settings_dict = {
        "theme": payload.theme,
        "notifications": payload.notifications,
        "target_roles": payload.target_roles or [user.get("target_role", "Software Engineer")],
        "preferred_locations": payload.preferred_locations or ["Remote", "Bengaluru"],
        "remote_preference": payload.remote_preference,
        "privacy_settings": payload.privacy_settings or {}
    }
    await user_repository.update_settings(user_id, settings_dict)
    return {
        "status": "success",
        "message": "Settings updated successfully in MongoDB.",
        "settings": settings_dict
    }

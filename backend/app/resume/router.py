from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from typing import Optional, List, Dict, Any
from app.utils.resume_parser import ResumeParser
from app.services.live_ats_scorer import LiveATSScorer
from app.repositories.resume_repository import resume_repository
from app.repositories.user_repository import user_repository
from app.dependencies.auth import get_optional_user
from app.schemas.resume import TextAnalysisRequest, BulletRewriteRequest, BenchmarkSearchRequest

router = APIRouter(prefix="/api/v1/resume", tags=["Resume & ATS Analyzer"])

@router.post("/analyze-text")
async def analyze_resume_text(payload: TextAnalysisRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    if not payload.resume_text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resume text cannot be empty.")
    
    from app.persona.router import classify_persona
    
    result = LiveATSScorer.calculate_live_score(
        resume_text=payload.resume_text,
        target_role=payload.target_role or "Software Engineer",
        custom_jd=payload.custom_jd or "",
        company_name=payload.company_name or ""
    )
    
    # Auto-classify candidate persona & update profile in MongoDB
    persona_data = classify_persona(payload.resume_text, payload.target_role)
    result["detected_persona"] = persona_data

    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    user_email = user.get("email", "demo@placement.edu") if user else "demo@placement.edu"
    
    target = user_email or user_id
    await user_repository.update(target, {
        "profile": persona_data,
        "target_role": persona_data["detectedRole"],
        "skills": persona_data["topSkills"]
    })

    saved = await resume_repository.save_scan(
        user_id=user_id,
        user_email=user_email,
        target_role=persona_data["detectedRole"],
        scan_data=result,
        resume_preview=payload.resume_text[:200]
    )
    result["scan_id"] = str(saved.get("_id", saved.get("id", "")))
    result["persisted_in_mongodb"] = True
    return {"status": "success", "data": result, "profile": persona_data}

@router.post("/analyze-file")
@router.post("/upload")
async def analyze_resume_file(
    file: UploadFile = File(...),
    target_role: str = Form("Software Engineer"),
    custom_jd: str = Form(""),
    company_name: str = Form(""),
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty.")

    filename_lower = (file.filename or "").lower()
    if filename_lower and not (filename_lower.endswith(".pdf") or filename_lower.endswith(".docx") or filename_lower.endswith(".txt")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file format. Please upload a .pdf or .docx document.")

    extracted_text = ResumeParser.extract_text_auto(contents, filename=file.filename or "")
    if not extracted_text.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Could not extract readable text from the file.")

    from app.persona.router import classify_persona

    # Auto-classify candidate persona & update profile in MongoDB
    persona_data = classify_persona(extracted_text, target_role if target_role != "Software Engineer" else None)

    result = LiveATSScorer.calculate_live_score(
        resume_text=extracted_text,
        target_role=persona_data["detectedRole"],
        custom_jd=custom_jd,
        company_name=company_name
    )
    result["extracted_text_preview"] = extracted_text[:800] + "..."
    result["detected_persona"] = persona_data

    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    user_email = user.get("email", "demo@placement.edu") if user else "demo@placement.edu"

    target = user_email or user_id
    await user_repository.update(target, {
        "profile": persona_data,
        "target_role": persona_data["detectedRole"],
        "skills": persona_data["topSkills"]
    })

    await resume_repository.save_resume_file(
        user_id=user_id,
        filename=file.filename or "resume.pdf",
        content_type=file.content_type or "application/pdf",
        parsed_text=extracted_text,
        ats_score=result["overall_score"]
    )
    saved_scan = await resume_repository.save_scan(
        user_id=user_id,
        user_email=user_email,
        target_role=persona_data["detectedRole"],
        scan_data=result,
        resume_preview=extracted_text[:200]
    )
    result["scan_id"] = str(saved_scan.get("_id", saved_scan.get("id", "")))
    result["persisted_in_mongodb"] = True

    return {"status": "success", "filename": file.filename, "data": result, "profile": persona_data}

@router.post("/benchmark-search")
async def search_role_benchmarks(payload: BenchmarkSearchRequest):
    benchmarks = LiveATSScorer.discover_role_benchmarks(
        target_role=payload.target_role,
        custom_jd=payload.custom_jd or "",
        company_context=payload.company_name or ""
    )
    return {
        "status": "success",
        "target_role": payload.target_role,
        "company_name": payload.company_name or "General Industry",
        "total_benchmarks_found": len(benchmarks),
        "benchmarks": benchmarks
    }

@router.get("/history")
async def get_scan_history(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    scans = await resume_repository.get_user_scans(user_id, limit=30)
    return {"status": "success", "user_id": user_id, "scans": scans}

@router.get("/history/{scan_id}")
@router.get("/scan/{scan_id}")
async def get_single_scan(scan_id: str, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    scans = await resume_repository.get_user_scans(user_id, limit=50)
    found = next((s for s in scans if str(s.get("_id", s.get("id", ""))) == scan_id), None)
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume analysis record not found.")
    return {"status": "success", "user_id": user_id, "scan": found}

@router.post("/rewrite-bullet")
async def rewrite_bullet_point(payload: BulletRewriteRequest):
    raw = payload.bullet_point.strip()
    verb = payload.action_verb or "Engineered"
    rewritten = f"{verb} scalable microservices and data pipelines, optimizing throughput by 38% and reducing latency for 50k+ active users."
    return {
        "original": raw,
        "suggested_rewrite": rewritten
    }

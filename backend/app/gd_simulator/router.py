from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from app.services.gd_service import GDService
from app.dependencies.auth import get_optional_user

router = APIRouter(prefix="/api/v1/gd", tags=["AI Group Discussion Simulator"])

class GenerateTopicRequest(BaseModel):
    category: str = "Technology"
    difficulty: str = "Medium"
    duration_minutes: int = 5

class EvaluateGDRequest(BaseModel):
    topic_title: str
    category: str = "Technology"
    difficulty: str = "Medium"
    duration_minutes: int = 5
    user_transcript: str

@router.get("/categories")
async def get_gd_categories():
    return {
        "status": "success",
        "categories": GDService.get_categories()
    }

@router.get("/topics")
async def get_gd_topics(
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None)
):
    topics = GDService.get_topics(category, difficulty)
    return {
        "status": "success",
        "topics": topics
    }

@router.post("/generate-topic")
async def generate_gd_topic(payload: GenerateTopicRequest):
    topics = GDService.get_topics(payload.category, payload.difficulty)
    if topics:
        selected_topic = topics[0]
    else:
        selected_topic = {
            "id": "gen_custom",
            "title": f"The Impact of {payload.category} Innovation on Modern Industry Frameworks",
            "difficulty": payload.difficulty,
            "background": f"As {payload.category.lower()} rapidly evolves, industry leaders debate strategic alignment and governance.",
            "key_angles": ["Strategic adoption", "Risk management", "Skill readiness"]
        }

    participants = GDService.generate_simulated_participants(selected_topic["title"], payload.category)

    return {
        "status": "success",
        "topic": selected_topic,
        "participants": participants,
        "duration_minutes": payload.duration_minutes,
        "disclaimer": "NOTICE: Group discussion topics are curated for communication practice and do not represent exact company exam questions."
    }

@router.post("/evaluate")
async def evaluate_gd_session(
    payload: EvaluateGDRequest,
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    res = await GDService.evaluate_gd_session(
        user_id=user_id,
        topic_title=payload.topic_title,
        category=payload.category,
        difficulty=payload.difficulty,
        duration_minutes=payload.duration_minutes,
        user_transcript=payload.user_transcript
    )

    if res.get("status") == "error":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res.get("error"))

    return res

@router.post("/evaluate-audio")
async def evaluate_gd_audio(
    file: UploadFile = File(...),
    topic_title: str = Form(...),
    category: str = Form("Technology"),
    difficulty: str = Form("Medium"),
    duration_minutes: int = Form(5),
    user_transcript: Optional[str] = Form(None),
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    audio_bytes = await file.read()

    transcript_text = user_transcript or "I believe that when evaluating this topic, balancing innovation with strategic governance is key to long-term success."

    res = await GDService.evaluate_gd_session(
        user_id=user_id,
        topic_title=topic_title,
        category=category,
        difficulty=difficulty,
        duration_minutes=duration_minutes,
        user_transcript=transcript_text,
        audio_bytes=audio_bytes,
        filename=file.filename or ""
    )

    if res.get("status") == "error":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res.get("error"))

    return res

@router.get("/history")
async def get_gd_history(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    history = await GDService.get_user_gd_history(user_id)
    return {
        "status": "success",
        "history": history
    }

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List, Dict, Any
import uuid
from app.schemas.chat import ChatMessagePayload
from app.services.google_search_service import GoogleSearchService
from app.services.placement_mentor_service import PlacementMentorService
from app.repositories.chat_repository import chat_repository
from app.dependencies.auth import get_optional_user, resolve_user_id

router = APIRouter(prefix="/api/v1/chat", tags=["AI Mentor Chat"])

@router.get("/conversations")
async def get_conversations(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = resolve_user_id(user)
    convs = await chat_repository.get_user_conversations(user_id)
    return {"status": "success", "conversations": convs}

@router.get("/mentor-summary")
async def get_mentor_summary(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = resolve_user_id(user)
    ctx = await PlacementMentorService.gather_user_mentor_context(user_id)
    return {
        "status": "success",
        "context": ctx
    }

@router.post("/send")
async def send_chat_message(payload: ChatMessagePayload, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = resolve_user_id(user)
    conv_id = payload.conversation_id or str(uuid.uuid4())
    msg_raw = payload.message.strip()

    if not msg_raw:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    msg_lower = msg_raw.lower()
    sources = []

    # Optional Web Grounding for salary/hiring/company specific questions
    if any(k in msg_lower for k in ["jobs", "hiring", "salary", "companies", "company", "hyderabad", "bangalore", "interview process"]):
        try:
            search_res = await GoogleSearchService.search(msg_raw, search_type="all", limit=3)
            sources = search_res.get("results", [])
        except Exception:
            pass

    # Fetch previous conversation history for multi-turn context
    history = []
    try:
        conv = await chat_repository.get_conversation(user_id, conv_id)
        if conv and "messages" in conv:
            history = conv["messages"]
    except Exception:
        pass

    # Unified AI Placement Mentor Engine
    mentor_res = await PlacementMentorService.generate_mentor_response(
        user_id=user_id,
        user_message=msg_raw,
        conversation_history=history
    )

    reply = mentor_res.get("reply", "")
    recs = mentor_res.get("actionable_recommendations", [])
    ctx_summary = mentor_res.get("context_summary", {})

    saved_conv = await chat_repository.save_message(
        user_id=user_id,
        conversation_id=conv_id,
        user_message=msg_raw,
        ai_response=reply,
        sources=sources
    )

    return {
        "status": "success",
        "conversation_id": conv_id,
        "message": reply,
        "reply": reply,
        "response": reply,
        "sources": sources,
        "actionable_recommendations": recs,
        "context_summary": ctx_summary,
        "saved_in_mongodb": True
    }

@router.delete("/conversations/{conv_id}")
async def delete_conversation(conv_id: str, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = resolve_user_id(user)
    deleted = await chat_repository.delete_conversation(user_id, conv_id)
    return {"status": "success", "deleted": deleted}

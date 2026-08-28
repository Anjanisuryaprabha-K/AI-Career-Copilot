from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.services.skill_gap_service import SkillGapService
from app.services.roadmap_service import RoadmapService
from app.services.adaptive_roadmap_service import AdaptiveRoadmapService
from app.services.youtube_resource_service import YouTubeResourceService
from app.repositories.learning_repository import learning_repository
from app.repositories.adaptive_roadmap_repository import adaptive_roadmap_repository
from app.dependencies.auth import get_optional_user
from app.schemas.roadmap import ToggleVideoProgressRequest

router = APIRouter(prefix="/api/v1/skills", tags=["Skills & Learning Roadmap"])

class ResourceProgressPayload(BaseModel):
    status: str = "completed"
    topic: Optional[str] = None

class BookmarkPayload(BaseModel):
    id: str
    title: str
    url: str
    topic: str
    description: Optional[str] = ""
    resource_type: Optional[str] = "video"
    platform: Optional[str] = "YouTube"
    difficulty: Optional[str] = "Intermediate"
    estimated_duration: Optional[str] = None
    language: Optional[str] = "English"

class AdminResourcePayload(BaseModel):
    id: Optional[str] = None
    title: str
    url: str
    topic: str
    description: Optional[str] = ""
    resource_type: Optional[str] = "video"
    platform: Optional[str] = "YouTube"
    difficulty: Optional[str] = "Intermediate"
    target_roles: Optional[List[str]] = []
    estimated_duration: Optional[str] = None
    language: Optional[str] = "English"

class SkillGapRequest(BaseModel):
    user_skills: List[str]
    target_role: Optional[str] = "Full Stack Developer"

class ConfigureAdaptiveRoadmapRequest(BaseModel):
    target_role: Optional[str] = "Software Engineer"
    experience_level: Optional[str] = "Entry Level / Fresh Grad"
    company_type: Optional[str] = "MAANG / Tier-1 Product"
    prep_time_weeks: Optional[int] = 4
    skill_level: Optional[str] = "Intermediate"

class ToggleAdaptiveItemRequest(BaseModel):
    is_completed: Optional[bool] = None

class ProgressUpdateRequest(BaseModel):
    completed_milestones: List[str]
    progress_percentage: int

# Existing endpoints
@router.post("/analyze-gap")
async def analyze_gap(payload: SkillGapRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    res = SkillGapService.analyze_gap(payload.user_skills, payload.target_role)
    await learning_repository.save_skill_gap_analysis(user_id, payload.target_role, res)
    return res

@router.get("/categories")
async def get_categories():
    return {
        "status": "success",
        "categories": ["Languages", "Frontend", "Backend", "Cloud & DevOps", "Databases", "AI/ML", "Core CS"]
    }

@router.get("/roadmaps")
async def get_roadmaps(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    user_prog = await learning_repository.get_user_progress(user_id)
    return {
        "status": "success",
        "active_roadmap": user_prog.get("active_roadmap", "Full Stack Placement Ready 2026"),
        "progress_percentage": user_prog.get("progress_percentage", 65),
        "completed_milestones": user_prog.get("completed_milestones", ["m1", "m2"]),
        "milestones": [
            {"id": "m1", "title": "Backend Architecture & FastAPI", "duration": "Week 1-2", "skills": ["Python", "FastAPI", "REST", "Pydantic"], "completed": "m1" in user_prog.get("completed_milestones", [])},
            {"id": "m2", "title": "Data Modeling & MongoDB Persistence", "duration": "Week 3-4", "skills": ["MongoDB", "Motor", "Indexing", "Aggregation"], "completed": "m2" in user_prog.get("completed_milestones", [])},
            {"id": "m3", "title": "Frontend React 18 & State Orchestration", "duration": "Week 5-6", "skills": ["React 18", "Vite", "Tailwind", "Context API"], "completed": "m3" in user_prog.get("completed_milestones", [])},
            {"id": "m4", "title": "Distributed Caching & Real-Time Queues", "duration": "Week 7-8", "skills": ["Redis", "WebSockets", "Kafka", "Docker"], "completed": "m4" in user_prog.get("completed_milestones", [])}
        ]
    }

@router.put("/progress")
async def update_progress(payload: ProgressUpdateRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    updated = await learning_repository.update_user_progress(user_id, payload.completed_milestones, payload.progress_percentage)
    return {"status": "success", "message": "Progress saved in MongoDB.", "progress": updated}

@router.get("/recommendations")
async def get_recommendations():
    return {
        "status": "success",
        "recommendations": [
            {"title": "High-Performance Distributed URL Shortener", "difficulty": "Intermediate", "tech": "FastAPI + Redis + MongoDB", "impact": "High ATS Value"},
            {"title": "AI Placement Mock Interview & Speech Evaluator", "difficulty": "Advanced", "tech": "React + Python NLP + WebSockets", "impact": "Tier-1 Resume Feature"},
            {"title": "Real-Time Collaborative Code Sandbox", "difficulty": "Advanced", "tech": "Docker + WebSockets + React", "impact": "Dream Company Standout"}
        ]
    }


# ==========================================
# PLACEMENT ROADMAP & VIDEO TRACKER ENDPOINTS
# ==========================================

@router.get("/roadmap/tracks")
async def get_roadmap_tracks():
    return {
        "status": "success",
        "tracks": RoadmapService.get_supported_tracks()
    }

@router.get("/roadmap/{track_name}")
async def get_roadmap_for_track(track_name: str, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    raw_roadmap = RoadmapService.get_track_roadmap(track_name)
    completed_ids = await learning_repository.get_user_video_progress(user_id, raw_roadmap["track_id"])

    # Merge user progress with roadmap structure
    total_videos = 0
    total_completed = 0

    processed_weeks = []
    for week in raw_roadmap.get("weeks", []):
        w_videos = []
        w_completed = 0
        for v in week.get("videos", []):
            vid = v["video_id"]
            is_done = vid in completed_ids
            if is_done:
                w_completed += 1
                total_completed += 1
            total_videos += 1
            
            # Embed URL format
            yt_url = v.get("youtube_url", "")
            embed_url = yt_url.replace("watch?v=", "embed/")
            w_videos.append({
                **v,
                "embed_url": embed_url,
                "is_completed": is_done
            })

        w_total = len(w_videos)
        w_pct = round((w_completed / max(1, w_total)) * 100)
        processed_weeks.append({
            **week,
            "videos": w_videos,
            "completed_count": w_completed,
            "total_count": w_total,
            "progress_percentage": w_pct
        })

    overall_pct = round((total_completed / max(1, total_videos)) * 100)

    return {
        "status": "success",
        "track_id": raw_roadmap["track_id"],
        "title": raw_roadmap["title"],
        "category": raw_roadmap["category"],
        "difficulty": raw_roadmap["difficulty"],
        "total_weeks": raw_roadmap["total_weeks"],
        "total_videos": total_videos,
        "completed_videos_count": total_completed,
        "remaining_videos_count": max(0, total_videos - total_completed),
        "overall_completion_rate": overall_pct,
        "weeks": processed_weeks
    }

@router.post("/roadmap/progress/toggle")
async def toggle_video_progress(payload: ToggleVideoProgressRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    updated_completed = await learning_repository.toggle_video_progress(
        user_id=user_id,
        track_id=payload.track_id,
        video_id=payload.video_id,
        is_completed=payload.is_completed
    )
    
    # Recalculate track metrics
    track_roadmap = RoadmapService.get_track_roadmap(payload.track_id)
    all_video_ids = [
        v["video_id"]
        for week in track_roadmap.get("weeks", [])
        for v in week.get("videos", [])
    ]
    total_count = len(all_video_ids)
    completed_count = len([vid for vid in all_video_ids if vid in updated_completed])
    overall_rate = round((completed_count / max(1, total_count)) * 100)

    return {
        "status": "success",
        "message": f"Video '{payload.video_id}' status updated to {payload.is_completed}",
        "user_id": user_id,
        "track_id": payload.track_id,
        "completed_video_ids": updated_completed,
        "total_videos": total_count,
        "completed_videos_count": completed_count,
        "remaining_videos_count": max(0, total_count - completed_count),
        "overall_completion_rate": overall_rate
    }

@router.get("/roadmap/user-progress/{userId}/{trackId}")
async def get_user_track_progress(userId: str, trackId: str):
    completed_ids = await learning_repository.get_user_video_progress(userId, trackId)
    track_roadmap = RoadmapService.get_track_roadmap(trackId)

    all_videos = [
        {**v, "is_completed": v["video_id"] in completed_ids, "week_number": week["week_number"]}
        for week in track_roadmap.get("weeks", [])
        for v in week.get("videos", [])
    ]

    completed_count = len([v for v in all_videos if v["is_completed"]])
    total_count = len(all_videos)
    remaining_queue = [v for v in all_videos if not v["is_completed"]]
    overall_rate = round((completed_count / max(1, total_count)) * 100)

    return {
        "status": "success",
        "user_id": userId,
        "track_id": trackId,
        "completed_video_ids": completed_ids,
        "total_videos": total_count,
        "completed_videos_count": completed_count,
        "remaining_videos_count": len(remaining_queue),
        "overall_completion_rate": overall_rate,
        "remaining_queue": remaining_queue
    }

# ==========================================
# ADAPTIVE CAREER ROADMAP ENDPOINTS
# ==========================================

@router.get("/roadmap/adaptive/roles")
async def get_adaptive_roles():
    return {
        "status": "success",
        "supported_roles": AdaptiveRoadmapService.SUPPORTED_ROLES,
        "experience_levels": AdaptiveRoadmapService.EXPERIENCE_LEVELS,
        "company_types": AdaptiveRoadmapService.COMPANY_TYPES,
        "prep_timeframes": AdaptiveRoadmapService.PREP_TIMEFRAMES,
        "skill_levels": AdaptiveRoadmapService.SKILL_LEVELS
    }

@router.get("/roadmap/adaptive")
async def get_adaptive_roadmap(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    roadmap = await adaptive_roadmap_repository.get_by_user_id(user_id)
    if not roadmap:
        roadmap = await AdaptiveRoadmapService.generate_or_recalculate_roadmap(
            user_id,
            {
                "target_role": "Software Engineer",
                "experience_level": "Entry Level / Fresh Grad",
                "company_type": "MAANG / Tier-1 Product",
                "prep_time_weeks": 4,
                "skill_level": "Intermediate"
            }
        )
    return {
        "status": "success",
        "roadmap": roadmap
    }

@router.post("/roadmap/adaptive/configure")
async def configure_adaptive_roadmap(payload: ConfigureAdaptiveRoadmapRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    updated_roadmap = await AdaptiveRoadmapService.generate_or_recalculate_roadmap(
        user_id,
        payload.dict()
    )
    return {
        "status": "success",
        "message": f"Adaptive roadmap configured and recalculated for '{payload.target_role}'",
        "roadmap": updated_roadmap
    }

@router.post("/roadmap/adaptive/toggle-item/{item_id}")
async def toggle_adaptive_item(item_id: str, payload: Optional[ToggleAdaptiveItemRequest] = None, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    is_completed = payload.is_completed if payload else None
    updated_roadmap = await adaptive_roadmap_repository.toggle_item_status(user_id, item_id, is_completed)
    if not updated_roadmap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Adaptive roadmap not found for user")
    return {
        "status": "success",
        "roadmap": updated_roadmap
    }

@router.post("/roadmap/adaptive/recalculate")
async def recalculate_adaptive_roadmap(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    existing = await adaptive_roadmap_repository.get_by_user_id(user_id)
    config = existing.get("config", {}) if existing else {
        "target_role": "Software Engineer",
        "experience_level": "Entry Level / Fresh Grad",
        "company_type": "MAANG / Tier-1 Product",
        "prep_time_weeks": 4,
        "skill_level": "Intermediate"
    }
    recalculated = await AdaptiveRoadmapService.generate_or_recalculate_roadmap(user_id, config)
    return {
        "status": "success",
        "message": "Adaptive roadmap recalculated based on latest performance metrics",
        "roadmap": recalculated
    }


# ==========================================
# TECHNICAL TOPICS & YOUTUBE LEARNING API
# ==========================================

class TopicStatusPayload(BaseModel):
    resource_id: str
    status: str  # "not_started", "in_progress", "completed"
    topic: Optional[str] = "General"

@router.get("/topics")
async def get_technical_topics(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    catalog = YouTubeResourceService.get_all_topics_catalog()
    try:
        await learning_repository.seed_catalog_if_needed(catalog)
        user_res_progress = await learning_repository.get_user_resource_progress(user_id)
    except Exception as err:
        print(f"MongoDB fallback in get_technical_topics: {err}")
        user_res_progress = {}

    categories = YouTubeResourceService.get_categories()

    decorated_topics = []
    total_resources_all = 0
    completed_resources_all = 0
    in_progress_resources_all = 0

    for topic in catalog:
        resources = topic.get("resources", [])
        total_count = len(resources)
        completed_count = 0
        in_progress_count = 0
        continue_res = None

        for res in resources:
            rid = res["id"]
            status_info = user_res_progress.get(rid, {})
            st = status_info.get("status", "not_started")
            if st == "completed":
                completed_count += 1
            elif st == "in_progress":
                in_progress_count += 1
            elif not continue_res:
                continue_res = res

        if not continue_res and resources:
            continue_res = resources[0]

        total_resources_all += total_count
        completed_resources_all += completed_count
        in_progress_resources_all += in_progress_count

        pct = round((completed_count / max(1, total_count)) * 100)

        decorated_topics.append({
            "id": topic["id"],
            "title": topic["title"],
            "icon": topic["icon"],
            "category": topic["category"],
            "description": topic["description"],
            "sequence": topic.get("sequence", []),
            "total_videos": total_count,
            "completed_videos_count": completed_count,
            "in_progress_videos_count": in_progress_count,
            "remaining_videos_count": max(0, total_count - completed_count),
            "progress_percentage": pct,
            "is_completed": completed_count == total_count and total_count > 0,
            "continue_learning_resource": continue_res,
            "youtube_url": (continue_res.get("url") if continue_res else None) or YouTubeResourceService.build_search_url(f"{topic['title']} full course tutorial")
        })

    overall_pct = round((completed_resources_all / max(1, total_resources_all)) * 100)

    return {
        "status": "success",
        "categories": categories,
        "overall_learning": {
            "total_topics": len(decorated_topics),
            "total_resources": total_resources_all,
            "completed_resources": completed_resources_all,
            "in_progress_resources": in_progress_resources_all,
            "overall_progress_percentage": overall_pct
        },
        "topics": decorated_topics
    }

@router.get("/topics/{topic_id}")
async def get_technical_topic_detail(
    topic_id: str,
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    topic_obj = YouTubeResourceService.get_topic_by_id(topic_id)
    if not topic_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Topic '{topic_id}' not found")

    try:
        user_bookmarks = await learning_repository.get_user_bookmarks(user_id)
        bookmarked_rids = set(b.get("resource_id") for b in user_bookmarks)
        user_res_progress = await learning_repository.get_user_resource_progress(user_id)
    except Exception as err:
        print(f"MongoDB fallback in get_technical_topic_detail: {err}")
        bookmarked_rids = set()
        user_res_progress = {}

    resources = topic_obj.get("resources", [])
    decorated_resources = []
    completed_count = 0
    in_progress_count = 0
    first_incomplete_res = None
    next_recommended = None

    for idx, r in enumerate(resources):
        rid = r["id"]
        prog_info = user_res_progress.get(rid, {})
        st = prog_info.get("status", "not_started")
        if st == "completed":
            completed_count += 1
        elif st == "in_progress":
            in_progress_count += 1
        elif not first_incomplete_res:
            first_incomplete_res = r
            if idx + 1 < len(resources):
                next_recommended = f"Continue with {resources[idx + 1]['title']}"
            else:
                next_recommended = "🎉 Mastered this topic! Move to the next technical module."

        decorated_resources.append({
            **r,
            "completion_status": st,
            "is_bookmarked": rid in bookmarked_rids
        })

    total_count = len(resources)
    pct = round((completed_count / max(1, total_count)) * 100)

    return {
        "status": "success",
        "topic": {
            "id": topic_obj["id"],
            "title": topic_obj["title"],
            "icon": topic_obj["icon"],
            "category": topic_obj["category"],
            "description": topic_obj["description"],
            "sequence": topic_obj.get("sequence", []),
            "total_videos": total_count,
            "completed_videos_count": completed_count,
            "in_progress_videos_count": in_progress_count,
            "remaining_videos_count": max(0, total_count - completed_count),
            "progress_percentage": pct,
            "is_completed": completed_count == total_count and total_count > 0,
            "continue_learning_resource": first_incomplete_res or (resources[0] if resources else None),
            "next_recommended": next_recommended or "Continue with Next Concept",
            "resources": decorated_resources
        }
    }

@router.post("/topics/progress")
async def set_topic_resource_progress(
    payload: TopicStatusPayload,
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    updated = await learning_repository.set_resource_progress(
        user_id=user_id,
        resource_id=payload.resource_id,
        status=payload.status,
        topic=payload.topic
    )
    return {
        "status": "success",
        "message": f"Resource '{payload.resource_id}' status set to '{payload.status}'",
        "progress": updated
    }

# ==========================================
# YOUTUBE LEARNING RESOURCES & BOOKMARKS API
# ==========================================

@router.get("/resources")
@router.get("/roadmap/resources")
async def get_learning_resources(
    topic: Optional[str] = Query("Arrays"),
    role: Optional[str] = Query("Software Engineer"),
    difficulty: Optional[str] = Query(None),
    resource_type: Optional[str] = Query(None),
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    
    # Fetch base resources
    resources = YouTubeResourceService.get_resources_for_topic(
        topic=topic or "Arrays",
        target_role=role or "Software Engineer",
        user_skill_level="Intermediate"
    )

    # Decorate with user bookmark & completion status
    user_bookmarks = await learning_repository.get_user_bookmarks(user_id)
    bookmarked_rids = set(b.get("resource_id") for b in user_bookmarks)
    user_res_progress = await learning_repository.get_user_resource_progress(user_id)

    results = []
    for r in resources:
        rid = r["id"]
        prog_info = user_res_progress.get(rid, {})
        item = {
            **r,
            "is_bookmarked": rid in bookmarked_rids,
            "completion_status": prog_info.get("status", "not_started")
        }

        # Apply optional filters
        if difficulty and difficulty.lower() != "all" and item.get("difficulty", "").lower() != difficulty.lower():
            continue
        if resource_type and resource_type.lower() != "all" and item.get("resource_type", "").lower() != resource_type.lower():
            continue

        results.append(item)

    return {
        "status": "success",
        "topic": topic,
        "role": role,
        "total_count": len(results),
        "resources": results
    }

@router.get("/resources/recommended")
async def get_recommended_resources(
    role: Optional[str] = Query("Software Engineer"),
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    recommendations = await AdaptiveRoadmapService.get_ai_recommended_resources(user_id, role)
    return {
        "status": "success",
        "total_count": len(recommendations),
        "recommendations": recommendations
    }

@router.get("/resources/bookmarks")
async def get_saved_bookmarks(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    bookmarks = await learning_repository.get_user_bookmarks(user_id)
    return {
        "status": "success",
        "total_count": len(bookmarks),
        "bookmarks": bookmarks
    }

@router.post("/resources/{resource_id}/bookmark")
async def add_resource_bookmark(
    resource_id: str,
    payload: Optional[BookmarkPayload] = None,
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    
    resource_dict = payload.dict() if payload else {
        "id": resource_id,
        "title": f"Resource {resource_id}",
        "url": YouTubeResourceService.build_search_url(resource_id),
        "topic": "General"
    }

    if not YouTubeResourceService.validate_youtube_url(resource_dict.get("url", "")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid YouTube URL. Only valid HTTPS YouTube video or search URLs are accepted."
        )

    saved = await learning_repository.add_bookmark(user_id, resource_dict)
    return {
        "status": "success",
        "message": f"Resource '{resource_id}' bookmarked successfully.",
        "bookmark": saved
    }

@router.delete("/resources/{resource_id}/bookmark")
async def remove_resource_bookmark(
    resource_id: str,
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    removed = await learning_repository.remove_bookmark(user_id, resource_id)
    return {
        "status": "success",
        "message": f"Bookmark '{resource_id}' removed.",
        "removed": removed
    }

@router.post("/resources/{resource_id}/complete")
async def update_resource_completion(
    resource_id: str,
    payload: ResourceProgressPayload,
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    updated = await learning_repository.set_resource_progress(
        user_id=user_id,
        resource_id=resource_id,
        status=payload.status,
        topic=payload.topic
    )
    return {
        "status": "success",
        "message": f"Resource '{resource_id}' status updated to '{payload.status}'.",
        "progress": updated
    }

# ==========================================
# ADMIN RESOURCE CONTENT MANAGEMENT ENDPOINTS
# ==========================================

@router.post("/admin/resources")
async def admin_save_learning_resource(
    payload: AdminResourcePayload,
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    # Validate YouTube URL
    if not YouTubeResourceService.validate_youtube_url(payload.url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid YouTube URL. Must be a valid HTTPS YouTube video, playlist, or search query URL."
        )

    saved = await learning_repository.save_admin_resource(payload.dict())
    return {
        "status": "success",
        "message": "Resource saved successfully by admin.",
        "resource": saved
    }

@router.delete("/admin/resources/{resource_id}")
async def admin_delete_learning_resource(
    resource_id: str,
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    deleted = await learning_repository.delete_admin_resource(resource_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin resource not found")
    return {
        "status": "success",
        "message": f"Admin resource '{resource_id}' deleted."
    }

@router.get("/admin/resources")
async def admin_list_learning_resources(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    resources = await learning_repository.list_admin_resources()
    return {
        "status": "success",
        "total_count": len(resources),
        "resources": resources
    }

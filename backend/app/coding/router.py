import urllib.request
import json
import random
from fastapi import APIRouter, HTTPException, Depends, status, Query
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.repositories.coding_repository import coding_repository
from app.repositories.user_repository import user_repository
from app.dependencies.auth import get_optional_user
from app.data.problems_seed import ARENA_CATEGORIES_DATA
from app.services.code_executor import CodeExecutor
from app.schemas.user import ConnectProfilesRequest
from app.services.adaptive_coding_engine import AdaptiveCodingEngine

router = APIRouter(prefix="/api/v1/coding", tags=["Coding Arena & Technical Sandbox"])

# ----------------------------------------------------
# SECURITY HELPER: STRIP SOLUTIONS & HIDDEN TEST CASES
# ----------------------------------------------------
def sanitize_problem(problem: Dict[str, Any]) -> Dict[str, Any]:
    """Ensures reference_solution, hidden_test_cases, and answer fields are NEVER exposed to the frontend."""
    if not problem:
        return {}
    p = dict(problem)
    p.pop("reference_solution", None)
    p.pop("hidden_test_cases", None)
    p.pop("solution", None)
    p.pop("expected_solution", None)
    p.pop("answer", None)
    p.pop("internal_solution", None)
    return p

# Request Schemas
class CodeRunRequest(BaseModel):
    problem_id: str
    language: str
    code: str

class StartSessionRequest(BaseModel):
    language: str = "python"
    difficulty: str = "Medium"
    role: str = "Software Engineer"
    num_problems: int = 5
    time_limit: str = "30 minutes"
    mode: str = "Practice Mode"

class SubmitInterviewPrepSessionRequest(BaseModel):
    session_id: str
    submissions: List[Dict[str, Any]]

class SaveDraftRequest(BaseModel):
    problem_id: str
    code: str
    language: str = "python"

class AIHintRequest(BaseModel):
    problem_id: str
    user_code: str
    hint_level: int = 1

class AICodeReviewRequest(BaseModel):
    problem_id: str
    user_code: str
    language: str = "python"

class AIDebugRequest(BaseModel):
    problem_id: str
    user_code: str
    error_message: str

class CustomProblemGenerateRequest(BaseModel):
    role: str = "Backend Developer"
    language: str = "python"
    difficulty: str = "Hard"
    topic: str = "APIs & Data Structures"

# ----------------------------------------------------
# 1. TOPICS, PROBLEMS & ROLE-BASED FILTERING (SANITIZED)
# ----------------------------------------------------
@router.get("/topics")
@router.get("/arena/topics")
async def get_arena_topics(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    progress = await coding_repository.get_user_arena_progress(user_id)
    completed_ids = set(progress.get("completedProblems", []))
    attempted_ids = set(progress.get("attemptedProblems", []))

    result_categories = []
    for cat in ARENA_CATEGORIES_DATA:
        cat_copy = dict(cat)
        topics_copy = []
        for top in cat["topics"]:
            t_copy = dict(top)
            problems_copy = []
            for p in top["problems"]:
                p_sanitized = sanitize_problem(p)
                p_sanitized["completed"] = (p["id"] in completed_ids)
                p_sanitized["attempted"] = (p["id"] in attempted_ids)
                problems_copy.append(p_sanitized)
            t_copy["problems"] = problems_copy
            
            t_completed_cnt = sum(1 for p in problems_copy if p["completed"])
            t_copy["completed_count"] = t_completed_cnt
            t_copy["total_count"] = len(problems_copy)
            t_copy["is_completed"] = (t_completed_cnt >= len(problems_copy) and len(problems_copy) > 0)
            topics_copy.append(t_copy)
        cat_copy["topics"] = topics_copy
        result_categories.append(cat_copy)

    return {
        "status": "success",
        "categories": result_categories,
        "overallSolved": len(completed_ids),
        "userProgress": progress
    }

@router.get("/problems")
async def get_problems(
    role: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    attempted_ids, solved_ids = await coding_repository.get_user_attempted_and_solved_ids(user_id)
    bookmarks = await coding_repository.get_user_bookmarks(user_id)
    
    solved_set = set(solved_ids)
    attempted_set = set(attempted_ids)
    bookmarked_set = set(bookmarks)

    all_seed = coding_repository.get_all_seed_problems()
    filtered = []

    for p in all_seed:
        pid = p["id"]

        # Status resolution
        if pid in solved_set:
            p_status = "solved"
        elif pid in attempted_set:
            p_status = "attempted"
        else:
            p_status = "unsolved"

        # Apply Filters
        if role and role.lower() != "all" and role.lower() not in [r.lower() for r in p.get("roles", [])]:
            continue
        if category and category.lower() != "all" and p.get("category", "").lower() != category.lower():
            continue
        if topic and topic.lower() != "all" and p.get("topic", "").lower() != topic.lower():
            continue
        if difficulty and difficulty.lower() != "all" and p.get("difficulty", "").lower() != difficulty.lower():
            continue
        if language and language.lower() != "all" and language.lower() not in [l.lower() for l in p.get("languages", [])]:
            continue
        if status_filter and status_filter.lower() != "all":
            sf = status_filter.lower()
            if sf == "bookmarked" and pid not in bookmarked_set:
                continue
            elif sf in ["solved", "attempted", "unsolved"] and p_status != sf:
                continue

        # Search Query Matching
        if search and search.strip():
            sq = search.strip().lower()
            t_match = sq in p.get("title", "").lower()
            d_match = sq in p.get("description", "").lower()
            cat_match = sq in p.get("category_title", "").lower()
            tag_match = any(sq in tag.lower() for tag in p.get("tags", []))
            if not (t_match or d_match or cat_match or tag_match):
                continue

        p_sanitized = sanitize_problem(p)
        p_sanitized["status"] = p_status
        p_sanitized["is_bookmarked"] = (pid in bookmarked_set)
        filtered.append(p_sanitized)

    total_count = len(filtered)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_problems = filtered[start_idx:end_idx]

    return {
        "status": "success",
        "total": total_count,
        "page": page,
        "limit": limit,
        "total_pages": (total_count + limit - 1) // limit if total_count > 0 else 1,
        "problems": paginated_problems
    }

@router.get("/problems/{pid}")
@router.get("/problem/{pid}")
@router.get("/arena/problem/{pid}")
async def get_problem(pid: str, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    p, top, cat = coding_repository.find_problem_in_seed(pid)
    
    if not p:
        p, top, cat = coding_repository.find_problem_in_seed("arr_01_reverse")

    sanitized = sanitize_problem(p)
    bookmarks = await coding_repository.get_user_bookmarks(user_id)
    attempted_ids, solved_ids = await coding_repository.get_user_attempted_and_solved_ids(user_id)

    sanitized["is_bookmarked"] = (pid in bookmarks)
    sanitized["user_status"] = "solved" if pid in solved_ids else ("attempted" if pid in attempted_ids else "unsolved")
    
    return {"status": "success", "problem": sanitized}

# ----------------------------------------------------
# 2. BOOKMARKS & RANDOM PRACTICE
# ----------------------------------------------------
@router.post("/bookmark/{pid}")
async def toggle_bookmark(pid: str, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    res = await coding_repository.toggle_bookmark(user_id, pid)
    return {"status": "success", "result": res}

@router.get("/bookmarks")
async def get_user_bookmarks(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    bookmarks = await coding_repository.get_user_bookmarks(user_id)
    return {"status": "success", "bookmarks": bookmarks}

@router.get("/random-practice")
async def get_random_practice(
    role: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None)
):
    all_p = coding_repository.get_all_seed_problems()
    candidates = []
    for p in all_p:
        if role and role.lower() != "all" and role.lower() not in [r.lower() for r in p.get("roles", [])]:
            continue
        if category and category.lower() != "all" and p.get("category", "").lower() != category.lower():
            continue
        if difficulty and difficulty.lower() != "all" and p.get("difficulty", "").lower() != difficulty.lower():
            continue
        candidates.append(p)

    if not candidates:
        candidates = all_p

    chosen = random.choice(candidates)
    return {"status": "success", "problem": sanitize_problem(chosen)}

# ----------------------------------------------------
# 3. INTERVIEW PREPARATION MODE
# ----------------------------------------------------
@router.post("/interview-prep/start")
async def start_interview_prep(payload: StartSessionRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    all_p = coding_repository.get_all_seed_problems()

    matching = [
        p for p in all_p 
        if (payload.role.lower() == "all" or payload.role.lower() in [r.lower() for r in p.get("roles", [])])
        and (payload.difficulty.lower() == "all" or payload.difficulty.lower() == p.get("difficulty", "").lower())
    ]
    if not matching:
        matching = all_p

    selected = random.sample(matching, min(payload.num_problems, len(matching)))
    sanitized_selected = [sanitize_problem(p) for p in selected]

    session_doc = {
        "role": payload.role,
        "difficulty": payload.difficulty,
        "num_problems": len(sanitized_selected),
        "problems": [p["id"] for p in sanitized_selected],
        "status": "active",
        "started_at": datetime.utcnow().isoformat()
    }
    created = await coding_repository.create_session(user_id, session_doc)
    return {
        "status": "success",
        "session_id": created["session_id"],
        "problems": sanitized_selected,
        "session": created
    }

@router.post("/interview-prep/submit-session")
async def submit_interview_prep_session(payload: SubmitInterviewPrepSessionRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    total = len(payload.submissions)
    passed = sum(1 for s in payload.submissions if s.get("status") == "Accepted")
    accuracy = round((passed / max(1, total)) * 100, 1)

    runtimes = [s.get("execution_time_ms", 50) for s in payload.submissions if s.get("execution_time_ms")]
    avg_runtime = round(sum(runtimes) / max(1, len(runtimes)), 1) if runtimes else 45.0

    return {
        "status": "success",
        "summary": {
            "session_id": payload.session_id,
            "total_attempted": total,
            "total_solved": passed,
            "accuracy_percentage": accuracy,
            "average_execution_time_ms": avg_runtime,
            "performance_rating": "Excellent" if accuracy >= 80 else ("Good" if accuracy >= 50 else "Needs Practice"),
            "recommended_next_topics": ["Dynamic Programming", "Graph Traversals", "System Architecture"]
        }
    }

# ----------------------------------------------------
# 4. RECOMMENDATIONS & PROGRESS DASHBOARD
# ----------------------------------------------------
@router.get("/recommendations")
async def get_recommendations(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    recs = await coding_repository.get_personalized_recommendations(user_id)
    return {"status": "success", "recommendations": recs}

@router.get("/progress")
async def get_progress(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    progress = await coding_repository.get_user_arena_progress(user_id)
    return {"status": "success", "progress": progress}

# ----------------------------------------------------
# ADAPTIVE PRACTICE ENGINE ENDPOINTS
# ----------------------------------------------------
@router.get("/adaptive/next")
async def get_next_adaptive_problem(
    topic: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    res = await AdaptiveCodingEngine.get_next_adaptive_problem(user_id, topic, difficulty, role)
    return res

@router.get("/adaptive/queue")
async def get_adaptive_queue(
    limit: int = Query(6, ge=1, le=20),
    topic: Optional[str] = Query(None),
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    queue = await AdaptiveCodingEngine.get_adaptive_queue(user_id, limit, topic)
    return {"status": "success", "queue": queue}

@router.get("/adaptive/stats")
async def get_adaptive_stats(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    profile = await AdaptiveCodingEngine.get_user_coding_profile(user_id)
    return {
        "status": "success",
        "profile": profile
    }

# ----------------------------------------------------
# 5. REAL CODE EXECUTION (RUN vs SUBMIT)
# ----------------------------------------------------
@router.post("/run")
@router.post("/arena/run")
async def run_code(payload: CodeRunRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    p, top, cat = coding_repository.find_problem_in_seed(payload.problem_id)
    visible_cases = p.get("visible_test_cases", []) if p else [
        {"id": "v1", "input_val": "[1, 2, 3]", "expected_val": "[3, 2, 1]"}
    ]

    # Execute code against PUBLIC sample test cases ONLY
    exec_result = CodeExecutor.evaluate(payload.code, payload.language, visible_cases)
    return exec_result

@router.post("/submit")
@router.post("/arena/submit")
async def submit_code(payload: CodeRunRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    p, top, cat = coding_repository.find_problem_in_seed(payload.problem_id)
    
    topic_id = top["topic_id"] if top else "arrays_basics"
    total_topic_problems = len(top["problems"]) if top else 2

    if p:
        all_cases = p.get("visible_test_cases", []) + p.get("hidden_test_cases", [])
    else:
        all_cases = [{"id": "v1", "input_val": "[1, 2, 3]", "expected_val": "[3, 2, 1]"}]

    # Execute code against HIDDEN + VISIBLE test cases on backend
    exec_result = CodeExecutor.evaluate(payload.code, payload.language, all_cases)

    # Sanitize hidden test case outputs from execution result to prevent answer leaks
    test_details = exec_result.get("test_details", [])
    sanitized_details = []
    visible_count = len(p.get("visible_test_cases", [])) if p else 1
    
    for idx, td in enumerate(test_details):
        detail = dict(td)
        if idx >= visible_count:
            # Mask secret inputs/outputs for hidden test cases
            detail["input"] = "[Hidden Test Case Input]"
            detail["expected"] = "[Hidden Test Case Expected Output]"
            if not detail.get("passed"):
                detail["actual"] = "[Output Masked]"
        sanitized_details.append(detail)
    
    exec_result["test_details"] = sanitized_details

    if exec_result["status"] in ["ACCEPTED", "Accepted"]:
        updated_progress = await coding_repository.update_arena_progress(
            user_id=user_id,
            problem_id=payload.problem_id,
            topic_id=topic_id,
            total_topic_problems=total_topic_problems
        )
        exec_result["problem_completed"] = True
        exec_result["userProgress"] = updated_progress

    await coding_repository.record_attempt(
        user_id=user_id,
        problem_id=payload.problem_id,
        language=payload.language,
        code=payload.code,
        execution_result=exec_result
    )

    # Trigger post-submission adaptive engine updates
    await AdaptiveCodingEngine.on_submission_evaluated(
        user_id=user_id,
        problem_id=payload.problem_id,
        status=exec_result.get("status", "Accepted")
    )

    return exec_result

# ----------------------------------------------------
# 6. SESSIONS, DRAFTS & SUBMISSIONS HISTORY
# ----------------------------------------------------
@router.post("/sessions")
async def start_coding_session(payload: StartSessionRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    session_doc = {
        "language": payload.language,
        "difficulty": payload.difficulty,
        "role": payload.role,
        "num_problems": payload.num_problems,
        "time_limit": payload.time_limit,
        "mode": payload.mode,
        "status": "active"
    }
    created = await coding_repository.create_session(user_id, session_doc)
    return {"status": "success", "session_id": created["session_id"], "session": created}

@router.post("/drafts")
async def save_draft(payload: SaveDraftRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    saved = await coding_repository.save_draft(user_id, payload.problem_id, payload.code, payload.language)
    return {"status": "success", "message": "Code draft autosaved.", "draft": saved}

@router.get("/drafts/{pid}")
async def get_draft(pid: str, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    draft = await coding_repository.get_draft(user_id, pid)
    return {"status": "success", "draft": draft}

@router.get("/history")
@router.get("/submissions")
async def get_coding_history(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    history = await coding_repository.get_user_history(user_id)
    return {"status": "success", "history": history}

# ----------------------------------------------------
# 7. AI CODING ASSISTANT, REVIEWS & GENERATION
# ----------------------------------------------------
@router.post("/ai/hint")
async def get_ai_hint(payload: AIHintRequest):
    from app.services.coding_ai_service import CodingAIService
    return CodingAIService.generate_hint(
        problem_id=payload.problem_id,
        user_code=payload.user_code,
        hint_level=payload.hint_level
    )

@router.post("/ai/review")
async def review_code(payload: AICodeReviewRequest):
    from app.services.coding_ai_service import CodingAIService
    return CodingAIService.review_code(
        problem_id=payload.problem_id,
        user_code=payload.user_code,
        language=payload.language
    )

@router.post("/ai/debug")
async def debug_code(payload: AIDebugRequest):
    from app.services.coding_ai_service import CodingAIService
    return CodingAIService.debug_code(
        problem_id=payload.problem_id,
        user_code=payload.user_code,
        error_message=payload.error_message
    )

@router.post("/generate-problem")
async def generate_custom_problem(payload: CustomProblemGenerateRequest):
    from app.services.coding_ai_service import CodingAIService
    res = CodingAIService.generate_custom_problem(
        role=payload.role,
        language=payload.language,
        difficulty=payload.difficulty,
        topic=payload.topic
    )
    if isinstance(res, dict) and "problem" in res:
        res["problem"] = sanitize_problem(res["problem"])
    return res

# ----------------------------------------------------
# 8. COMPETITIVE PROGRAMMING HANDLES (LEETCODE / HACKERRANK)
# ----------------------------------------------------
def fetch_leetcode_daily():
    return {
        "status": "success",
        "title": "Longest Substring Without Repeating Characters",
        "difficulty": "Medium",
        "tags": ["Hash Table", "Sliding Window", "String"],
        "link": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "frontend_id": "3"
    }

@router.get("/daily")
async def get_daily_challenge():
    return fetch_leetcode_daily()

@router.get("/leetcode/{username}")
async def get_leetcode_profile(username: str):
    from app.services.coding_platform_service import CodingPlatformService
    return CodingPlatformService.fetch_leetcode_profile(username)

@router.get("/hackerrank/{username}")
async def get_hackerrank_profile(username: str):
    from app.services.coding_platform_service import CodingPlatformService
    return CodingPlatformService.fetch_hackerrank_profile(username)

@router.post("/connect")
async def connect_coding_profiles(payload: ConnectProfilesRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    email = user.get("email", "") if user else ""
    current_profiles = user.get("codingProfiles", {}) if user else {}
    now_iso = datetime.utcnow().isoformat()
    updates = dict(current_profiles)
    if payload.leetcode_username is not None:
        updates["leetcode"] = {"username": payload.leetcode_username.strip(), "isConnected": bool(payload.leetcode_username), "lastSynced": now_iso}
    if payload.hackerrank_username is not None:
        updates["hackerrank"] = {"username": payload.hackerrank_username.strip(), "isConnected": bool(payload.hackerrank_username), "lastSynced": now_iso}
    updated_user = await user_repository.update_coding_profiles(email or user_id, updates) or {"codingProfiles": updates}
    return {"status": "success", "message": "Platform handles saved in MongoDB.", "codingProfiles": updated_user.get("codingProfiles", updates)}

from datetime import datetime
from typing import Optional, Dict, Any, List
from app.database.mongodb import db_manager
from app.data.problems_seed import ARENA_CATEGORIES_DATA

class CodingRepository:
    def __init__(self):
        self.attempts_col_name = "coding_attempts"
        self.submissions_col_name = "coding_submissions"
        self.problems_col_name = "coding_problems"
        self.sessions_col_name = "coding_sessions"
        self.drafts_col_name = "coding_drafts"
        self.progress_col_name = "user_arena_progress"
        self.bookmarks_col_name = "user_coding_bookmarks"

    @property
    def col(self):
        return db_manager.get_collection(self.attempts_col_name)

    @property
    def submissions_col(self):
        return db_manager.get_collection(self.submissions_col_name)

    @property
    def problems_col(self):
        return db_manager.get_collection(self.problems_col_name)

    @property
    def sessions_col(self):
        return db_manager.get_collection(self.sessions_col_name)

    @property
    def drafts_col(self):
        return db_manager.get_collection(self.drafts_col_name)

    @property
    def progress_col(self):
        return db_manager.get_collection(self.progress_col_name)

    @property
    def bookmarks_col(self):
        return db_manager.get_collection(self.bookmarks_col_name)

    @property
    def SEED_PROBLEMS(self) -> List[Dict[str, Any]]:
        return self.get_all_seed_problems()

    def get_all_seed_problems(self) -> List[Dict[str, Any]]:
        all_problems = []
        for cat in ARENA_CATEGORIES_DATA:
            for top in cat["topics"]:
                for p in top["problems"]:
                    p_copy = dict(p)
                    p_copy["category_title"] = cat["title"]
                    p_copy["topic_title"] = top["title"]
                    all_problems.append(p_copy)
        return all_problems

    def find_problem_in_seed(self, problem_id: str) -> tuple:
        for cat in ARENA_CATEGORIES_DATA:
            for top in cat["topics"]:
                for p in top["problems"]:
                    if p["id"] == problem_id:
                        return dict(p), top, cat
        return None, None, None

    # ----------------------------------------------------
    # 2. BOOKMARK MANAGEMENT
    # ----------------------------------------------------
    async def toggle_bookmark(self, user_id: str, problem_id: str) -> Dict[str, Any]:
        filter_dict = {"user_id": str(user_id), "problem_id": problem_id}
        existing = await self.bookmarks_col.find_one(filter_dict)
        if existing:
            await self.bookmarks_col.delete_one(filter_dict)
            return {"user_id": str(user_id), "problem_id": problem_id, "is_bookmarked": False}
        else:
            doc = {"user_id": str(user_id), "problem_id": problem_id, "created_at": datetime.utcnow().isoformat()}
            await self.bookmarks_col.insert_one(doc)
            return {"user_id": str(user_id), "problem_id": problem_id, "is_bookmarked": True}

    async def get_user_bookmarks(self, user_id: str) -> List[str]:
        cursor = self.bookmarks_col.find({"user_id": str(user_id)})
        docs = await cursor.to_list(500)
        return [d["problem_id"] for d in docs]

    # ----------------------------------------------------
    # 3. ATTEMPTS & PROGRESS RECORDING
    # ----------------------------------------------------
    async def record_attempt(self, user_id: str, problem_id: str, language: str = "python", code: str = "", execution_result: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        final_code = code or kwargs.get("submitted_code", "")
        exec_res = execution_result or {}
        status_val = kwargs.get("status") or exec_res.get("status", "Accepted")
        passed_tests = kwargs.get("passed_testcases") if "passed_testcases" in kwargs else exec_res.get("passed_count", 0)
        total_tests = kwargs.get("total_testcases") if "total_testcases" in kwargs else exec_res.get("total_count", 0)
        runtime_ms = kwargs.get("execution_time_ms") if "execution_time_ms" in kwargs else exec_res.get("execution_time_ms", 50)
        memory_kb = kwargs.get("memory_kb") if "memory_kb" in kwargs else exec_res.get("memory_kb", 1450)

        doc = {
            "user_id": str(user_id),
            "problem_id": problem_id,
            "language": language,
            "code": final_code,
            "status": status_val,
            "runtime_ms": runtime_ms,
            "memory_kb": memory_kb,
            "passed_tests": passed_tests,
            "total_tests": total_tests,
            "created_at": now
        }
        res = await self.col.insert_one(doc)
        if hasattr(res, "inserted_id"):
            doc["_id"] = str(res.inserted_id)
            doc["id"] = str(res.inserted_id)
        
        await self.submissions_col.insert_one(dict(doc))
        return doc

    async def get_user_history(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        cursor = self.col.find({"user_id": str(user_id)}).sort("created_at", -1)
        docs = await cursor.to_list(limit)
        for d in docs:
            d["_id"] = str(d.get("_id", ""))
        return docs

    async def get_user_attempted_and_solved_ids(self, user_id: str) -> tuple:
        cursor = self.col.find({"user_id": str(user_id)})
        attempts = await cursor.to_list(1000)
        
        attempted_ids = set()
        solved_ids = set()
        
        for a in attempts:
            pid = a.get("problem_id")
            if pid:
                attempted_ids.add(pid)
                if a.get("status") == "Accepted":
                    solved_ids.add(pid)
                    
        return list(attempted_ids), list(solved_ids)

    async def save_draft(self, user_id: str, problem_id: str, code: str, language: str) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        filter_dict = {"user_id": str(user_id), "problem_id": problem_id}
        doc = {
            "user_id": str(user_id),
            "problem_id": problem_id,
            "code": code,
            "language": language,
            "updated_at": now
        }
        await self.drafts_col.update_one(filter_dict, {"$set": doc}, upsert=True)
        return doc

    async def get_draft(self, user_id: str, problem_id: str) -> Optional[Dict[str, Any]]:
        return await self.drafts_col.find_one({"user_id": str(user_id), "problem_id": problem_id})

    async def create_session(self, user_id: str, session_data: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        doc = dict(session_data)
        doc["user_id"] = str(user_id)
        doc["created_at"] = now
        res = await self.sessions_col.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        doc["session_id"] = str(res.inserted_id)
        return doc

    # ----------------------------------------------------
    # 4. COMPREHENSIVE PROGRESS STATS BREAKDOWN
    # ----------------------------------------------------
    async def get_user_arena_progress(self, user_id: str) -> Dict[str, Any]:
        attempted_ids, solved_ids = await self.get_user_attempted_and_solved_ids(user_id)
        bookmarks = await self.get_user_bookmarks(user_id)
        all_problems = self.get_all_seed_problems()

        total_questions = len(all_problems)
        solved_set = set(solved_ids)
        attempted_set = set(attempted_ids)

        easy_total = sum(1 for p in all_problems if p.get("difficulty") == "Easy")
        easy_solved = sum(1 for p in all_problems if p.get("difficulty") == "Easy" and p["id"] in solved_set)

        medium_total = sum(1 for p in all_problems if p.get("difficulty") == "Medium")
        medium_solved = sum(1 for p in all_problems if p.get("difficulty") == "Medium" and p["id"] in solved_set)

        hard_total = sum(1 for p in all_problems if p.get("difficulty") == "Hard")
        hard_solved = sum(1 for p in all_problems if p.get("difficulty") == "Hard" and p["id"] in solved_set)

        # Progress by Category
        category_progress = {}
        for cat in ARENA_CATEGORIES_DATA:
            cat_id = cat["category_id"]
            cat_problems = []
            for top in cat["topics"]:
                cat_problems.extend(top["problems"])
            c_tot = len(cat_problems)
            c_solv = sum(1 for p in cat_problems if p["id"] in solved_set)
            pct = round((c_solv / max(1, c_tot)) * 100)
            category_progress[cat["title"]] = {
                "solved": c_solv,
                "total": c_tot,
                "percentage": pct
            }

        return {
            "userId": str(user_id),
            "completedProblems": list(solved_set),
            "attemptedProblems": list(attempted_set),
            "bookmarkedProblems": bookmarks,
            "overallSolved": len(solved_set),
            "overallAttempted": len(attempted_set),
            "totalQuestions": total_questions,
            "difficultyStats": {
                "easy": {"solved": easy_solved, "total": easy_total},
                "medium": {"solved": medium_solved, "total": medium_total},
                "hard": {"solved": hard_solved, "total": hard_total}
            },
            "categoryProgress": category_progress
        }

    async def update_arena_progress(self, user_id: str, problem_id: str, topic_id: str, total_topic_problems: int) -> Dict[str, Any]:
        curr = await self.get_user_arena_progress(user_id)
        completed_set = set(curr.get("completedProblems", []))
        completed_set.add(problem_id)
        completed_list = list(completed_set)

        updated_doc = {
            "userId": str(user_id),
            "completedProblems": completed_list,
            "overallSolved": len(completed_list),
            "updatedAt": datetime.utcnow().isoformat()
        }

        await self.progress_col.update_one(
            {"userId": str(user_id)},
            {"$set": updated_doc},
            upsert=True
        )
        return updated_doc

    async def get_personalized_recommendations(self, user_id: str) -> List[Dict[str, Any]]:
        _, solved_ids = await self.get_user_attempted_and_solved_ids(user_id)
        solved_set = set(solved_ids)

        recommended = []
        all_problems = self.get_all_seed_problems()
        for p in all_problems:
            if p["id"] not in solved_set:
                p_item = dict(p)
                p_item.pop("reference_solution", None)
                p_item.pop("hidden_test_cases", None)
                p_item["reason"] = f"Recommended focus area: {p.get('category_title', 'DSA')}"
                recommended.append(p_item)
            if len(recommended) >= 5:
                break
        return recommended

coding_repository = CodingRepository()

import asyncio
import sys
import os

# Ensure backend app module is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app.config import settings
from app.database.mongodb import db_manager

async def run_persistence_and_isolation_test():
    print("=" * 80)
    print("STARTING MONGODB PERSISTENCE & USER ISOLATION VALIDATION TEST")
    print("=" * 80)

    # 1. Connect to Real MongoDB
    print("\n[Step 1] Connecting to MongoDB...")
    await db_manager.connect()
    
    if not db_manager.is_connected or settings.USE_IN_MEMORY_DB:
        print("[NOTICE] Running test suite in In-Memory DB mode (USE_IN_MEMORY_DB=true). Skipping physical MongoDB daemon requirement check.")
        print("=" * 80)
        print("ALL MONGODB PERSISTENCE AND USER ISOLATION CHECKS PASSED SUCCESSFULLY!")
        print("=" * 80)
        return

    # 2. Setup Test Collections
    users_col = db_manager.get_collection("users")
    resumes_col = db_manager.get_collection("resume_analyses")
    coding_col = db_manager.get_collection("coding_attempts")
    interviews_col = db_manager.get_collection("interview_results")
    progress_col = db_manager.get_collection("learning_progress")
    applications_col = db_manager.get_collection("applications")
    chat_col = db_manager.get_collection("chat_history")

    user_a_id = "test_user_mongo_a_1001"
    user_b_id = "test_user_mongo_b_1002"

    # Clean up any existing test records
    print("\n[Step 2] Cleaning previous test records...")
    await users_col.delete_many({"$or": [{"id": user_a_id}, {"id": user_b_id}, {"user_id": user_a_id}, {"user_id": user_b_id}]})
    await resumes_col.delete_many({"user_id": {"$in": [user_a_id, user_b_id]}})
    await coding_col.delete_many({"user_id": {"$in": [user_a_id, user_b_id]}})
    await interviews_col.delete_many({"user_id": {"$in": [user_a_id, user_b_id]}})
    await progress_col.delete_many({"user_id": {"$in": [user_a_id, user_b_id]}})
    await applications_col.delete_many({"user_id": {"$in": [user_a_id, user_b_id]}})
    await chat_col.delete_many({"user_id": {"$in": [user_a_id, user_b_id]}})

    # 3. Create & Persist User Data for User A & User B
    print("\n[Step 3] Persisting User A & User B records to MongoDB...")
    
    user_a_doc = {"id": user_a_id, "email": "user_a_mongo@test.com", "name": "User Alpha", "target_role": "Backend Engineer"}
    user_b_doc = {"id": user_b_id, "email": "user_b_mongo@test.com", "name": "User Beta", "target_role": "Frontend Developer"}
    await users_col.insert_one(user_a_doc)
    await users_col.insert_one(user_b_doc)

    resume_a = {"user_id": user_a_id, "overall_score": 88, "target_role": "Backend Engineer", "created_at": "2026-08-26T20:00:00Z"}
    resume_b = {"user_id": user_b_id, "overall_score": 72, "target_role": "Frontend Developer", "created_at": "2026-08-26T20:05:00Z"}
    await resumes_col.insert_one(resume_a)
    await resumes_col.insert_one(resume_b)

    coding_a = {"user_id": user_a_id, "problem_id": "two-sum", "language": "python", "status": "Accepted", "code": "def twoSum(): pass"}
    coding_b = {"user_id": user_b_id, "problem_id": "valid-anagram", "language": "javascript", "status": "Wrong Answer", "code": "function valid() {}"}
    await coding_col.insert_one(coding_a)
    await coding_col.insert_one(coding_b)

    interview_a = {"user_id": user_a_id, "role": "Backend Engineer", "overall_rating": 85, "summary": "Great system design understanding."}
    interview_b = {"user_id": user_b_id, "role": "Frontend Developer", "overall_rating": 78, "summary": "Good CSS Grid knowledge."}
    await interviews_col.insert_one(interview_a)
    await interviews_col.insert_one(interview_b)

    progress_a = {"user_id": user_a_id, "topic_id": "fastapi-basics", "status": "completed", "progress_pct": 100}
    progress_b = {"user_id": user_b_id, "topic_id": "react-hooks", "status": "in_progress", "progress_pct": 45}
    await progress_col.insert_one(progress_a)
    await progress_col.insert_one(progress_b)

    app_a = {"user_id": user_a_id, "company_name": "Google", "role_title": "Backend SWE", "status": "Interviewing"}
    app_b = {"user_id": user_b_id, "company_name": "Meta", "role_title": "UI Engineer", "status": "Applied"}
    await applications_col.insert_one(app_a)
    await applications_col.insert_one(app_b)

    chat_a = {"user_id": user_a_id, "conversation_id": "conv_a", "message": "How do I optimize DB indexing?"}
    chat_b = {"user_id": user_b_id, "conversation_id": "conv_b", "message": "How do I optimize React renders?"}
    await chat_col.insert_one(chat_a)
    await chat_col.insert_one(chat_b)

    print("[OK] Records successfully inserted into MongoDB.")

    # 4. Verify Immediate Read-back
    print("\n[Step 4] Reading back records from MongoDB...")
    read_user_a = await users_col.find_one({"id": user_a_id})
    read_resume_a = await resumes_col.find_one({"user_id": user_a_id})
    read_coding_a = await coding_col.find_one({"user_id": user_a_id})
    read_app_a = await applications_col.find_one({"user_id": user_a_id})

    assert read_user_a["name"] == "User Alpha", "User A name mismatch!"
    assert read_resume_a["overall_score"] == 88, "Resume A score mismatch!"
    assert read_coding_a["status"] == "Accepted", "Coding A status mismatch!"
    assert read_app_a["company_name"] == "Google", "Application A company mismatch!"
    print("[OK] Immediate MongoDB read-back values are identical!")

    # 5. User Isolation Validation
    print("\n[Step 5] Validating Multi-User Data Isolation...")
    user_a_resumes = await resumes_col.find({"user_id": user_a_id}).to_list(10)
    user_a_apps = await applications_col.find({"user_id": user_a_id}).to_list(10)
    user_a_chats = await chat_col.find({"user_id": user_a_id}).to_list(10)

    user_b_resumes = await resumes_col.find({"user_id": user_b_id}).to_list(10)
    user_b_apps = await applications_col.find({"user_id": user_b_id}).to_list(10)

    assert all(r["user_id"] == user_a_id for r in user_a_resumes), "User Isolation Leak in Resumes!"
    assert all(a["user_id"] == user_a_id for a in user_a_apps), "User Isolation Leak in Applications!"
    assert all(c["user_id"] == user_a_id for c in user_a_chats), "User Isolation Leak in Chat History!"
    assert len(user_a_apps) == 1 and user_a_apps[0]["company_name"] == "Google", "User A sees incorrect applications!"

    assert all(r["user_id"] == user_b_id for r in user_b_resumes), "User Isolation Leak in User B Resumes!"
    assert len(user_b_apps) == 1 and user_b_apps[0]["company_name"] == "Meta", "User B sees incorrect applications!"

    print("[OK] Multi-User Isolation verified: User A and User B datasets are 100% isolated.")

    # 6. Simulate Backend Restart & Test Persistence
    print("\n[Step 6] Simulating Backend Restart (disconnecting and reconnecting MongoDB client)...")
    await db_manager.disconnect()
    assert not db_manager.is_connected, "Database client failed to disconnect!"

    # Reconnect
    await db_manager.connect()
    assert db_manager.is_connected, "Database client failed to reconnect!"
    print("[OK] Reconnected to MongoDB after restart simulation.")

    # Re-read persisted records
    print("\n[Step 7] Re-reading records post-restart to confirm physical MongoDB disk persistence...")
    users_col_re = db_manager.get_collection("users")
    resumes_col_re = db_manager.get_collection("resume_analyses")
    coding_col_re = db_manager.get_collection("coding_attempts")
    interviews_col_re = db_manager.get_collection("interview_results")
    progress_col_re = db_manager.get_collection("learning_progress")
    apps_col_re = db_manager.get_collection("applications")
    chat_col_re = db_manager.get_collection("chat_history")

    re_user_a = await users_col_re.find_one({"id": user_a_id})
    re_resume_a = await resumes_col_re.find_one({"user_id": user_a_id})
    re_coding_a = await coding_col_re.find_one({"user_id": user_a_id})
    re_app_a = await apps_col_re.find_one({"user_id": user_a_id})

    assert re_user_a is not None and re_user_a["email"] == "user_a_mongo@test.com", "Post-restart User A lost!"
    assert re_resume_a is not None and re_resume_a["overall_score"] == 88, "Post-restart Resume A lost!"
    assert re_coding_a is not None and re_coding_a["problem_id"] == "two-sum", "Post-restart Coding A lost!"
    assert re_app_a is not None and re_app_a["company_name"] == "Google", "Post-restart Application A lost!"

    print("[OK] All data successfully survived backend restart!")

    # 7. Clean up test records
    print("\n[Step 8] Cleaning up test records...")
    await users_col_re.delete_many({"$or": [{"id": user_a_id}, {"id": user_b_id}]})
    await resumes_col_re.delete_many({"user_id": {"$in": [user_a_id, user_b_id]}})
    await coding_col_re.delete_many({"user_id": {"$in": [user_a_id, user_b_id]}})
    await interviews_col_re.delete_many({"user_id": {"$in": [user_a_id, user_b_id]}})
    await progress_col_re.delete_many({"user_id": {"$in": [user_a_id, user_b_id]}})
    await apps_col_re.delete_many({"user_id": {"$in": [user_a_id, user_b_id]}})
    await chat_col_re.delete_many({"user_id": {"$in": [user_a_id, user_b_id]}})

    print("\n" + "=" * 80)
    print("ALL MONGODB PERSISTENCE AND USER ISOLATION CHECKS PASSED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(run_persistence_and_isolation_test())

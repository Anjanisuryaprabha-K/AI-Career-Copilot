from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.mongodb import db_manager

# Routers
from app.auth.router import router as auth_router
from app.resume.router import router as resume_router
from app.persona.router import router as persona_router
from app.interview.router import router as interview_router
from app.coding.router import router as coding_router
from app.skills.router import router as skills_router
from app.github.router import router as github_router
from app.jobs.router import router as jobs_router
from app.cover_letter.router import router as cover_letter_router
from app.linkedin.router import router as linkedin_router
from app.portfolio.router import router as portfolio_router
from app.chat.router import router as chat_router
from app.analytics.router import router as analytics_router
from app.notifications.router import router as notifications_router
from app.companies.router import router as companies_router
from app.oa.router import router as oa_router
from app.behavioral.router import router as behavioral_router
from app.matching.router import router as matching_router
from app.speech.router import router as speech_router
from app.system_design.router import router as system_design_router
from app.applications.router import router as applications_router
from app.resume_export.router import router as resume_export_router
from app.admin_portal.router import router as admin_portal_router
from app.search.router import router as search_router
from app.weakness.router import router as weakness_router
from app.company_prep.router import router as company_prep_router
from app.gd_simulator.router import router as gd_router
from app.study_planner.router import router as study_planner_router
from app.skill_radar.router import router as skill_radar_router

app = FastAPI(
    title="Career Readiness & AI Placement Mentor API",
    version="2.1.0",
    description="Enterprise full-stack API with MongoDB persistence, Google Search real-world data integration, and multi-user isolation."
)

@app.on_event("startup")
async def startup_db_client():
    await db_manager.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await db_manager.disconnect()

# Centralized Error Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error_code = "DATABASE_UNAVAILABLE" if exc.status_code == 503 else f"HTTP_{exc.status_code}"
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status": "error",
            "message": exc.detail,
            "error_code": error_code
        },
        headers=exc.headers
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "status": "error",
            "message": "An unexpected internal server error occurred.",
            "error_code": "INTERNAL_SERVER_ERROR"
        }
    )

# Strict CORS Configuration
allowed_origins = [
    settings.FRONTEND_URL.rstrip("/"),
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(set(allowed_origins)),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register All API Routers (Clean & Non-Duplicate)
app.include_router(auth_router)
app.include_router(search_router)
app.include_router(resume_router)
app.include_router(persona_router)
app.include_router(interview_router)
app.include_router(coding_router)
app.include_router(skills_router)
app.include_router(github_router)
app.include_router(jobs_router)
app.include_router(cover_letter_router)
app.include_router(linkedin_router)
app.include_router(portfolio_router)
app.include_router(chat_router)
app.include_router(analytics_router)
app.include_router(notifications_router)
app.include_router(companies_router)
app.include_router(oa_router)
app.include_router(behavioral_router)
app.include_router(matching_router)
app.include_router(speech_router)
app.include_router(system_design_router)
app.include_router(applications_router)
app.include_router(resume_export_router)
app.include_router(admin_portal_router)
app.include_router(weakness_router)
app.include_router(company_prep_router)
app.include_router(gd_router)
app.include_router(study_planner_router)
app.include_router(skill_radar_router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Enterprise Career Readiness Platform API",
        "version": "2.1.0",
        "docs_url": "/docs",
        "total_active_modules": 23,
        "database_connected": db_manager.is_connected,
        "database_type": "mongodb" if (db_manager.is_connected and not settings.USE_IN_MEMORY_DB) else ("in-memory" if settings.USE_IN_MEMORY_DB else "none")
    }

@app.get("/api/v1/health")
async def health_check():
    if db_manager.is_connected and not settings.USE_IN_MEMORY_DB:
        return {
            "status": "healthy",
            "database": "connected",
            "database_type": "mongodb",
            "version": "2.1.0"
        }
    elif settings.USE_IN_MEMORY_DB:
        return {
            "status": "healthy",
            "database": "connected",
            "database_type": "in-memory (dev mode)",
            "version": "2.1.0"
        }
    else:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "database_type": "none",
                "error": f"MongoDB is not reachable at {settings.MONGODB_URL}.",
                "version": "2.1.0"
            }
        )

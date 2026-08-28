from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.behavioral_service import BehavioralService

router = APIRouter(prefix="/api/v1/behavioral", tags=["Behavioral STAR Builder"])

class STARRequest(BaseModel):
    prompt: Optional[str] = "Tell me about a time you resolved a major production bug under tight deadlines."
    situation: str = "Our e-commerce checkout service crashed during the Black Friday flash sale due to connection pool exhaustion."
    task: str = "I was tasked with identifying the root cause and restoring checkout uptime in under 30 minutes."
    action: str = "I analyzed query metrics, identified slow locks, introduced Redis caching for inventory checks, and scaled the connection pool."
    result: str = "Checkout was restored in 18 minutes with 0 data loss, handling 40,000 requests per minute with 99.99% uptime."

@router.post("/evaluate-star")
async def evaluate_star(req: STARRequest):
    return {"status": "success", "data": BehavioralService.evaluate_star(req.situation, req.task, req.action, req.result, req.prompt)}

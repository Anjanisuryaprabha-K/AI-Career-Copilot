from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.services.system_design_service import SystemDesignService

router = APIRouter(prefix="/api/v1/system-design", tags=["System Design & Architecture Evaluator"])

class ArchitectureRequest(BaseModel):
    prompt: Optional[str] = "Design a High-Throughput URL Shortener"
    components: Optional[List[str]] = ["Client", "Load Balancer (Nginx)", "FastAPI Microservices", "Redis Cache", "MongoDB Sharded Cluster", "Kafka Queue"]

@router.post("/evaluate-architecture")
async def evaluate_architecture(req: ArchitectureRequest):
    return {"status": "success", "data": SystemDesignService.evaluate_architecture(req.components or [], req.prompt or "")}

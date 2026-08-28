from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class SearchRequest(BaseModel):
    query: str
    page: Optional[int] = 1
    limit: Optional[int] = 10
    type: Optional[str] = "all" # all, jobs, companies, skills

class SearchResultItem(BaseModel):
    title: str
    url: str
    snippet: str
    source: str
    published_date: Optional[str] = None
    cached: Optional[bool] = False
    retrieved_at: Optional[str] = None

class SearchResponse(BaseModel):
    success: bool
    query: str
    total_results: int
    results: List[SearchResultItem]
    source_transparency: Dict[str, Any]

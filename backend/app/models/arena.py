from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class TestCaseItem(BaseModel):
    id: str
    input_val: str
    expected_val: str
    is_hidden: Optional[bool] = False

class ArenaProblem(BaseModel):
    id: str
    title: str
    topic_id: str
    topic_name: str
    category: str
    difficulty: str
    description: str
    constraints: Optional[str] = ""
    starter_code: Dict[str, str]
    visible_test_cases: List[TestCaseItem]
    hidden_test_cases: List[TestCaseItem]
    completed: Optional[bool] = False

class TopicStatusItem(BaseModel):
    topic_id: str
    topic_name: str
    category: str
    completedCount: int
    totalCount: int
    isCompleted: bool

class ArenaUserProgress(BaseModel):
    userId: str
    completedProblems: List[str]
    topicStatus: Dict[str, TopicStatusItem]
    overallSolved: int


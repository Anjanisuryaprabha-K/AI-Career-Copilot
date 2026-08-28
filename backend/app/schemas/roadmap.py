from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class VideoItem(BaseModel):
    video_id: str
    title: str
    channel: str
    concept: str
    duration: str
    youtube_url: str
    embed_url: Optional[str] = ""
    practice_link: Optional[str] = ""
    is_completed: Optional[bool] = False

class WeeklyModule(BaseModel):
    week_number: int
    week_title: str
    learning_objectives: List[str]
    videos: List[VideoItem]
    completed_count: Optional[int] = 0
    total_count: Optional[int] = 0
    progress_percentage: Optional[int] = 0

class RoadmapTrack(BaseModel):
    track_id: str
    title: str
    category: str
    difficulty: str
    total_weeks: int
    weeks: List[WeeklyModule]

class ToggleVideoProgressRequest(BaseModel):
    track_id: str
    video_id: str
    is_completed: bool

class UserTrackProgressResponse(BaseModel):
    status: str
    user_id: str
    track_id: str
    completed_video_ids: List[str]
    overall_completion_rate: int
    total_videos: int
    completed_videos_count: int
    remaining_videos_count: int

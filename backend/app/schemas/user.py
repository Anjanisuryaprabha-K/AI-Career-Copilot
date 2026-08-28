from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class PlatformProfile(BaseModel):
    username: Optional[str] = ""
    isConnected: Optional[bool] = False
    lastSynced: Optional[str] = None

class CodingProfiles(BaseModel):
    leetcode: Optional[PlatformProfile] = Field(default_factory=PlatformProfile)
    hackerrank: Optional[PlatformProfile] = Field(default_factory=PlatformProfile)

class UserBase(BaseModel):
    email: str
    name: str
    target_role: Optional[str] = "Software Engineer"
    skills: Optional[List[str]] = []
    location: Optional[str] = "India"
    experience: Optional[str] = "Student / Fresh Graduate"
    education: Optional[str] = "B.Tech Computer Science"
    github: Optional[str] = ""
    linkedin: Optional[str] = ""
    portfolio: Optional[str] = ""
    codingProfiles: Optional[CodingProfiles] = Field(default_factory=CodingProfiles)

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    target_role: Optional[str] = "Software Engineer"

class UserLogin(BaseModel):
    email: str
    password: str

class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    target_role: Optional[str] = None
    skills: Optional[List[str]] = None
    location: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None
    readiness_score: Optional[float] = None
    codingProfiles: Optional[CodingProfiles] = None

class ConnectProfilesRequest(BaseModel):
    leetcode_username: Optional[str] = None
    hackerrank_username: Optional[str] = None

class UserSettingsUpdate(BaseModel):
    theme: Optional[str] = "dark"
    notifications: Optional[bool] = True
    target_roles: Optional[List[str]] = []
    preferred_locations: Optional[List[str]] = []
    remote_preference: Optional[bool] = True
    privacy_settings: Optional[Dict[str, Any]] = {}

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    target_role: str
    readiness_score: float
    skills: List[str]
    location: Optional[str] = ""
    experience: Optional[str] = ""
    education: Optional[str] = ""
    github: Optional[str] = ""
    linkedin: Optional[str] = ""
    portfolio: Optional[str] = ""
    settings: Optional[Dict[str, Any]] = {}
    codingProfiles: Optional[Dict[str, Any]] = {}
    created_at: Optional[str] = ""

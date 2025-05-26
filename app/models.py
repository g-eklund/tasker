from pydantic import BaseModel
from typing import Dict, Any, Optional
import time

class Challenge(BaseModel):
    item_id: int
    start_time: float
    time_limit: int = 60
    completed: bool = False
    success: bool = False

class ChallengeResult(BaseModel):
    status: str
    message: str
    points: Optional[int] = None
    completed: bool
    confidence: Optional[float] = None
    detected_objects: Optional[list] = None

class SessionStats(BaseModel):
    total_successful_challenges: int
    average_duration: float

# In-memory storage (for development - replace with Redis/database in production)
active_challenges: Dict[str, Dict] = {}
user_sessions: Dict[str, Dict[str, Any]] = {} 
import time
import uuid
import random
import os
from typing import Optional
from fastapi import APIRouter, Request, Response, Cookie, File, UploadFile, HTTPException

from .config import CONFIG
from .models import Challenge, ChallengeResult, SessionStats, active_challenges, user_sessions
from .utils import get_user_and_session_ids
from .supabase_client import supabase
from .image_recognition import analyze_image, get_points_for_match

# Create router
router = APIRouter()

@router.get("/")
async def root():
    """API root endpoint - redirects to React frontend"""
    return {
        "message": "House Hunt Challenge API",
        "version": CONFIG["app"]["version"],
        "frontend_url": "Deploy your React frontend to access the game",
        "api_docs": "/docs"
    }

@router.get("/api/config")
async def get_config():
    """Get game configuration for frontend"""
    return {
        "challenge_duration": CONFIG["challenge"]["time"]["default_duration"],
        "max_points": CONFIG["challenge"]["points"]["goal"],
        "max_points_per_challenge": CONFIG["challenge"]["points"]["max_per_challenge"],
        "ui": CONFIG["ui"],
        "items": CONFIG["content"]["items"]
    }

@router.post("/api/new-challenge")
async def new_challenge(
    request: Request, 
    response: Response, 
    user_id: Optional[str] = Cookie(None), 
    session_id: Optional[str] = Cookie(None)
):
    """Create a new challenge. Use user/session IDs."""
    user_id, session_id = get_user_and_session_ids(request, response, user_id, session_id, user_sessions)
    
    # Select a random challenge item
    challenge_item = random.choice(CONFIG["content"]["items"])
    
    # Generate unique challenge id
    challenge_id = str(uuid.uuid4())
    
    # Create and store the challenge
    challenge = Challenge(
        item_id=challenge_item["id"],
        start_time=time.time(),
        time_limit=CONFIG["challenge"]["time"]["default_duration"]
    )
    
    active_challenges[challenge_id] = {
        "item": challenge_item,
        "start_time": challenge.start_time,
        "time_limit": challenge.time_limit,
        "completed": False,
        "success": False,
        "user_id": user_id,
        "session_id": session_id
    }
    
    response_data = {
        "challenge_id": challenge_id,
        "item": challenge_item,
        "time_limit": challenge.time_limit,
        "start_time": challenge.start_time,
        "session_id": session_id
    }
    
    # Debug logging
    print(f"New challenge response: {response_data}")
    
    return response_data

@router.post("/api/submit-photo/{challenge_id}")
async def submit_photo(challenge_id: str, photo: UploadFile = File(...)):
    """Submit a photo for a challenge. Log results to Supabase."""
    if challenge_id not in active_challenges:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    challenge = active_challenges[challenge_id]
    
    # Check if time has expired
    elapsed_time = time.time() - challenge["start_time"]
    if elapsed_time > challenge["time_limit"]:
        challenge["completed"] = True
        # Log event as failure
        supabase.table("challenge-events").insert({
            "user_id": challenge["user_id"],
            "session_id": challenge["session_id"],
            "success": False,
            "duration": float(elapsed_time)
        }).execute()
        return {"status": "failed", "message": "Time expired", "completed": True}
    
    # Read the photo data
    contents = await photo.read()
    
    # Use image recognition to analyze the photo
    analysis_result = analyze_image(
        contents, 
        challenge["item"]["name"],
        confidence_threshold=CONFIG["image_recognition"]["confidence_threshold"]
    )
    
    if analysis_result["is_match"]:
        challenge["completed"] = True
        challenge["success"] = True
        
        # Calculate points based on how quickly they found the item
        points = get_points_for_match(elapsed_time, challenge["time_limit"])
        
        # Update session points in session table
        prev = supabase.table("sessions").select("points").eq("session_id", challenge["session_id"]).single().execute()
        curr_points = prev.data["points"] if prev.data else 0
        supabase.table("sessions").update({"points": curr_points + points}).eq("session_id", challenge["session_id"]).execute()
        
        # Log event as success
        supabase.table("challenge-events").insert({
            "user_id": challenge["user_id"],
            "session_id": challenge["session_id"],
            "success": True,
            "duration": float(elapsed_time)
        }).execute()
        
        return {
            "status": "success", 
            "message": analysis_result["message"],
            "points": points,
            "completed": True,
            "confidence": analysis_result["confidence"],
        }
    else:
        # Log event as failure but not completed
        return {
            "status": "failed", 
            "message": analysis_result["message"],
            "completed": False,
            "confidence": analysis_result["confidence"],
            }

@router.get("/api/challenge-status/{challenge_id}")
async def challenge_status(challenge_id: str):
    """Get the status of a challenge"""
    if challenge_id not in active_challenges:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    challenge = active_challenges[challenge_id]
    elapsed_time = time.time() - challenge["start_time"]
    time_remaining = max(0, challenge["time_limit"] - elapsed_time)
    
    # Auto-complete if time expired
    if time_remaining <= 0 and not challenge["completed"]:
        challenge["completed"] = True
    
    return {
        "completed": challenge["completed"],
        "success": challenge["success"],
        "time_remaining": time_remaining,
        "item": challenge["item"]
    }

@router.get("/api/stats")
async def get_stats():
    """Get overall statistics"""
    total_challenges = len(active_challenges)
    successful_challenges = sum(1 for c in active_challenges.values() if c["success"])
    
    avg_completion_time = 0
    if successful_challenges > 0:
        completion_times = [
            time.time() - c["start_time"] 
            for c in active_challenges.values() 
            if c["success"]
        ]
        avg_completion_time = sum(completion_times) / len(completion_times)
    
    return {
        "total_challenges": total_challenges,
        "successful_challenges": successful_challenges,
        "success_rate": successful_challenges / total_challenges if total_challenges > 0 else 0,
        "avg_completion_time": round(avg_completion_time, 2)
    }

@router.get("/api/session-stats/{session_id}")
async def get_session_stats(session_id: str):
    """Get statistics for a specific session from Supabase"""
    try:
        # Get all successful challenge events for this session
        events_response = supabase.table("challenge-events").select("duration").eq("session_id", session_id).eq("success", True).execute()
        
        if not events_response.data:
            return {
                "total_successful_challenges": 0,
                "average_duration": 0
            }
        
        durations = [event["duration"] for event in events_response.data]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            "total_successful_challenges": len(durations),
            "average_duration": round(avg_duration, 1)
        }
    except Exception as e:
        # Return default values if there's an error
        return {
            "total_successful_challenges": 0,
            "average_duration": 0
        }

@router.get("/debug/env")
async def debug_env():
    """Debug endpoint to check environment variables (remove in production)"""
    env_vars = {}
    for key, value in os.environ.items():
        if key.startswith("SUPABASE"):
            env_vars[key] = f"Set ({len(value)} chars)" if value else "Empty"
        elif key in ["PORT", "HOST", "RAILWAY_", "NIXPACKS_"]:
            env_vars[key] = f"Set ({len(str(value))} chars)" if value else "Empty"
    
    return {
        "supabase_vars": {k: v for k, v in env_vars.items() if k.startswith("SUPABASE")},
        "railway_vars": {k: v for k, v in env_vars.items() if "RAILWAY" in k},
        "total_env_vars": len(os.environ),
        "all_env_keys": list(os.environ.keys())[:20]  # First 20 keys for debugging
    }

@router.get("/health")
async def health_check():
    """Simple health check endpoint for Railway"""
    return {
        "status": "healthy", 
        "message": "House Hunt Challenge API is running",
        "port": os.environ.get("PORT", "not set"),
        "host": os.environ.get("HOST", "not set"),
        "railway_environment": os.environ.get("RAILWAY_ENVIRONMENT", "not set")
    } 
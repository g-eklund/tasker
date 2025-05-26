import random
import time
import io
import yaml
import os
import uuid
from typing import List, Dict, Optional, Any
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException, Response, Cookie
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn



# Supabase client
from app.supabase_client import supabase


from dotenv import load_dotenv
load_dotenv()

# Import our image recognition module
from app.image_recognition import analyze_image, get_points_for_match

# Load configuration
def load_config():
    with open("config.yaml", "r") as config_file:
        return yaml.safe_load(config_file)

CONFIG = load_config()

# Create the FastAPI app
app = FastAPI(
    title=CONFIG["app"]["title"],
    description=CONFIG["app"]["description"],
    version=CONFIG["app"]["version"]
)

# Add CORS middleware to allow frontend requests
import os
allowed_origins = [
    "http://localhost:3000",  # React dev server
    "https://*.vercel.app",   # Vercel deployments
    "https://your-app-name.vercel.app",  # Replace with your actual domain
]

# Add production domain from environment variable if available
if os.environ.get("FRONTEND_URL"):
    allowed_origins.append(os.environ.get("FRONTEND_URL"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory=CONFIG["content"]["paths"]["static_dir"]), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory=CONFIG["content"]["paths"]["templates_dir"])

# Define challenge items from config
CHALLENGE_ITEMS = CONFIG["content"]["items"]

# Store active challenges
active_challenges: Dict[str, Dict] = {}

# Simple in-memory user/session cache. For prod, use persistent store or auth
user_sessions: Dict[str, Dict[str, Any]] = {}

# Helper functions
def generate_user_id():
    return str(random.getrandbits(63))

def generate_session_id():
    return str(random.getrandbits(63))

# Fetch or create user_id & session_id for this client (cookie-based for now)
def get_user_and_session_ids(request: Request, response: Response, user_id: Optional[str], session_id: Optional[str]):
    if not user_id:
        user_id = generate_user_id()
        response.set_cookie(key="user_id", value=user_id, httponly=True)
    if not session_id:
        session_id = generate_session_id()
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        # Also create a session entry in Supabase
        # (insert new session row with points=0)
        supabase.table("sessions").insert({
            "session_id": session_id,
            "user_id": user_id,
            "points": 0
        }).execute()
    # Save mapping for reference (dev only, in-memory)
    user_sessions[user_id] = {"session_id": session_id}
    return user_id, session_id

class Challenge(BaseModel):
    item_id: int
    start_time: float
    time_limit: int = CONFIG["challenge"]["time"]["default_duration"]
    completed: bool = False
    success: bool = False

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, response: Response, user_id: Optional[str] = Cookie(None), session_id: Optional[str] = Cookie(None)):
    """Render the home page. Also create user/session IDs if needed (cookie-based)"""
    # Cookies handled automatically
    get_user_and_session_ids(request, response, user_id, session_id)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "challenge_duration": CONFIG["challenge"]["time"]["default_duration"],
        "max_points": CONFIG["challenge"]["points"]["goal"],
        "max_points_per_challenge": CONFIG["challenge"]["points"]["max_per_challenge"],
        "ui": CONFIG["ui"]
    })

@app.get("/challenge-complete", response_class=HTMLResponse)
async def challenge_complete(request: Request):
    """Render the challenge complete page"""
    return templates.TemplateResponse("challenge-complete.html", {
        "request": request,
        "max_points": CONFIG["challenge"]["points"]["goal"]
    })

@app.post("/api/new-challenge")
async def new_challenge(request: Request, response: Response, user_id: Optional[str] = Cookie(None), session_id: Optional[str] = Cookie(None)):
    """Create a new challenge. Use user/session IDs."""
    user_id, session_id = get_user_and_session_ids(request, response, user_id, session_id)
    # Select a random challenge item
    challenge_item = random.choice(CHALLENGE_ITEMS)
    # Generate unique challenge id (use uuid)
    challenge_id = str(uuid.uuid4())
    # Create and store the challenge
    challenge = Challenge(
        item_id=challenge_item["id"],
        start_time=time.time()
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
    # Return challenge details
    return {
        "challenge_id": challenge_id,
        "item": challenge_item,
        "time_limit": challenge.time_limit,
        "start_time": challenge.start_time,
        "session_id": session_id
    }

@app.post("/api/submit-photo/{challenge_id}")
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
    # Use our image recognition module to analyze the photo
    analysis_result = analyze_image(
        contents, 
        challenge["item"]["id"], 
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
            "detected_objects": analysis_result["detected_objects"]
        }
    else:
        # Log event as failure but not completed (no session points change)
        return {
            "status": "failed", 
            "message": analysis_result["message"],
            "completed": False,
            "confidence": analysis_result["confidence"],
            "detected_objects": analysis_result["detected_objects"]
        }

@app.get("/api/challenge-status/{challenge_id}")
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

# Add a statistics endpoint to track user progress
@app.get("/api/stats")
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

@app.get("/api/session-stats/{session_id}")
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

@app.get("/debug/env")
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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", CONFIG["app"]["port"]))
    host = os.environ.get("HOST", CONFIG["app"]["host"])
    
    uvicorn.run(
        "main:app", 
        host=host, 
        port=port, 
        reload=CONFIG["app"]["debug"]
    )

import random
import time
import io
import yaml
import os
from typing import List, Dict, Optional, Any
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

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

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory=CONFIG["content"]["paths"]["static_dir"]), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory=CONFIG["content"]["paths"]["templates_dir"])

# Define challenge items from config
CHALLENGE_ITEMS = CONFIG["content"]["items"]

# Store active challenges
active_challenges: Dict[str, Dict] = {}

class Challenge(BaseModel):
    item_id: int
    start_time: float
    time_limit: int = CONFIG["challenge"]["time"]["default_duration"]
    completed: bool = False
    success: bool = False

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/challenge-complete", response_class=HTMLResponse)
async def challenge_complete(request: Request):
    """Render the challenge complete page"""
    return templates.TemplateResponse("challenge-complete.html", {"request": request})

@app.post("/api/new-challenge")
async def new_challenge():
    """Create a new challenge"""
    # Select a random challenge item
    challenge_item = random.choice(CHALLENGE_ITEMS)
    
    # Generate a unique ID for this challenge
    challenge_id = str(int(time.time()))
    
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
        "success": False
    }
    
    # Return challenge details
    return {
        "challenge_id": challenge_id,
        "item": challenge_item,
        "time_limit": challenge.time_limit,
        "start_time": challenge.start_time
    }

@app.post("/api/submit-photo/{challenge_id}")
async def submit_photo(challenge_id: str, photo: UploadFile = File(...)):
    """Submit a photo for a challenge"""
    if challenge_id not in active_challenges:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    challenge = active_challenges[challenge_id]
    
    # Check if time has expired
    elapsed_time = time.time() - challenge["start_time"]
    if elapsed_time > challenge["time_limit"]:
        challenge["completed"] = True
        return {"status": "failed", "message": "Time expired", "completed": True}
    
    # Read the photo data
    contents = await photo.read()
    
    # Use our image recognition module to analyze the photo with confidence threshold from config
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
        
        return {
            "status": "success", 
            "message": analysis_result["message"],
            "points": points,
            "completed": True,
            "confidence": analysis_result["confidence"],
            "detected_objects": analysis_result["detected_objects"]
        }
    else:
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

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=CONFIG["app"]["host"], 
        port=CONFIG["app"]["port"], 
        reload=CONFIG["app"]["debug"]
    )

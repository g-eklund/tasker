import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import app modules
from app.config import CONFIG
from app.routes import router

# Create the FastAPI app
app = FastAPI(
    title=CONFIG["app"]["title"],
    description=CONFIG["app"]["description"],
    version=CONFIG["app"]["version"]
)

# Add CORS middleware to allow frontend requests
# For now, allow all origins to debug the issue
# TODO: Restrict this in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for challenge images)
app.mount("/static", StaticFiles(directory=CONFIG["content"]["paths"]["static_dir"]), name="static")

# Include all routes
app.include_router(router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", CONFIG["app"]["port"]))
    host = os.environ.get("HOST", CONFIG["app"]["host"])
    
    print(f"Starting server on {host}:{port}")
    print(f"Environment: {os.environ.get('RAILWAY_ENVIRONMENT', 'local')}")
    
    uvicorn.run(
        "main:app", 
        host=host, 
        port=port, 
        reload=CONFIG["app"]["debug"]
    )

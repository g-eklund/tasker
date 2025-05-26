import random
import os
from typing import Optional, Tuple, Dict, Any
from fastapi import Request, Response
from .supabase_client import supabase

def generate_user_id() -> str:
    """Generate a unique user ID"""
    return str(random.getrandbits(63))

def generate_session_id() -> str:
    """Generate a unique session ID"""
    return str(random.getrandbits(63))

def get_user_and_session_ids(
    request: Request, 
    response: Response, 
    user_id: Optional[str], 
    session_id: Optional[str],
    user_sessions: Dict[str, Dict[str, Any]]
) -> Tuple[str, str]:
    """Fetch or create user_id & session_id for this client (cookie-based)"""
    if not user_id:
        user_id = generate_user_id()
        response.set_cookie(key="user_id", value=user_id, httponly=True)
    
    if not session_id:
        session_id = generate_session_id()
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        # Create a session entry in Supabase
        supabase.table("sessions").insert({
            "session_id": session_id,
            "user_id": user_id,
            "points": 0
        }).execute()
    
    # Save mapping for reference (dev only, in-memory)
    user_sessions[user_id] = {"session_id": session_id}
    return user_id, session_id 
import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Debug logging for Railway deployment
print(f"SUPABASE_URL loaded: {'Yes' if SUPABASE_URL else 'No'}")
print(f"SUPABASE_ANON_KEY loaded: {'Yes' if SUPABASE_ANON_KEY else 'No'}")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL environment variable is required")
if not SUPABASE_ANON_KEY:
    raise ValueError("SUPABASE_ANON_KEY environment variable is required")

supabase: Client = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_ANON_KEY)

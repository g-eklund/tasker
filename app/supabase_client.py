import os
from supabase import create_client, Client

# Try to load .env file only if it exists (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available in production, which is fine
    pass

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Debug logging for Railway deployment
print(f"Environment variables check:")
print(f"SUPABASE_URL loaded: {'Yes' if SUPABASE_URL else 'No'}")
print(f"SUPABASE_ANON_KEY loaded: {'Yes' if SUPABASE_ANON_KEY else 'No'}")

# Print first few characters for debugging (without exposing full keys)
if SUPABASE_URL:
    print(f"SUPABASE_URL starts with: {SUPABASE_URL[:20]}...")
if SUPABASE_ANON_KEY:
    print(f"SUPABASE_ANON_KEY starts with: {SUPABASE_ANON_KEY[:20]}...")

# List all environment variables that start with SUPABASE for debugging
print("All SUPABASE environment variables:")
for key, value in os.environ.items():
    if key.startswith("SUPABASE"):
        print(f"  {key}: {'Set' if value else 'Empty'}")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL environment variable is required")
if not SUPABASE_ANON_KEY:
    raise ValueError("SUPABASE_ANON_KEY environment variable is required")

supabase: Client = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_ANON_KEY)

import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from supabase import Client, create_client

# Load environment from common locations to be flexible with layout.
# 1) Nearest .env from the current working directory (when running the app)
# 2) backend/.env relative to this file
# 3) project-root .env relative to this file

# Try nearest .env based on the current working directory 
nearest_env = find_dotenv(usecwd=True)
if nearest_env:
    load_dotenv(nearest_env)

# Then try backend/.env (same directory level as this module's parent)
backend_env = Path(__file__).resolve().parents[1] / ".env"
if backend_env.exists():
    load_dotenv(backend_env)

# Finally try project-root .env (two levels up)
root_env = Path(__file__).resolve().parents[2] / ".env"
if root_env.exists():
    load_dotenv(root_env)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "http://127.0.0.1:54321")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
if not SUPABASE_KEY:
    raise ValueError("Supabase key is not set in environment variables.")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
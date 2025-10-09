# supabase_client.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables (local development)
load_dotenv()

# Fetch Supabase URL and KEY from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or KEY is missing in environment variables")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

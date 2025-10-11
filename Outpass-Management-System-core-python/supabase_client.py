import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get keys from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials missing in .env file!")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


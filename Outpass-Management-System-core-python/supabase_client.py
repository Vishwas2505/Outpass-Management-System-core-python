
import sys
import os

# --- CRITICAL FIX START ---
# 1. Get the directory where this script (streamlit_app.py) is located.
current_dir = os.path.dirname(os.path.abspath())

# 2. Add this directory to the Python path.
# This makes local modules (like supabase_client.py, which is in the same folder) importable.
sys.path.append(current_dir)
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

try:
    supabase: Client = create_client(url, key)
    print("✅ Supabase client initialized successfully!")
except Exception as e:
    print(f"❌ Error initializing Supabase client: {e}")
    supabase = None


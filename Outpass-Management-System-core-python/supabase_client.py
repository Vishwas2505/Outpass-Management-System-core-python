import sys
import os

current_dir = os.path.dirname(os.path.abspath(https://github.com/Vishwas2505/Outpass-Management-System-core-python/tree/main/Outpass-Management-System-core-python))

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



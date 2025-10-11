# supabase_client.py file content
import os
# This line requires the 'supabase' package listed in requirements.txt
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

try:
    # This is the actual connection attempt
    supabase: Client = create_client(url, key)
    # Note: print() output won't be visible in the Streamlit app itself, only in the logs.
except Exception as e:
    # Log the error if connection fails
    supabase = None

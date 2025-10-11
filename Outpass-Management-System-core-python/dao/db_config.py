from dotenv import load_dotenv
load_dotenv()  # Loads environment variables from a .env file locally

import os
from supabase import create_client, Client

def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("Supabase URL or Key is not set. Please check your environment variables or Streamlit Secrets.")
    
    return create_client(url, key)

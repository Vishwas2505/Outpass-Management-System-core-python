from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env in project root

def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise EnvironmentError("Please create a .env file with SUPABASE_URL and SUPABASE_KEY")
    return create_client(url, key)

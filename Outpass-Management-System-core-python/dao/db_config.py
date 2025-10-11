import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env file locally (ignored on Streamlit Cloud)
load_dotenv()

def get_supabase_client() -> Client:
    """
    Returns a Supabase client. Works locally (.env) or on Streamlit Cloud (Secrets).
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError(
            "Supabase URL or Key not set! "
            "Locally use a .env file, on Streamlit Cloud use Secrets."
        )

    return create_client(url, key)

import os
import streamlit as st   # <-- ADD THIS
from supabase import create_client, Client

def get_supabase_client() -> Client:
    """
    Returns a Supabase sync client using Streamlit secrets.
    Make sure SUPABASE_URL and SUPABASE_KEY are set in Streamlit secrets.
    """
    url = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError(
            "Supabase URL or Key not set! "
            "Use .env locally or Secrets in Streamlit Cloud."
        )

    return create_client(url, key)

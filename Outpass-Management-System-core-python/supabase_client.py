import os
from supabase import create_client, Client
import streamlit as st

# Try both Streamlit secrets and .env for local
SUPABASE_URL = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials missing! Add to Streamlit secrets or .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

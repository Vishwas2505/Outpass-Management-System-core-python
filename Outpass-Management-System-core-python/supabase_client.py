# supabase_client.py
import os
from supabase import create_client, Client
import streamlit as st

# ✅ Load from Streamlit Cloud Secrets or environment variables
SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ Supabase credentials missing! Add them to Streamlit Secrets or .env locally.")

# Initialize client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("✅ Supabase client initialized successfully!")

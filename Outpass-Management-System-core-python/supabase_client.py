# supabase_client.py
import streamlit as st
from supabase import create_client, Client

# Load Supabase credentials from Streamlit secrets
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except KeyError:
    st.error("Supabase URL or KEY not found in Streamlit secrets!")
    st.stop()

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# supabase_client.py
import streamlit as st
from supabase import create_client, Client
import os

# Use Streamlit secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    st.write("Supabase client initialized!")
except Exception as e:
    st.error(f"Error initializing Supabase client: {e}")

from supabase import create_client
import streamlit as st

def get_supabase_client():
    """
    Returns a Supabase client using secrets from Streamlit Cloud.
    Make sure to set SUPABASE_URL and SUPABASE_KEY in Streamlit secrets.
    """
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

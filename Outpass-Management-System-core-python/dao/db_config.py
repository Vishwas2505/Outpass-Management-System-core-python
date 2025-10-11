import streamlit as st
from supabase import create_client

def get_supabase_client():
    """
    Returns a Supabase client using secrets from Streamlit Cloud.
    Make sure SUPABASE_URL and SUPABASE_KEY are set in Streamlit secrets.
    """
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except KeyError:
        raise ValueError("Supabase secrets are missing. Set SUPABASE_URL and SUPABASE_KEY in Streamlit secrets.")

    return create_client(url, key)

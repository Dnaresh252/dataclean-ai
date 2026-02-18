"""
Database Configuration
======================

Supabase client setup for production database.
"""

from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase() -> Client:
    """
    Get Supabase client instance.
    
    Returns:
        Supabase client
    """
    return supabase
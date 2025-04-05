"""
Supabase client configuration and initialization.
Provides a configured Supabase client instance for database operations.
"""
from supabase import create_client
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables for Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")  # Using anon key for client operations

print("Debug - SUPABASE_URL:", SUPABASE_URL)
print("Debug - SUPABASE_KEY:", SUPABASE_KEY)

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError(
        "Missing required environment variables: SUPABASE_URL and/or SUPABASE_ANON_KEY"
    )

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

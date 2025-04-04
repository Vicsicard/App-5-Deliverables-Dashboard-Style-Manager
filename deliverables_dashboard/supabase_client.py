"""
Supabase client configuration and initialization.
Provides a configured Supabase client instance for database operations.
"""
from supabase import create_client
import os
from typing import Optional

# Environment variables for Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # Using service role key for backend operations

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError(
        "Missing required environment variables: SUPABASE_URL and/or SUPABASE_SERVICE_ROLE_KEY"
    )

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

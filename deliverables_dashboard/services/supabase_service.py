"""
Supabase service configuration and initialization.
"""
import os
from supabase import create_client
from typing import Dict, List, Optional
from datetime import datetime, timezone

def get_supabase_client():
    """Get configured Supabase client, checking environment variables."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        raise EnvironmentError(
            "Missing required environment variables: SUPABASE_URL and/or SUPABASE_SERVICE_ROLE_KEY"
        )
    
    return create_client(url, key)

def fetch_user_files(user_id: str, transcript_id: Optional[str] = None) -> List[Dict]:
    """
    Fetch transcript files metadata for a specific user from Supabase.
    """
    try:
        supabase = get_supabase_client()
        query = supabase.table("transcript_files").select("*").eq("user_id", user_id)
        
        if transcript_id:
            query = query.eq("transcript_id", transcript_id)

        result = query.execute()
        return result.data if result else []
        
    except Exception as e:
        print(f"Error fetching transcript files: {str(e)}")
        raise Exception(f"Failed to fetch transcript files for user {user_id}") from e

def get_signed_url(bucket: str, path: str, expiry_seconds: int = 3600) -> str:
    """
    Generate a signed URL for secure access to a file in Supabase Storage.
    """
    try:
        supabase = get_supabase_client()
        result = supabase.storage.from_(bucket).create_signed_url(path, expiry_seconds)
        
        if result.get('error'):
            raise Exception(result['error']['message'])
            
        signed_url = result.get('signedURL')
        if not signed_url:
            raise Exception(f"Failed to generate signed URL for {bucket}/{path}")
            
        return signed_url
        
    except Exception as e:
        print(f"Error generating signed URL for {bucket}/{path}: {str(e)}")
        raise Exception(f"Failed to generate signed URL for file {path} in bucket {bucket}") from e

def approve_file(file_id: str) -> Dict:
    """
    Mark a file as approved and record the approval timestamp.
    """
    try:
        supabase = get_supabase_client()
        result = (supabase.table("transcript_files")
                 .update({
                     "status": "approved",
                     "approved_at": datetime.now(timezone.utc).isoformat()
                 })
                 .eq("id", file_id)
                 .execute())
        
        if not result.data:
            raise Exception(f"No file found with ID {file_id}")
            
        return result.data[0]
    except Exception as e:
        print(f"Error approving file {file_id}: {str(e)}")
        raise Exception(f"Failed to approve file {file_id}") from e

def reject_file(file_id: str, reason: Optional[str] = None) -> Dict:
    """
    Mark a file as rejected with an optional reason.
    """
    try:
        supabase = get_supabase_client()
        update_data = {
            "status": "rejected",
            "rejected_at": datetime.now(timezone.utc).isoformat()
        }
        if reason:
            update_data["rejection_reason"] = reason
            
        result = (supabase.table("transcript_files")
                 .update(update_data)
                 .eq("id", file_id)
                 .execute())
        
        if not result.data:
            raise Exception(f"No file found with ID {file_id}")
            
        return result.data[0]
    except Exception as e:
        print(f"Error rejecting file {file_id}: {str(e)}")
        raise Exception(f"Failed to reject file {file_id}") from e

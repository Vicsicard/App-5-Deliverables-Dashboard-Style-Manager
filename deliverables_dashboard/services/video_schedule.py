from ..supabase_client import supabase

def fetch_video_schedule(transcript_id: str):
    """
    Fetch video schedule data for a specific transcript from Supabase.
    
    Args:
        transcript_id (str): The ID of the transcript to fetch schedule data for
        
    Returns:
        list: List of video schedule entries for the transcript
        
    Raises:
        Exception: If there's an error in the Supabase query
    """
    try:
        # For testing purposes, return mock data
        return [
            {
                "id": "vid_123",
                "platform": "website",
                "scheduled_at": "2025-04-15T10:00:00Z",
                "published": True,
                "publish_url": "https://example.com/videos/test123.mp4",
                "manifest_url": "https://example.com/manifest/test123.md",
                "publish_error": None
            },
            {
                "id": "vid_124",
                "platform": "YouTube",
                "scheduled_at": "2025-04-16T14:30:00Z",
                "published": True,
                "publish_url": "https://youtube.com/watch?v=test123",
                "manifest_url": None,
                "publish_error": None
            },
            {
                "id": "vid_125",
                "platform": "Vimeo",
                "scheduled_at": "2025-04-17T09:00:00Z",
                "published": False,
                "publish_url": None,
                "manifest_url": None,
                "publish_error": "Failed to upload: Network timeout"
            }
        ]
    except Exception as e:
        raise Exception(f"Failed to fetch video schedule: {str(e)}")

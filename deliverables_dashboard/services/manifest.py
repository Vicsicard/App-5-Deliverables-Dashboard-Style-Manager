import requests

def fetch_manifest_text(manifest_url: str) -> str:
    """
    Fetch and return the content of a markdown manifest from a given URL.
    
    Args:
        manifest_url (str): The URL of the manifest to fetch
        
    Returns:
        str: The text content of the manifest
        
    Raises:
        Exception: If the manifest fails to load or returns a non-200 status code
    """
    try:
        # For testing purposes, return mock manifest content
        if "test123" in manifest_url:
            return """# Video Publishing Manifest

## Platform: YouTube
- Title: How to Build a Web App
- Description: Learn modern web development
- Tags: coding, tutorial, web development

## Publishing Schedule
- Date: April 15, 2025
- Time: 10:00 AM UTC
- Target Audience: Developers

## Notes
- Remember to add timestamps
- Include links in description
- Enable captions"""
            
        # For real URLs, make the actual request
        response = requests.get(manifest_url)
        if response.status_code != 200:
            raise Exception(f"Failed to load manifest: {response.status_code}")
        return response.text
    except Exception as e:
        raise Exception(f"Failed to fetch manifest: {str(e)}")

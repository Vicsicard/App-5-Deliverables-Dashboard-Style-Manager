"""
Main controller for the deliverables dashboard, integrating file fetching, preview, and approval functionality.
"""
from typing import Dict, List, Optional
from itertools import groupby
from operator import itemgetter

from ..services import supabase_service

class DashboardController:
    def __init__(self):
        self.PREVIEW_URL_EXPIRY = 3600  # 1 hour
        self.SUPPORTED_PREVIEW_TYPES = {
            'video': ['.mp4'],
            'text': ['.md', '.json']
        }
    
    def get_user_files(self, user_id: str, transcript_id: Optional[str] = None) -> Dict[str, List[Dict]]:
        """
        Fetch all files for a user with preview URLs.
        
        Args:
            user_id (str): The ID of the user
            transcript_id (Optional[str]): Optional transcript ID filter
            
        Returns:
            Dict[str, List[Dict]]: Files grouped by transcript_id with preview URLs
        """
        # Fetch base file data
        files = supabase_service.fetch_user_files(user_id, transcript_id)
        
        # Add preview URLs and organize by type
        for file in files:
            file['preview_url'] = supabase_service.get_signed_url(
                file['bucket'],
                file['file_path'],
                self.PREVIEW_URL_EXPIRY
            )
            
            # Determine preview type
            extension = file.get('file_name', '').lower()
            if any(extension.endswith(ext) for ext in self.SUPPORTED_PREVIEW_TYPES['video']):
                file['preview_type'] = 'video'
            elif any(extension.endswith(ext) for ext in self.SUPPORTED_PREVIEW_TYPES['text']):
                file['preview_type'] = 'text'
            else:
                file['preview_type'] = 'unknown'
        
        # Group by transcript_id
        files.sort(key=itemgetter('transcript_id'))
        grouped_files = {
            transcript_id: list(group)
            for transcript_id, group in groupby(files, key=itemgetter('transcript_id'))
        }
        
        return grouped_files
    
    def approve_user_file(self, file_id: str) -> Dict:
        """
        Approve a file and return updated record.
        
        Args:
            file_id (str): The ID of the file to approve
            
        Returns:
            Dict: Updated file record
        """
        return supabase_service.approve_file(file_id)
    
    def reject_user_file(self, file_id: str, reason: Optional[str] = None) -> Dict:
        """
        Reject a file and return updated record.
        
        Args:
            file_id (str): The ID of the file to reject
            reason (Optional[str]): Optional reason for rejection
            
        Returns:
            Dict: Updated file record
        """
        return supabase_service.reject_file(file_id, reason)
    
    def get_file_preview_data(self, file_data: Dict) -> Dict:
        """
        Get formatted preview data for a file.
        
        Args:
            file_data (Dict): File metadata including preview_url and preview_type
            
        Returns:
            Dict: Preview configuration for the UI
        """
        preview_config = {
            'id': file_data['id'],
            'name': file_data['file_name'],
            'type': file_data['preview_type'],
            'url': file_data['preview_url'],
            'status': file_data.get('status', 'pending'),
            'approved_at': file_data.get('approved_at'),
            'rejected_at': file_data.get('rejected_at'),
            'rejection_reason': file_data.get('rejection_reason')
        }
        
        return preview_config

"""
Integration tests for Supabase functionality in the deliverables dashboard.
"""
import unittest
from unittest.mock import MagicMock, patch
import os
from datetime import datetime, timedelta, timezone
import logging
from deliverables_dashboard.controllers.dashboard_controller import DashboardController
from deliverables_dashboard.services import supabase_service
from deliverables_dashboard.utils.logging_config import setup_logger

logger = setup_logger()

class TestSupabaseIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.dashboard = DashboardController()
        self.test_user_id = "test-user-123"
        self.test_transcript_id = "test-transcript-456"
        
        # Mock data
        self.mock_file = {
            'id': 'test-file-1',
            'user_id': self.test_user_id,
            'transcript_id': self.test_transcript_id,
            'file_name': 'test.mp4',
            'bucket': 'videos',
            'file_path': 'test/path/test.mp4',
            'status': 'pending'
        }
        
    @patch('deliverables_dashboard.services.supabase_service.get_supabase_client')
    def test_file_metadata_retrieval(self, mock_get_client):
        """Test file metadata retrieval functionality."""
        # Setup mock client
        mock_client = MagicMock()
        mock_client.table().select().eq().execute.return_value.data = [self.mock_file]
        
        # Mock storage signed URL
        mock_storage = MagicMock()
        mock_storage.from_().create_signed_url.return_value = {
            'signedURL': 'https://example.com/signed-url'
        }
        mock_client.storage = mock_storage
        
        mock_get_client.return_value = mock_client
        
        # Test without transcript_id
        files = self.dashboard.get_user_files(self.test_user_id)
        self.assertIsInstance(files, dict)
        self.assertEqual(len(files), 1)
        
        # Verify mock was called correctly
        mock_client.table.assert_called_with("transcript_files")
        mock_client.table().select().eq.assert_called_with("user_id", self.test_user_id)
        
        logger.info(f"Retrieved {sum(len(f) for f in files.values())} total files")
        
    @patch('deliverables_dashboard.services.supabase_service.get_supabase_client')
    def test_signed_url_generation(self, mock_get_client):
        """Test signed URL generation and validation."""
        # Setup mock client
        mock_client = MagicMock()
        mock_signed_url = "https://example.com/signed-url?token=abc123"
        mock_client.storage.from_().create_signed_url.return_value = {
            'signedURL': mock_signed_url
        }
        mock_client.table().select().eq().execute.return_value.data = [self.mock_file]
        mock_get_client.return_value = mock_client
        
        # Test URL generation
        files = self.dashboard.get_user_files(self.test_user_id)
        first_transcript = next(iter(files.values()))
        file_data = first_transcript[0]
        
        preview_data = self.dashboard.get_file_preview_data(file_data)
        self.assertEqual(preview_data['url'], mock_signed_url)
        self.assertEqual(preview_data['type'], 'video')
        
        logger.info(
            f"Generated preview for {preview_data['name']}: "
            f"Type={preview_data['type']}, Valid URL=True"
        )
        
    @patch('deliverables_dashboard.services.supabase_service.get_supabase_client')
    def test_file_approval_workflow(self, mock_get_client):
        """Test file approval and rejection workflow."""
        # Setup mock client
        mock_client = MagicMock()
        
        # Setup mock for approval
        mock_approved_file = dict(self.mock_file)
        mock_approved_file['status'] = 'approved'
        mock_approved_file['approved_at'] = datetime.now(timezone.utc).isoformat()
        mock_client.table().update().eq().execute.return_value.data = [mock_approved_file]
        mock_get_client.return_value = mock_client
        
        # Test approval
        approved_file = self.dashboard.approve_user_file(self.mock_file['id'])
        self.assertEqual(approved_file['status'], 'approved')
        self.assertIsNotNone(approved_file['approved_at'])
        
        # Setup mock for rejection
        mock_rejected_file = dict(self.mock_file)
        mock_rejected_file['status'] = 'rejected'
        mock_rejected_file['rejection_reason'] = "Test rejection"
        mock_client.table().update().eq().execute.return_value.data = [mock_rejected_file]
        
        # Test rejection
        rejected_file = self.dashboard.reject_user_file(
            self.mock_file['id'],
            "Test rejection"
        )
        self.assertEqual(rejected_file['status'], 'rejected')
        self.assertEqual(rejected_file['rejection_reason'], "Test rejection")
        
        logger.info(
            f"Tested approval workflow on file {self.mock_file['id']}: "
            f"Approval and rejection successful"
        )

if __name__ == '__main__':
    unittest.main()

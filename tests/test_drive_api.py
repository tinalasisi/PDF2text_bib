# test_drive_api.py

import unittest
import tempfile
from unittest.mock import Mock, MagicMock, patch
from googleapiclient.http import MediaIoBaseDownload

import drive_api

class TestDriveAPI(unittest.TestCase):
    @patch.object(MediaIoBaseDownload, '__init__', return_value=None)  # Mock MediaIoBaseDownload's initialization
    @patch.object(MediaIoBaseDownload, 'next_chunk')  # Mock MediaIoBaseDownload's next_chunk method
    def test_download_pdf(self, mock_next_chunk, mock_init):
        # Set up mock objects
        mock_service = Mock()
        mock_request = Mock()
        mock_request.headers = {}  # add headers attribute to mock_request
        mock_service.files().get_media.return_value = mock_request

        mock_status = Mock()
        mock_status.progress = Mock(return_value=1)  # Mock the progress method to always return 1

        mock_next_chunk.side_effect = [(mock_status, False), (mock_status, True)]  # Mock next_chunk method

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Call the function with a mock service, file id, and file path in the temporary directory
            drive_api.download_pdf(mock_service, 'file_id', f'{temp_dir}/filename.pdf')

            # Check that the API was called with the correct arguments
            mock_service.files().get_media.assert_called_once_with(fileId='file_id')

            # Check that the next_chunk method was called
            mock_next_chunk.assert_called()

if __name__ == '__main__':
    unittest.main()

# test_pdf_processing.py

import unittest
from unittest.mock import Mock, patch, mock_open
from PyPDF2 import PdfReader

import pdf_processing

class TestPdfProcessing(unittest.TestCase):
    @patch('pdf_processing.PdfReader')
    @patch('builtins.open', new_callable=mock_open, read_data=b"mocked data")
    def test_pdf_to_text(self, mock_file, mock_reader):
        # Set up mock objects
        mock_pdf_reader = Mock()
        mock_pdf_reader.pages = [Mock(), Mock()]  # Set up mock objects for pages
        mock_pdf_reader.pages[0].extract_text.return_value = 'mocked text 1'
        mock_pdf_reader.pages[1].extract_text.return_value = 'mocked text 2'
        mock_reader.return_value = mock_pdf_reader

        # Call the function with a mock pdf_path
        pdf_processing.pdf_to_text('mock_pdf_path', 'mock_txt_path', 'mocked preamble')

        # Check that the file was opened correctly
        mock_file.assert_any_call('mock_pdf_path', 'rb')
        mock_file.assert_any_call('mock_txt_path', 'w')

        # Check that PdfReader was called with the correct argument
        mock_reader.assert_called_once_with(mock_file.return_value.__enter__.return_value)

        # Check that extract_text was called
        mock_pdf_reader.pages[0].extract_text.assert_called_once()
        mock_pdf_reader.pages[1].extract_text.assert_called_once()

        # Check that write was called with the correct arguments
        mock_file.return_value.write.assert_any_call('mocked preamble')
        mock_file.return_value.write.assert_any_call('mocked text 1mocked text 2')

if __name__ == '__main__':
    unittest.main()

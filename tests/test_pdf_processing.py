# test_pdf_processing.py

import unittest
from unittest.mock import Mock, patch, mock_open
from PyPDF2 import PdfFileReader

import pdf_processing

class TestPdfProcessing(unittest.TestCase):
    @patch('pdf_processing.PdfFileReader')
    @patch('builtins.open', new_callable=mock_open, read_data=b"mocked data")
    def test_pdf_to_text(self, mock_file, mock_reader):
        # Set up mock objects
        mock_pdf_reader = Mock()
        mock_pdf_reader.extract_text.return_value = 'mocked text'
        mock_reader.return_value = mock_pdf_reader

        # Call the function with a mock pdf_path
        result = pdf_processing.pdf_to_text('mock_pdf_path')

        # Check that the file was opened correctly
        mock_file.assert_called_once_with('mock_pdf_path', 'rb')

        # Check that PdfFileReader was called with the correct argument
        mock_reader.assert_called_once_with(mock_file.return_value.__enter__.return_value)

        # Check that extract_text was called and the returned text is correct
        mock_pdf_reader.extract_text.assert_called_once()
        self.assertEqual(result, 'mocked text')

if __name__ == '__main__':
    unittest.main()

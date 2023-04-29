# test_folder_checker.py

import os
import unittest
import tempfile

from folder_checker import check_folder

class TestFolderChecker(unittest.TestCase):
    def test_check_folder(self):
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Call the function
            check_folder(temp_dir)

            # Check that the folder exists
            self.assertTrue(os.path.exists(temp_dir))

if __name__ == '__main__':
    unittest.main()

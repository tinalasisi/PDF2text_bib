import unittest
import os
import tempfile
import shutil

import bibtex_processing

class TestbibtexProcessing(unittest.TestCase):
    def setUp(self):
        # Create temporary directory
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        # Delete temporary directory and its contents
        self.temp_dir.cleanup()
        
        # Delete filenames.txt file if exists
        if os.path.exists(os.path.join('workspace/bibtex', 'filenames.txt')):
            os.remove(os.path.join('workspace/bibtex', 'filenames.txt'))

    def test_process_bibtex(self):
        # Create temporary bibtex file in temporary directory
        temp_bibtex_file = os.path.join(self.temp_dir.name, "test.bib")
        with open(temp_bibtex_file, 'w') as f:
            f.write("@article{key1,\n")
            f.write("    author={Author1 and Author2},\n")
            f.write("    title={Title1},\n")
            f.write("    journal={Journal1},\n")
            f.write("    year={2022},\n")
            f.write("}\n")
            f.write("@article{key2,\n")
            f.write("    author={Author3 and Author4 and Author5},\n")
            f.write("    title={Title2},\n")
            f.write("    journal={Journal2},\n")
            f.write("    year={2021},\n")
            f.write("}\n")
            f.write("@article{key3,\n")
            f.write("    author={Author6},\n")
            f.write("    title={Title3},\n")
            f.write("    journal={Journal3},\n")
            f.write("    year={2020},\n")
            f.write("}\n")

         # Run process_bibtex function on temporary bibtex file with mode 1
        filenames, entries = bibtex_processing.process_bibtex(temp_bibtex_file, mode=1)
        # Check that filenames.txt file was created and has the correct contents for mode 1
        expected_filenames_mode1 = ["Author1-and-Author2_2022_Title1.pdf", 
                                     "Author3-et-al_2021_Title2.pdf",
                                     "Author6_2020_Title3.pdf"]
        with open(os.path.join('workspace/bibtex', 'filenames.txt'), 'r') as f:
            lines = f.read().splitlines()
            self.assertListEqual(lines, expected_filenames_mode1, 
                                 "The output filenames did not match the expected filenames for mode 1.")
        
        # Assert that filenames and entries are correctly returned
        self.assertListEqual(filenames, expected_filenames_mode1, "Returned filenames did not match expected filenames.")
        self.assertIsInstance(entries, list, "Entries is not a list.")
        self.assertEqual(len(entries), 3, "Number of entries is not correct.")

        # Run process_bibtex function on temporary bibtex file with mode 2
        filenames, entries = bibtex_processing.process_bibtex(temp_bibtex_file, mode=2)
        # Check that filenames.txt file was created and has the correct contents for mode 2
        expected_filenames_mode2 = ["Author1-and-Author2_Journal1_2022_Title1.pdf", 
                                     "Author3-et-al_Journal2_2021_Title2.pdf",
                                     "Author6_Journal3_2020_Title3.pdf"]
        with open(os.path.join('workspace/bibtex', 'filenames.txt'), 'r') as f:
            lines = f.read().splitlines()
            self.assertListEqual(lines, expected_filenames_mode2, 
                                 "The output filenames did not match the expected filenames for mode 2.")
        
        # Assert that filenames and entries are correctly returned
        self.assertListEqual(filenames, expected_filenames_mode2, "Returned filenames did not match expected filenames.")
        self.assertIsInstance(entries, list, "Entries is not a list.")
        self.assertEqual(len(entries), 3, "Number of entries is not correct.")
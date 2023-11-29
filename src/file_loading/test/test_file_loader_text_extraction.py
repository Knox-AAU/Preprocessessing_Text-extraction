"""
Module providing functionality needed to run integration tests.
"""

import unittest
from file_loading.file_loader import FileLoader
from text_extraction.text_extractor import TextExtractor

class TestFileLoaderTextExtraction(unittest.TestCase):
    """
    Integration test between file_loader and text_extraction.
    """
    def setUp(self):
        self.pdf_file_path = "src/file_loading/test/PDF_test1.pdf"

    def test_file_loader_and_text_extractor_integration(self):
        """
        This method verifies that the FileLoader correctly loads an image file,
        and the TextExtractor extracts text from the specified PDF file.
        """
        # Arrange
        file_loader = FileLoader()
        text_extractor = TextExtractor()

        # Act
        file_loader.readextension(self.pdf_file_path)
        file_loader.openpdf()
        print(file_loader.images[0].file_name)
        text_extractor.read(self.pdf_file_path)

        # Assert
        # Verify that loaded image file is created by FileLoader
        self.assertTrue(file_loader.last_load_status)
        self.assertEqual(len(file_loader.images), 1)
        self.assertEqual(file_loader.images[0].file_name, "PDF_test1.pdf")
        self.assertEqual(file_loader.images[0].format, "PPM")

        # Verify that the text is extracted by TextExtractor
        output_file_path = text_extractor.out_dir + "PDF_test1.pdf"
        with open(output_file_path, "r", encoding="utf-8") as output_file:
            content = output_file.read()
            content = content.strip('\n')
            self.assertIn("word", content)

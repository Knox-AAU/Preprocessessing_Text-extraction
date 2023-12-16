""" 
Module providing functionaly needed to run integration test. 
"""

import unittest
import os
import shutil
from file_loading.file_loader import FileLoader
from text_extraction.text_extractor import TextExtractor
from text_extraction.metadata_handler.metadata_handler import MetadataHandler


class TestFileLoaderTextExtraction(unittest.TestCase):
    """
    Integration test between file_loader and text_extraction.
    """
    def setUp(self):
        source = "src/file_loading/test/test_files/PDF_test1.pdf"
        destination = "src/file_loading/test/PDF_test1.pdf"

        try:
            shutil.copy(source, destination)
            print("File copied successfully.")
        except shutil.SameFileError:
            print("Source and destination represents the same file.")
        except PermissionError:
            print("Permission denied.")

        self.pdf_file_path = "src/file_loading/test/PDF_test1.pdf"
        self.output_folder_file_loader = "/watched/text_extraction/" + "out_0_PDF_test1.png"

    def tearDown(self):
        if os.path.exists(self.pdf_file_path):
            os.remove(self.pdf_file_path)

    def test_file_loader_and_text_extractor_integration(self):
        """
        This method verifies that the FileLoader correctly loads an image file,
        and the TextExtractor extracts text from the specified PDF file.
        """
        # Arrange
        metadata_handler = MetadataHandler(api_url="http://knox-proxy01.srv.aau.dk/metadata-api")
        file_loader = FileLoader()
        file_loader.output_folder = "/watched/text_extraction/"
        text_extractor = TextExtractor(metadata_handler=metadata_handler)
        text_extractor.out_dir = "/watched/spell_checking/"

        # Act
        if os.path.exists("src/file_loading/test/PDF_test1.pdf"):
            file_loader.handle_files(self.pdf_file_path)

        # Assert
        # Verify that loaded image file is created by FileLoader
        self.assertTrue(os.path.exists("/watched/spell_checking/out_0_PDF_test1.txt"))

        # Verify that the text is extracted by TextExtractor
        output_file_path = text_extractor.out_dir + "out_0_PDF_test1.txt"
        with open(output_file_path, "r", encoding="utf-8") as output_file:
            content = output_file.read()
            print(content)

        self.assertIn("word", content)
                        
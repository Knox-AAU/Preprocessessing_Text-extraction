import unittest
from file_loading.file_loader import FileLoader
from text_extraction.text_extractor import TextExtractor


class Test_File_Loader_Text_Extraction_copy(unittest.TestCase):
    def setUp(self):
        self.pdf_file_path = "src/file_loading/test/PDF_test1.pdf"

    def test_file_loader_and_text_extractor_integration(self):
        # Arrange
        file_loader = FileLoader()
        text_extractor = TextExtractor()

        # Act
        file_loader.readextension(self.pdf_file_path)
        file_loader.openpdf()
        print(file_loader.images[0].file_name)
        text_extractor.read(file_loader.images[0].file_name)

        # Assert
        # Verify that loaded image file is created by FileLoader
        self.assertTrue(file_loader.last_load_status)
        self.assertEqual(len(file_loader.images), 1)
        self.assertEqual(file_loader.images[0].file_name, "PDF_test1.pdf")
        self.assertEqual(file_loader.images[0].format, "PDF")

        # Verify that the text is extracted by TextExtractor
        output_file_path = text_extractor.out_dir / "_out_" / "PDF_test1.pdf"
        with open(output_file_path, "r", encoding="utf-8") as output_file:
            content = output_file.read()
            self.assertIn("Test", content)

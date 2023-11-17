import unittest
import tempfile
import os
from file_loading.file_loader import FileLoader
from text_extraction.text_extractor import TextExtractor

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.pdf_file = tempfile.NamedTemporaryFile(mode="w + b", delete=False)
        self.pdf_file.write(
            b"%PDF-1.3\n1 0 obj\n<< /Type /Catalog\n/Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages\n/Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page\n/MediaBox [0 0 612 792] /Parent 2 0 R /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 39 >>\nstream\nBT\n/F1 12 Tf\n100 100 Td\n(Test) Tj\nET\nendstream\nendobj\n5 0 obj\n<< /Type /Font\n/Subtype /Type1\n/BaseFont /Courier\n/Encoding /WinAnsiEncoding >>\nendobj\n6 0 obj\n<< /Type /Font\n/Subtype /Type1\n/BaseFont /Courier-Bold\n/Encoding /WinAnsiEncoding >>\nendobj\n7 0 obj\n[ /PDF /Text ]\nendobj\nxref\n0 8\n0000000000 65535 f \n0000000010 00000 n \n0000000077 00000 n \n0000000175 00000 n \n0000000304 00000 n \n0000000409 00000 n \n0000000474 00000 n \n0000000557 00000 n \ntrailer\n<< /Size 8\n/Root 1 0 R\n\n\n\n/Info 5 0 R\n>>\nstartxref\n591\n%%EOF"
        )
        self.pdf_file.close()

    def test_file_loader_and_text_extractor_intergration(self):
        # Arrange
        file_loader = FileLoader()
        text_extractor = TextExtractor()

        # Act
        file_loader.readextension(self.pdf_file.name)
        file_loader.openpd()
        text_extractor.read(file_loader.images[0].file_name)

        # Assert
        # Vertify that loaded image file is created by FileLoader
        self.assertTrue(file_loader.last_load_status)
        self.assertEqual(len(file_loader.images), 1)
        self.assertEqual(
            file_loader.images[0].file_name, os.path.basename(self.pdf_file.name)
        )
        self.assertEqual(file_loader.images[0].format, "PDF")

        # Vertify that the text is extracted by TextExtractor
        self.assertTrue(text_extractor.out_dir.exists())
        output_file_path = (
            text_extractor.out_dir / "_out_" / os.path.basename(self.pdf_file.name)
        )
        with open(output_file_path, "r", encoding="utf-8") as output_file:
            content = output_file.read()
            self.assertIn("Test", content)


if __name__ == "__main__":
    unittest.main()

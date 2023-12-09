"""
Unit tests for the MetadataHandler class in text_extraction.metadata_handler module.
"""

import unittest
from io import StringIO
from text_extraction.metadata_handler import MetadataHandler

class TestMetadataHandler(unittest.TestCase):
    """
    Test suite for the MetadataHandler class.

    This class includes unit tests for the methods of the MetadataHandler class.
    """

    def setUp(self):
        """
        This method sets MetadataHandler up for dependencies.
        """
        # Arrange
        self.metadata_handler = MetadataHandler()

    def test_write_metadata(self):
        """
        Test the write_metadata method.
        """
        # Arrange
        file_mock = StringIO()
        metadata_dict = {
            "File Name": "example.txt",
            "Uploader": "user",
            "Index": 1,
            "Title": "Test Title"
        }

        expected_content = (
        "File Name: example.txt\n"
        "Uploader: user\n"
        "Index: 1\n"
        "Title: Test Title\n\n"
        )

        # Act
        self.metadata_handler.write_metadata(file_mock, metadata_dict)

        # Assert: Check if the actual output matches the expected output
        self.assertEqual(file_mock.getvalue(), expected_content)

    def test_write_sentence_metadata(self):
        """
        Test the write_file_metadata method.
        """
        # Arrange
        sentence_index = 1
        sentence = "This is a test sentence."
        expected_metadata = {"Sentence Index": 1, "Start Index": 0, "End Index": len(sentence)}

        # Act
        self.metadata_handler.write_sentence_metadata(sentence_index, sentence)

        # Assert
        self.assertEqual(self.metadata_handler.metadata, expected_metadata)

if __name__ == '__main__':
    unittest.main()
    
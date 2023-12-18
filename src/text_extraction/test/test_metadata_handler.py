"""
Unit tests for the MetadataHandler class in text_extraction.metadata_handler module.
"""

import unittest
from unittest.mock import patch
from text_extraction.metadata_handler.metadata_handler import MetadataHandler

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
        self.api_url = "http://knox-proxy01.srv.aau.dk/metadata-api"
        self.metadata_handler = MetadataHandler(api_url=self.api_url)

    @patch('requests.post')
    def test_write_metadata(self, mock_post):
        """
        Test the write_metadata method.
        """
        # Arrange
        api_url = "http://knox-proxy01.srv.aau.dk/metadata-api"
        metadata_handler = MetadataHandler(api_url=api_url)
        metadata_dict = {
            "File Name": "example.txt",
            "Uploader": "user",
            "Index": 1,
            "Title": "Test Title"
        }

        # Configure the mock response from requests.post
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "message": "mocked_uuid"}

        # Act
        metadata_handler.write_metadata(metadata_dict)

        # Assert:
        mock_post.assert_called_once_with(
            f"{api_url}/metadata",
            json={"metadata": metadata_dict},
            timeout=30
        )

        # Assert: Check if the actual output matches the expected output
        mock_post.assert_called_once_with(
            f"{self.api_url}/metadata",
            json={"metadata": metadata_dict},
            timeout=30
        )
        self.assertEqual(self.metadata_handler.metadata, {})

    def test_write_file_metadata(self):
        """Tests write_file_metadata method."""
        # Arrange
        input_file = "/path/to/example.txt"
        uploader = "user"
        index = 1

        # Act
        self.metadata_handler.write_file_metadata(input_file, uploader, index)

        # Assert
        expected_metadata = {
            "File Name": "example.txt",
            "Uploader": "user",
            "Index": 1,
        }
        self.assertEqual(self.metadata_handler.metadata, expected_metadata)

    def test_write_sentence_metadata(self):
        """Test the write_file_metadata method."""
        # Arrange
        sentence_index = 1
        sentence = "This is a test sentence."

        # Act
        self.metadata_handler.write_sentence_metadata(sentence_index, sentence)

        # Assert
        expected_metadata = {"Sentence Index": 1, "Start Index": 0, "End Index": len(sentence)}
        self.assertEqual(self.metadata_handler.metadata, expected_metadata)

    def test_reset_metadata(self):
        """Tests reset_metadata method."""
        # Arrange
        self.metadata_handler.metadata = {"key": "value", "other_key": "other_value"}

        # Act
        self.metadata_handler.reset_metadata()

        # Assert
        self.assertEqual(self.metadata_handler.metadata, {})
        self.assertEqual(self.metadata_handler.current_position, 0)

if __name__ == '__main__':
    unittest.main()
    
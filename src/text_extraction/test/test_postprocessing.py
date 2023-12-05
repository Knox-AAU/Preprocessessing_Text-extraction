"""Unittests for post processing"""
import unittest
from text_extraction.postprocessing import clean_word, clean_sentence

class PostProcessingTests(unittest.TestCase):
    """ Tests for the post processing module """
    def test_numbers_removed(self):
        """ Check if numbers are correctly removed """
        # Arrange
        to_test = "test1234"
        expected = "test"
        # Act
        actual = clean_word(to_test)
        # Assert
        self.assertEqual(expected, actual)


    def test_spaces_removed(self):
        """ Check if spaces are correctly removed """
        # Arrange
        to_test = "test     \n\n"
        expected = "test"
        # Act
        actual = clean_word(to_test)
        # Assert
        self.assertEqual(expected, actual)

    def test_invalid_characters_removed(self):
        """ Check if invalid characters are correctly removed """
        # Arrange
        to_test = "te.-,;st;"
        expected = "test;"
        # Act
        actual = clean_word(to_test)
        # Assert
        self.assertEqual(expected, actual)

    def test_clean_sentence(self):
        """ Test to check if a sentence is properly cleaned """
        # Arrange
        to_test = "this is a ; long se123ntence \n\n "
        expected = "this is a long sentence"

        # Act
        actual = clean_sentence(to_test)

        # Assert
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()

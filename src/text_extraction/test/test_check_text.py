"""provides unit test functionality"""
import unittest

def get_word_stream(path):
    """splits string read into individual words to compare the extracted words"""
    with open(path, encoding='utf8', mode='r') as file:
        words = file.read().split()
        return words

class TextExtractionTests(unittest.TestCase):
    """unit testing class"""

    def test_compare_text(self):
        #Arrange
        """perform ocr on the test image and extracts the words into an extracted.txt file"""
        #generate a txt file called extracted.txt from test.png here
        extracted_text = get_word_stream('extracted.txt')
        expected_text = get_word_stream('expected.txt')

        #Act
        result = extracted_text == expected_text

        #Assert
        self.assertTrue(result, 'the results is false thus the extracted is not correct')

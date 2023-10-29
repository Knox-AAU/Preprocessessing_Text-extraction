import unittest
from ocr import ocr_comp
"""does ocr on a constructed pdf where the text is known and has placed in expected.txt and during the test ocr will done on the pdf and contents will be compared to see if equal"""

def get_word_stream(path):
    """splits string read into individual words to compare the extracted words themselves"""
    with open(path, 'r') as file:
        words = file.read().split()
        return words

class TextExtractionTests(unittest.TestCase):

    def test_compare_text(self):
        #Arrange
        """perform ocr on the test image and extracts the words from file created and compare it to the test"""
        ocr_comp('test.png')
        extracted_text = get_word_stream('extracted.txt')
        expected_text = get_word_stream('expected.txt')
        

        #Act
        #read the indvidual words and run them through the spellchecker return the number of correct words
        result = extracted_text == expected_text

        #Assert
        self.assertTrue(result, 'the results is false thus the extracted is not correct')
        

if __name__ == "__main__":
    unittest.main()
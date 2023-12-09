"""provides unit test functionality"""
import unittest
import shutil
import os
from text_extraction.text_extractor import TextExtractor

def get_word_stream(path):
    """splits string read into individual words to compare the extracted words"""
    with open(path, encoding='utf8', mode='r') as file:
        words = file.read().lower().split()
        return words

class TextExtractionTests(unittest.TestCase):
    """unit testing class"""

    def test_compare_text(self):
        """perform ocr on the test image and extracts the words into an extracted.txt file"""

        #Arrange
        src = "src/text_extraction/test/test_files/test.png"
        dst = "src/text_extraction/test/extracted.png"
        text_extractor = TextExtractor()
        text_extractor.out_dir = "src/text_extraction/test/"
        #copies test file since text extractor deletes files once processed
        shutil.copy(src, dst)

        #Act
        text_extractor.read("src/text_extraction/test/extracted.png")
        #convert expected and extracted texts into lists
        extracted_text = get_word_stream("src/text_extraction/test/extracted.txt")
        expected_text = get_word_stream("src/text_extraction/test/test_files/expected.txt")
        #compares extracted text to the expected text to see if extraction was a success
        result = extracted_text == expected_text
        #deletes the testing file that was copied over
        if os.path.exists("src/text_extraction/test/extracted.png"):
            os.remove("src/text_extraction/test/extracted.png")

        #Assert
        self.assertTrue(result, 'the results is false thus the extracted text is not correct')

"""Module providing functionaly needed to run test"""
import unittest
import os
import pytesseract
from pdf2image import convert_from_path

def chars_to_string(chars):
    """function to convert a list of chars to a string"""
    string = ' '.join(chars)
    return string

def log_results(passed_chars, declined_chars, text):
    """function that creates a log in text file of the test results"""
    with open("src/text_extraction/test/edge_cases_log.txt", 'w', encoding="utf-8") as log:
        lines =["passed characters: " + chars_to_string(passed_chars) + "\n",
                "declined characters: " + chars_to_string(declined_chars) + "\n",
                f"passed:{len(passed_chars)}" + "|" + f"declined: {len(declined_chars)}"+"\n",
                "the extracted text: \n", text]
        log.writelines(lines)

class EdgeCaseTests(unittest.TestCase):
    """Class containing the tests of edgecases for tesseract"""

    def test_edge_cases(self):
        """Method testing proficiency in extraction of different characters"""
        #Arrange
        text =""
        passed_chars = []
        declined_chars = []
        temp_path = "src/text_extraction/test/pdf_page_"
        ground_truth_path = "src/text_extraction/test/ground_truth.txt"
        #convert pdf to images and then perform ocr on those images
        pdf_images = convert_from_path('src/text_extraction/test/Testing_document.pdf')
        for image in enumerate(pdf_images):
            image[1].save(temp_path + f"{image[0]+1}.png", 'PNG')
            text = text + (pytesseract.image_to_string(temp_path + f"{image[0]+1}.png",lang="dan"))
            os.remove(f"src/text_extraction/test/pdf_page_{image[0]+1}.png")

        #separate words/characters from ground_truth into list
        with open(ground_truth_path, 'r', encoding="utf-8") as ground_truth:
            ground_truth = ground_truth.read().split()

        #Act
        #if length of text is more than 0 text was succesfully extracted
        status = len(text) > 0
        ground_truth_len = len(ground_truth)
        #iterate all elements in ground_truth and check if that substring is in the extracted text
        #then append found elements to passed_chars and the ones that weren't to declined_chars
        for char in range(ground_truth_len):
            match = text.find(ground_truth[char])
            if match > -1:
                passed_chars.append(ground_truth[char])
            else:
                declined_chars.append(ground_truth[char])

        chars_evaluated = (len(passed_chars) > 0 or len(declined_chars) > 0)
        log_results(passed_chars, declined_chars, text)

        #Assert
        self.assertTrue(status, "Nothing extracted")
        self.assertTrue(chars_evaluated, "characters have not been evaluated")
        
"""Module providing functionaly needed to run test"""
import unittest
from PIL import Image
import pytesseract

class Edge_Case_Tests(unittest.TestCase):
    """Class containing the integrationtest of edgecases"""

    def test_edge_cases(self):
        """Method testing edgscases of tesseract"""
        #Arrange
        text = pytesseract.image_to_string("src/text_extraction/test/Testing_document.jpg",lang="dan")

        #Act
        print(text)
        status = len(text) > 0

        #Assert
        self.assertTrue(status, "Nothing extracted")
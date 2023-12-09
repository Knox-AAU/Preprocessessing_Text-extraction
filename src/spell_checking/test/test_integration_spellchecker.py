"""Module providing functionaly needed to run integration test"""
import unittest
import os
import shutil
from spell_checking.spell_checker import SpellChecker
from text_extraction.text_extractor import TextExtractor

class SpellcheckerIntegrationTests(unittest.TestCase):
    """Class containing the integrationtest between textextractor and spellchecker"""

    def test_integration_spellchecker(self):
        """Method testing if the input of the textextractor cen be received by the spellchecker"""
        #Arrange
        text_extractor = TextExtractor()
        text_extractor.out_dir = "/watched/spell_checking/"
        spellchecker = SpellChecker("src/spell_checking/wordList.txt")
        spellchecker.out_dir = "/watched/output"
        with open("src/spell_checking/test/test_files/expected.txt", 'r', encoding="utf-8") as expected_text:
            expected_text = expected_text.read().lower().split()
            print(f'Expected text: {expected_text}')
        shutil.copy("src/spell_checking/test/test_files/Test_File.jpg", "src/spell_checking/test/Test_File.jpg")

        #Act
        if not os.path.exists("/watched/output/Test_File.txt"):
            text_extractor.read("src/spell_checking/test/Test_File.jpg")
            spellchecker.handle_files("/watched/spell_checking/Test_File.txt")
        with open("/watched/output/Test_File.txt", 'r', encoding="utf-8") as output:
            output = output.read().lower().split()
            print(f'Spellchecked text: {output}')
            status = bool(output == expected_text)
        if os.path.exists("src/spell_checking/test/Test_File.jpg"):
            os.remove("src/spell_checking/test/Test_File.jpg")

        #Assert
        self.assertTrue(status, "The text was not extracted correctly")
        
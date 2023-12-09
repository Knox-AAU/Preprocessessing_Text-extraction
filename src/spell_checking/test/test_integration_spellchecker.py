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
        src = "src/spell_checking/test/test_files/Test_File.jpg"
        dst = "src/spell_checking/test/Test_File.jpg"
        ground_truth = "src/spell_checking/test/test_files/expected.txt"
        text_extractor = TextExtractor()
        text_extractor.out_dir = "/watched/spell_checking/"
        spellchecker = SpellChecker("src/spell_checking/wordList.txt")
        spellchecker.out_dir = "/watched/output"
        #register expected.txt as a list
        with open(ground_truth, 'r', encoding="utf-8") as expected_text:
            expected_text = expected_text.read().lower().split()
            print(f'Expected text: {expected_text}')
        #copies test file since text extractor deletes files once processed
        shutil.copy(src, dst)

        #Act
        #if a txt file has already been processed do not run extraction again
        if not os.path.exists("/watched/output/Test_File.txt"):
            text_extractor.read("src/spell_checking/test/Test_File.jpg")
            spellchecker.handle_files("/watched/spell_checking/Test_File.txt")
        with open("/watched/output/Test_File.txt", 'r', encoding="utf-8") as output:
            output = output.read().lower().split()
            print(f'Spellchecked text: {output}')
            status = bool(output == expected_text)
        #deletes the testing file that was copied over
        if os.path.exists("src/spell_checking/test/Test_File.jpg"):
            os.remove("src/spell_checking/test/Test_File.jpg")

        #Assert
        self.assertTrue(status, "The text was not extracted correctly")
        
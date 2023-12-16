"""Module providing functionaly needed to run integration test"""
import unittest
import os
import responses
from spell_checking.spell_checker import SpellChecker
from text_extraction.text_extractor import TextExtractor

class SpellcheckerIntegrationTests(unittest.TestCase):
    """Class containing the integrationtest between textextractor and spellchecker"""

    @responses.activate
    def test_integration_spellchecker(self):
        """Method testing if the input of the textextractor can be received by the spellchecker"""
        #Arrange
        text_extractor = TextExtractor()
        text_extractor.out_dir = "/watched/spell_checking/"
        spellchecker = SpellChecker("src/spell_checking/wordList.txt")
        spellchecker.out_dir = "/watched/output"
        with open("src/spell_checking/test/expected.txt", 'r', encoding="utf-8") as expected_text:
            expected_text = expected_text.read().lower().split()
            print(f'Expected text: {expected_text}')

        #Act
        if not os.path.exists("/watched/output/Test_File.txt"):
            text_extractor.read("src/spell_checking/test/Test_File.jpg")
            spellchecker.handle_files("/watched/spell_checking/Test_File.txt")
        with open("/watched/output/Test_File.txt", 'r', encoding="utf-8") as output:
            output = output.read().lower().split()
            print(f'Spellchecked text: {output}')
            status = bool(output == expected_text)

        exclude_words = ["file", "name:", "none", "uploader:", "none", "index:", "none", "title:"]

        # Extract relevant text for comparison
        relevant_output = [word for word in output if word not in exclude_words]
        relevant_expected = [word for word in expected_text if word not in exclude_words]

        # Assert
        status = all(word in relevant_output for word in relevant_expected)
        self.assertTrue(
            status,
            "The expected words are not present in the extracted text"
        )

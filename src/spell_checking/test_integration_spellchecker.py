"""Module providing functionaly needed to run integration test"""
import unittest
from spell_checking.spell_checker import SpellChecker
from text_extraction.text_extractor import TextExtractor

class SpellcheckerIntegrationTests(unittest.TestCase):
    """Class containing the integrationtest between textextractor and spellchecker"""

    def test_integration_spellchecker(self):
        """Method testing if the input of the textextractor cen be received by the spellchecker"""
        #Arrange
        spellchecker = SpellChecker("src/spell_checking/wordList.txt")
        text_extractor = TextExtractor()
        expected_text = []
        with open("src/spell_checking/expected.txt", 'r', encoding="utf-8") as temp_text:
            temp_text = temp_text.read().split()
            for word in temp_text:
                word = word.lower()
                word = word.strip()
                expected_text.append(word)
            print(f'Expected text: {expected_text}')

        #Act
        text_extractor.read("src/spell_checking/Test_File.pdf")
        spellchecker.handle_files("/watched/spell_checking/Test_File.pdf")
        with open("/watched/output/Test_File.pdf", 'r', encoding="utf-8") as output:
            output = output.read().split('\n')
            spellchecked_file = list(filter(lambda word: word != "", output))
            print(f'Spellchecked text: {spellchecked_file}')
            status = bool(spellchecked_file == expected_text)

        #Assert
        self.assertTrue(status, "The text was not extracted correctly")
        
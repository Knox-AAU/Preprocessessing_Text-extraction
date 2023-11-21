import unittest
from spell_checking.spell_checker import SpellChecker
from text_extraction.text_extractor import TextExtractor

class SpellcheckerIntegrationTests(unittest.TestCase):

    def test_integration_spellchecker(self):
        #Arrange
        spellchecker = SpellChecker("src/spell_checking/wordList.txt")
        text_extractor = TextExtractor()
        with open("src/spell_checking/expected.txt", 'r', encoding="utf-8") as expected_text:
            expected_text = expected_text.read().split()
            for word in expected_text:
                word = word.strip
            print(f'Expected text: {expected_text}')

        #Act
        text_extractor.read("src/spell_checking/Test_of_TextExtraction.pdf")
        spellchecker.handle_files("src/spell_checking/Test_of_TextExtraction.pdf")
        with open("watched/output/Test_of_TextExtraction", 'r', encoding="utf-8") as spellchecked_file:
            spellchecked_file = spellchecked_file.read().split('\n')
            print(f'Spellchecked text: {spellchecked_file}')
            if(spellchecked_file == expected_text):
                incorrect = False
            else:
                incorrect = True
       
        #Assert
        self.assertTrue(incorrect)
        
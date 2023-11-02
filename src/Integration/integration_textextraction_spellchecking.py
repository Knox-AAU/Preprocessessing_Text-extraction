""" idk """
import unittest
from Spellchecking.spell_checker import SpellChecker
from TextExtraction.text_extractor import TextExtractor
from Queue.queue import Queue

class FileLoaderToSpellcheckerTest(unittest.TestCase):
    """ idk """
    def test_name_this(self):
        """ Snut """
        # Arrange
        q = Queue()
        spell_checker = SpellChecker("src/Spellchecking/wordList.txt")
        text_extractor = TextExtractor("src/Integration/textextraction_testinput.pdf", q)

        # Act
        text_extractor.start_extraction()
        print("Starting queue")
        spell_checker.consume_queue(q)
        print("Started queue")

        text_extractor.end_extraction()
        print("Ending consumation")
        spell_checker.end_consumation()
        print("Ended consumation")
        # Assert
        expected = "8 valid words and 0 invalid words"
        actual = f"""{spell_checker.valid_words} valid words and {spell_checker.invalid_words} invalid words"""

        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()

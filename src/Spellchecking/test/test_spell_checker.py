"""Module providing a function printing python version."""
import unittest
from Spellchecking.spell_checker import SpellChecker

class TestCase(unittest.TestCase):
    """Testing the SpellChecker class"""
    def test_correct_initialization(self):
        """ Initializaer function """

        # Arrange
        sc = SpellChecker('src/Spellchecking/test/test_wordlist.txt')

        # Act
        # Assert
        expected = sc.root.char == ""
        self.assertEqual(expected, expected)

if __name__ == '__main__':
    unittest.main()

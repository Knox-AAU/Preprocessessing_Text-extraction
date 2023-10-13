"""Module providing a function printing python version."""
import unittest
from Spellchecking.src.spell_checker import SpellChecker

class TestCase(unittest.TestCase):
    """Testing the SpellChecker class"""
    def test_correctInitialization(self):
        """ Initializaer function """

        # Arrange
        sc = SpellChecker('wordList.txt')

        # Act
        # Assert
        expected = sc.root.char == ""
        self.assertEqual(expected, expected)
        
    def test_addingWord(self):
        """  """

if __name__ == '__main__':
    unittest.main()

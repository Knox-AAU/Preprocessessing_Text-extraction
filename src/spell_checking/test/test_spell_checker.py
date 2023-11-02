"""Module providing a function printing python version."""
import unittest
from spell_checking.spell_checker import SpellChecker

class TestCase(unittest.TestCase):
    """Testing the SpellChecker class"""
    def test_trie_initializes(self):
        """ Test if the Trie is correctly initialized """
        # Arrange
        sc = SpellChecker()

        # Act
        # Assert
        actual = sc.root.char == ""
        self.assertEqual(actual, True)


    def test_trie_inserts_correctly(self):
        """ Test if the insert function works """
        # Arrange
        sc = SpellChecker()
        # Act
        sc.insert('test')
        actual = sc.query('t')

        # Assert
        self.assertEqual(actual[0][0], 'test')


    def test_trie_query_correctly(self):
        """ Test if the query function works """
        # Arrange
        sc = SpellChecker()
        sc.insert('cat')
        sc.insert('death')
        sc.insert('deer')

        # Act
        actual = sc.query('d')

        # Assert
        self.assertEqual(actual[0][0], 'death')


if __name__ == '__main__':
    unittest.main()

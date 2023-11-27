"""Module providing a function printing python version."""
import unittest
import os
from ..file_loader import FileLoader

class TestCase(unittest.TestCase):
    """Testing the SpellChecker class"""


    # pylint: disable=W0511
    # TODO: This function needs some way to verify the expected values
    # TODO: Right now it just reads from printed output :))
    def test_opens_pdf(self):
        """ Test if the openpdf function correctly opens and reads data """

        # Arrange
        file_loader = FileLoader()
        file_loader.path = 'src/file_loading/test/test.pdf'
        file_loader.output_folder = 'src/file_loading/test/'
        # Act
        file_loader.openpdf()
        file_found = False

        if os.path.exists('src/file_loading/test/out_0_test.png'):
            file_found = True

        #Assert
        self.assertTrue(file_found)

if __name__ == '__main__':
    unittest.main()

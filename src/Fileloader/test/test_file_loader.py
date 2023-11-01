"""Module providing a function printing python version."""
import unittest

from ..file_loader import FileLoader


class TestCase(unittest.TestCase):
    """Testing the SpellChecker class"""
    def test_reads_correct_path(self):
        """ Test if the readextension function reads the correct path """
        # Arrange
        file_loader = FileLoader()
        file_loader.readextension('src/Fileloader/test/test.pdf')

        # Act
        actual_path = file_loader.path
        # Assert
        self.assertEqual(actual_path, 'src/Fileloader/test/test')


    def test_reads_correct_extension(self):
        """ Test if the readextension function reads the correct file extension """
        # Arrange
        file_loader = FileLoader()
        file_loader.readextension('src/Fileloader/test/test.pdf')

        # Act
        actual_extension = file_loader.extension
        # Assert
        self.assertEqual(actual_extension, '.pdf')


    # pylint: disable=W0511
    # TODO: This function needs some way to verify the expected values
    # TODO: Right now it just reads from printed output :))
    def test_opens_pdf(self):
        """ Test if the openpdf function correctly opens and reads data """
        # Arrange
        file_loader = FileLoader()
        file_loader.readextension('src/Fileloader/test/test.pdf')

        # Act
        file_loader.openpdf()

        actual = [
            file_loader.images[0].format,
            file_loader.images[0].size,
            file_loader.images[0].mode,
            file_loader.images[0].file_name,
        ]
        # Assert
        self.assertListEqual(actual, [
            'PPM',
            (1100, 1700),
            'RGB',
            'test.pdf'
        ])


    def test_opens_image(self):
        """ Test if the openimage function correctly opens and reads data """
        # Arrange
        file_loader = FileLoader()
        file_loader.readextension('src/Fileloader/test/test.jpg')

        # Act
        file_loader.openimage()
        actual = [
            file_loader.images[0].format,
            file_loader.images[0].size,
            file_loader.images[0].mode,
            file_loader.images[0].file_name,
        ]
        # Assert
        self.assertListEqual(actual, [
            'JPEG',
            (543, 360),
            'RGB',
            'test.jpg'
        ])

if __name__ == '__main__':
    unittest.main()

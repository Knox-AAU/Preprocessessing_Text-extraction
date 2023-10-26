"""Unittests for extension checker"""
import os
import unittest
from ..extension_checker import ExtChecker

class extcheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        testFile = open("test.txt", "a")
        testFile.write("Hello World!")
        testFile.close()

    def tearDown(self) -> None:
        os.remove("./test.txt")

    def test_wrong_file_ext(self) -> None:
        """Test for checking if file extension corresponding to actual file
        extension type where input is wrong extension to actual file"""

        # Arrange
        os.rename("./test.txt", "./test.pdf")

        # Act
        ExtChecker.check_file("./test.pdf")

        # Assert
        self.assertTrue(os.path.exists("./test.txt"))

    def test_correct_file_ext(self) -> None:
        """Test for checking if file extension corresponding to actual file
        extension type where input is correct extension to actual file"""
       
        # Arrange
        os.rename("./test.txt", "./test.pdf")

        # Act
        ExtChecker.check_file("./test.pdf")

        # Assert
        self.assertTrue(os.path.exists("./test.txt"))

    def test_no_file(self) -> None:
        """Test for checking if exception handling is correct"""

        # Assert
        self.assertRaises(ValueError, ExtChecker.check_file(None))

    def test_file_not_exists(self) -> None:
        """Test for checking if exception handling is correct when file doesn't exist"""

        # Assert
        self.assertRaises(FileNotFoundError, ExtChecker.check_file("./NoneExistingFile.ABC"))
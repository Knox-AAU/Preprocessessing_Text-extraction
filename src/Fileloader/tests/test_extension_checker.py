"""Unittests for extension checker"""
import os
import unittest
from ..extension_checker import ExtChecker

class ExtCheckerTests(unittest.TestCase):
    """Unittesting of extension_checker"""
    def setUp(self) -> None:
        with open("test.txt", "a", encoding="utf-8") as test_file:
            test_file.write("Hello World!")
        test_file.close()

        self.file = "./test.txt"
        self.checker = ExtChecker(self.file)

    # def tearDown(self) -> None:
    #     os.remove("./test.txt")

    def test_wrong_file_ext(self) -> None:
        """Test for checking if file extension corresponding to actual file
        extension type where input is wrong extension to actual file"""

        # Arrange
        wrong_ext_checker = ExtChecker("./test.pdf")
        os.rename("./test.txt", "./test.pdf")

        # Act
        wrong_ext_checker.check_file()

        # Assert
        self.assertTrue(os.path.exists("./test.txt"))

        os.remove("./test.pdf")

    def test_correct_file_ext(self) -> None:
        """Test for checking if file extension corresponding to actual file
        extension type where input is correct extension to actual file"""

        # Arrange
        # os.rename("./test.txt", "./test.pdf")

        # Act
        self.checker.check_file()

        # Assert
        self.assertTrue(os.path.exists("./test.txt"))

    def test_no_file(self) -> None:
        """Test for checking if exception handling is correct"""
        
        # Arrange
        no_file_test = ExtChecker()

        # Assert
        with self.assertRaises(ValueError):
            no_file_test.check_file()

    def test_file_not_exists(self) -> None:
        """Test for checking if exception handling is correct when file doesn't exist"""

        # Arrange
        no_file_found_test = ExtChecker("./NoneExistingFile.ABC")

        # Assert
        with self.assertRaises(FileNotFoundError):
            no_file_found_test.check_file()

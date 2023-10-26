"""Unittests for extension checker"""
import os
import unittest
from ..extension_checker import ExtChecker

class extcheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        testFile = open("test.txt", "a")
        testFile.write("Hello World!")
        testFile.close()

    def test_wrong_file_ext(self) -> None:
        """Test for checking if file extension corresponding to actual file
        extension type where input is wrong extension to actual file"""

        # Arrange
        print(ExtChecker.check_file("test.txt"))

        # Act

        # Assert


    def test_correct_file_ext(self) -> None:
        """Test for checking if file extension corresponding to actual file
        extension type where input is correct extension to actual file"""
       
        # Arrange
        
        # Act

        #Assert

    def test_convert_file_ext(self) -> None:
        """Test for wrong extension is inputtet"""
      
        # Arrange
        
        # Act

        #Assert

    def test_convert_correct_file_ext(self) -> None:
        """Test for wrong extension is inputtet"""
     
        # Arrange
        
        # Act

        #Assert
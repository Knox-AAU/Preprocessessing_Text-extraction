import os
import unittest

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), "readme.md")


class MyTest(unittest.TestCase):
    def setUp(self):
        self.testfile = open(TESTDATA_FILENAME).read()
        self.testdata = self.testfile.read()

    def tearDown(self):
        self.testfile.close()

from typing_extensions import TYPE_CHECKING
import unittest
from main import extract_title

class Test_Extract_Title(unittest.TestCase):
    def test_extract_title_simple(self):
        self.assertEqual(extract_title("# Title"), "Title")

    def test_extract_title_header_second_line(self):
        test_markdown = """
Testing this thing
# Test Header
But there is more text here!
"""

        self.assertEqual(extract_title(test_markdown), "Test Header")

    def test_extract_title_hash_on_end(self):
        test_markdown = """
Testing this thing
# Test Header
But there is more text here!
And even # here!
"""

        self.assertEqual(extract_title(test_markdown), "Test Header")

if __name__ == "__main__":
    unittest.main()

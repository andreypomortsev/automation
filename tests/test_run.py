import unittest
from unittest.mock import patch, Mock
import io
import sys
from source.run import read_txt

class TestUpload(unittest.TestCase):
    def setUp(self):
        self.txt_file = "example.txt"

    def test_read_txt(self):
        with patch('builtins.open', create=True) as mock_open:
            mock_text = "Apple\n200 lbs\nA juicy red apple"
            mock_open.return_value.__enter__.return_value.read.return_value = mock_text
            expected_output = "name: Apple\nweight: 200 lbs"
            output = read_txt(self.txt_file, False)
            self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, mock_open
from source.run import read_txt

class TestUpload(unittest.TestCase):
    def setUp(self):
        self.txt_file = "example.txt"

    def test_read_txt(self):
        mock_text = "Apple\n200 lbs\nA juicy red apple"
        with patch('builtins.open', mock_open(read_data=mock_text)) as mock_file:
            mock_file.return_value.__enter__.return_value.read.return_value = mock_text
            expected_output = "name: Apple\nweight: 200 lbs"
            output = read_txt(self.txt_file, False)
            self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()

""" Test module for `source/run.py script
"""

import os
import unittest
from unittest.mock import patch
from source.run import read_txt, POST_PATH


class TestUpload(unittest.TestCase):
    """ Test source/run.py script on reading files and sending its contents by `requests.post()`
    """
    def setUp(self):
        """
        Sets up the test case by creating a temporary text file with test data.

        The temporary file contains information about a fruit, including its name,
        weight, and description, and is used to test the file upload functionality of
        the application.

        Args:
            self (unittest.TestCase): The current test case object.

        Returns:
            None.
        """
        self.txt_file = "example.txt"
        self.mock_text = "Apple\n3 lbs\nA delicious fruit\n"
        # Create a temporary text file with test data
        with open(self.txt_file, "w", encoding="UTF-8") as mock_file:
            mock_file.write(self.mock_text)

    def test_read_txt(self):
        """
        Tests the behavior of the `read_txt()` function when called with a mock text file.

        This test uses the temporarely file self.txt_file with test data, 
        and then calls `read_txt()` with this file and the `send` flag set to False.
        The test asserts that the output string matches the expected output string.

        Args:
            self (unittest.TestCase): The current test case object.

        Returns:
            None.
        """
        expected_output = "name: Apple\nweight: 3 lbs"
        output = read_txt(self.txt_file, False)
        self.assertEqual(output, expected_output)

    @patch("source.run.requests.post")
    def test_read_txt_send(self, mock_post):
        """
        Tests the functionality of the read_txt function with the flag `send` set to True.

        This test uses the `unittest.mock.patch` decorator to patch the `requests.post` method
        with a mock object, and calls the `read_txt` function with a temporary file and 
        the send flag set to True. The expected output is compared with the output of the function,
        and the `assert_called_with` method of the mock object is used to verify that 
        `requests.post` method was called with the expected arguments.

        Args:
            self (unittest.TestCase): The current test case object.

        Returns:
            None.
        """
        # Call the function with the temporary file and send flag set to True
        output_str = read_txt(self.txt_file, send=True)
        # Check that the expected string is returned
        self.assertEqual(output_str, "name: Apple\nweight: 3 lbs")
        # Check that requests.post() was called with the expected arguments
        mock_post.assert_called_with(
            POST_PATH,
            json={
                "name": "Apple",
                "weight": 3,
                "description": "A delicious fruit",
                "image_name": self.txt_file,
            },
            timeout=2,
        )

    def tearDown(self) -> None:
        os.remove(self.txt_file)
        return super().tearDown()

if __name__ == "__main__":
    unittest.main()

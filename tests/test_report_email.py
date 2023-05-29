import unittest
from unittest.mock import patch, MagicMock
import os
from source import reports
from source import report_email

class TestMain(unittest.TestCase):
    def test_main(self):
        # Set up mock environment variables
        os.environ["USER"] = "testuser"
        mock_glob = MagicMock(return_value=["file1.txt", "file2.txt"])
        with patch("source.report_email.glob.glob", mock_glob):
            # Call main() function
            report_email.main()
            # Assert that reports.generate_report and emails.send were called with the expected arguments
            reports.generate_report.assert_called_once_with("/tmp/processed.pdf", "Sales summary for last month", "summary1<br/>summary2")
            emails.send.assert_called_once()

if __name__ == '__main__':
    unittest.main()

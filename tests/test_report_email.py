import unittest
import os
import shutil
from source import emails, reports, run
from source import report_email, full_path


class TestMain(unittest.TestCase):
    """Test source/report_emails.py
    """
    def setUp(self) -> None:
        """Create folders from `full_path`, and txt files
        to check the modulde. 
        """
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        self.files = ("1.txt", "2.txt", "3.txt")
        self.lines = []
        for number, file in enumerate(self.files):
            with open(file, "w", encoding="UTF-8") as mock_file:
                line = f"{number}Apple\n{number}00 lbs\nSuch a tasty {number} Apple\n"
                self.lines.append(line)
                mock_file.write(line)

    def tearDown(self) -> None:
        """Tear down all the folders and files from full_path
        by deleting the folder, which is one folder up from the `full_path` 
        """
        os.chdir(full_path)
        os.path.dirname(full_path)
        shutil.rmtree(os.getcwd())

    def test_main(self) -> None:
        """Check if the report_emails.py call the needed functions with
        the right params, which a variable `summary` hold.
        """
        report_email.main()
        # Assert that reports.generate_report and emails.send
        # were called with the expected arguments
        summary = [run.read_txt(line) for line in self.lines]
        reports.generate_report.assert_called_once_with(
            "/tmp/processed.pdf",
            "Upload Completed - Online Fruit Store",
            "<br/>".join(summary),
        )
        emails.send.assert_called_once()


if __name__ == "__main__":
    unittest.main()

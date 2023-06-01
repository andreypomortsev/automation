import os
from os.path import isdir, isfile
import pathlib as pl
import shutil
import unittest
from unittest import mock
from source import reports, report_email


class PathTests:
    """
    This mixin provides a set of assertion methods to test
    whether a given path is a folder or a file.
    """

    def assertIsFolder(self, path, msg="Not a folder"):
        """
        Asserts that the given path exists and is a folder.

        Args:
            path (str): The path to check.
            msg (str, optional): The error message to display if the assertion fails.
        """
        return self.assertTrue(isdir(path), msg)

    def assertIsFile(self, path, msg="Not a file"):
        """
        Asserts that the given path exists and is a file.

        Args:
            path (str): The path to check.
            msg (str, optional): The error message to display if the assertion fails.
        """
        return self.assertTrue(isfile(path), msg)


class TestReportEmail(unittest.TestCase, PathTests):
    """Test source/report_emails.py"""

    def setUp(self) -> None:
        """Create folders from `full_path`, and txt files
        to check the modulde.
        """
        if not os.path.exists(report_email.full_path):
            os.makedirs(report_email.full_path)
        self.files = ("1.txt", "2.txt", "3.txt")
        self.lines, self.summary = [], []
        for number, file in enumerate(self.files, start=1):
            txt_path = os.path.join(report_email.full_path, file)
            with open(txt_path, "w", encoding="UTF-8") as mock_file:
                line = f"{number}Apple\n{number}00 lbs\nSuch a tasty {number} Apple\n"
                self.summary.append(f"name: {number}Apple\nweight: {number}00 lbs")
                self.lines.append(line)
                mock_file.write(line)

    def tearDown(self) -> None:
        """Tear down all the folders and files from full_path
        by deleting the folder, which is one folder up from the `full_path`
        """
        os.chdir(report_email.full_path)
        os.path.dirname(report_email.full_path)
        shutil.rmtree(os.getcwd())

    def test_txt_files(self) -> None:
        """Test if the files exists"""
        for file in self.files:
            path = pl.Path(os.path.join(report_email.full_path, file))
            self.assertIsFile(path)

    def test_full_path(self) -> None:
        """Test if the full_path exists"""
        path = pl.Path(report_email.full_path)
        self.assertIsFolder(path)

    def test_make_message(self) -> None:
        """Check if the report_emails.py call the needed functions with
        the right params, which a variable `summary` hold.
        """
        # Test if the report_email.make_message was called
        report_email_make_message = mock.create_autospec(report_email.make_message)
        report_email_make_message()
        report_email_make_message.assert_called_once()

        # Assert that reports.generate_report
        # was called with the expected arguments
        reports_generate_reports = mock.create_autospec(reports.generate_report)
        args = (
            "/tmp/processed.pdf",
            "Upload Completed - Online Fruit Store",
            "<br/>".join(self.summary),
        )
        reports_generate_reports(*args)
        reports_generate_reports.assert_called_once_with(*args)


if __name__ == "__main__":
    unittest.main()

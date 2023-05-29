#!/usr/bin/env python3

"""
A module to generate PDF reports using the ReportLab library.

The module includes a `generate_report` function that takes in a file path to save 
as the PDF report, a title string and a paragraph string as the content. 
The function uses ReportLab's SimpleDocTemplate, Paragraph, Spacer and 
getSampleStyleSheet classes to create and format the PDF report with the given data.

Functions:
----------
    generate_report(attachment: str, title: str, paragraph: str) -> None:
        Generates a PDF report using the given data.

        Args:
            attachment (str): The file path of the PDF report to generate.
            title (str): The title of the report.
            paragraph (str): The body text of the report.

        Returns:
            None

Author: Andrey Pomortsev
"""

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(attachment: str, title: str, paragraph: str) -> None:
    """
    Generates a PDF report using the given data.

    Args:
        attachment (str): The file path of the PDF report to generate.
        title (str): The title of the report.
        paragraph (str): The body text of the report.

    Returns:
        None
    """
    styles = getSampleStyleSheet()
    report = SimpleDocTemplate(attachment)
    report_title = Paragraph(title, styles["h1"])
    report_info = Paragraph(paragraph, styles["BodyText"])
    empty_line = Spacer(1, 20)
    report.build([report_title, empty_line, report_info, empty_line])

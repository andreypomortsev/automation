#!/usr/bin/env python3

"""
A module to generate an update summary report and send it via email.

The module includes a `main` function, which reads text files containing update descriptions
in a specific directory, generates a summary using Report's `generate_report` function,
attaches the resulting PDF report to an email message created using `generate` function
of the `emails` module, and sends the email using `send` function of the `emails` module.

Functions:
----------
    main() -> None:
        Generates an update summary PDF report and sends it via email.

        Reads text files containing update descriptions and generates a summary using Report's
        `generate_report` function. The resulting PDF report is attached to an email message
        created using `generate` function of the `emails` module. The email message is then sent
        using `send` function of the `emails` module.

        The details for the email sender is obtained from environment variable.

        Args:
            None

        Returns:
            
Author: Andrey Pomortsev
"""

import glob
import os
from source import reports
from source import run
from source import emails

PATH = "~/supplier-data/descriptions"
full_path = os.path.expanduser(PATH)

def main():
    """
    Generates an update summary PDF report and sends it via email.

    Reads text files containing update descriptions and generates a summary using Report's
    `generate_report` function. The resulting PDF report is attached to an email message
    created using `generate` function of the `emails` module. The email message is then sent
    using `send` function of the `emails` module.

    The details for the email sender is obtained from environment variable.

    Args:
        None

    Returns:
        None
    """

    descriptions = tuple(glob.glob(os.path.join(PATH, "*.txt")))

    # Report part
    summary = [run.read_txt(file, False) for file in descriptions]
    title = "Upload Completed - Online Fruit Store"
    attachement = "/tmp/processed.pdf"
    reports.generate_report(attachement, title, "<br/>".join(summary))

    # Email part
    sender = "automation@example.com"
    receiver = "{}@example.com".format(os.environ.get("USER"))
    subject = "Upload Completed - Online Fruit Store"
    body = "All fruits are uploaded to our website successfully. \
	A detailed list is attached to this email."
    message = emails.generate(sender, receiver, subject, body, attachement)
    emails.send(message)


if __name__ == "__main__":
    main()

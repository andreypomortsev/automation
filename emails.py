#!/usr/bin/env python3

"""
This module provides functions to generate an email with an attachment and send it via SMTP servers.

Functions:
- generate(sender, recipient, subject, body, attachment_path): Creates an email with an attachment.
- send(message): Sends the message to the configured SMTP server.

Author: Andrey Pomortsev
"""

import email.message
import mimetypes
import os.path
import smtplib


def generate(sender, recipient, subject, body, attachment_path):
    """Creates an email with an attachement."""
    message = email.message.EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    # Process the attachment and add it to the email
    attachment_filename = os.path.basename(attachment_path)
    mime_type, _ = mimetypes.guess_type(attachment_path)
    mime_type, mime_subtype = mime_type.split("/", 1)
    with open(attachment_path, "rb") as path:
        message.add_attachment(
            path.read(),
            maintype=mime_type,
            subtype=mime_subtype,
            filename=attachment_filename,
        )
    return message


def send(message):
    """Sends the message to the configured SMTP server."""
    mail_server = smtplib.SMTP("localhost")
    mail_server.send_message(message)
    mail_server.quit()

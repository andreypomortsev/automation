import os
import shutil
import socket
import psutil
from source import emails

BODY = "Please check your system and resolve the issue as soon as possible."
SENDER = "automation@example.com"
RECIPIENT = f"{os.environ.get('USER')}@example.com"


def check_cpu() -> str | None:
    """
    Check if the CPU usage is above 80%. If so, generate an email message with
    the subject "Error - CPU usage is over 80%" and the body text in the variable BODY,
    and send the message using the 'emails' module.

    :return: None
    """
    if psutil.cpu_percent(60) > 80:
        subject = "Error - CPU usage is over 80%"
        return subject
    return None


def check_ram() -> str | None:
    """
    Check if available memory is less than 500 MB. If so, generate an email message with
    the subject "Error - Available memory is less than 500MB" and the body text in the variable BODY
    and send the message using the 'emails' module.

    :return: None
    """
    available_memory = psutil.virtual_memory().available / (1024 * 1024)
    if available_memory < 500:
        subject = "Error - Available memory is less than 500MB"
        return subject
    return None


def check_disk() -> str | None:
    """
    Check if free disk space is less than 20%. If so, generate an email message
    with the subject "Error - Available disk space is less than 20%" and the body text
    in the variable BODY, and send the message using the 'emails' module.

    :return: None
    """
    disk_usage = shutil.disk_usage("/")
    if (disk_usage.free / disk_usage.total) * 100 < 20:
        subject = "Error - Available disk space is less than 20%"
        return subject
    return None


def check_network() -> str | None:
    """
    Check if the local host can access the internet. If not, generate an email message
    with the subject "Error - localhost cannot be resolved to 127.0.0.1" and the body text
    in the variable BODY, and send the message using the 'emails' module.
    """
    try:
        socket.gethostbyname("127.0.0.1")
        return None
    except socket.error:
        subject = "Error - localhost cannot be resolved to 127.0.0.1"
        return subject


def system_check() -> None:
    """Test the system resources and send an email if there is something wrong"""
    for func in (check_cpu, check_ram, check_network, check_disk):
        subject = func()
        if subject:
            message = emails.generate(SENDER, RECIPIENT, subject, BODY)
            emails.send(message=message)

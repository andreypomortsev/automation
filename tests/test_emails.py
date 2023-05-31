import unittest
from unittest import mock
import os
from source import emails


class TestEmails(unittest.TestCase):
    def setUp(self) -> None:
        self.sender = "example@example.com"
        self.recipient = "test@example.com"
        self.subject = "Test email"
        self.body = "Test email body"
        self.attachment_path = "test_attachment.txt"
        # Create the attachment file
        with open(self.attachment_path, "w") as f:
            f.write("test text")
        self.message = emails.generate(self.sender, self.recipient, self.subject, self.body, self.attachment_path)
    
    def tearDown(self) -> None:
        os.remove(self.attachment_path)
    
    def test_email_generate(self):
        """Test generate() in emails.py
        """
        # Assert that the generated message has the correct attributes
        self.assertEqual(self.message["From"], self.sender)
        self.assertEqual(self.message["To"], self.recipient)
        self.assertEqual(self.message["Subject"], self.subject)
        self.assertEqual(self.message.get_body(('plain',)).get_content().strip('\n'), self.body)

        attachment_filename = os.path.basename(self.attachment_path)
        attachment = self.message.get_payload()[1]
        self.assertEqual(attachment.get_filename(), attachment_filename)
        self.assertEqual(attachment.get_content_type(), "text/plain")
    
    @mock.patch('smtplib.SMTP')
    def test_emails_send_with_server(self, mock_smtp):
        emails.send(self.message, mock_smtp)
        mock_smtp.assert_not_called()
        mock_smtp.send_message.assert_called_once_with(self.message)
        mock_smtp.quit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
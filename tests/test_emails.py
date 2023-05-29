import unittest
import os
from source.emails import generate

class TestEmail(unittest.TestCase):
    def test_email_with_attachment(self):
        sender = "example@example.com"
        recipient = "test@example.com"
        subject = "Test email"
        body = "Test email body"
        attachment_path = "test_attachment.txt"

        # Create the attachment file
        with open(attachment_path, "w") as f:
            f.write("test attachment")

        message = generate(sender, recipient, subject, body, attachment_path)

        # Assert that the generated message has the correct attributes
        self.assertEqual(message["From"], sender)
        self.assertEqual(message["To"], recipient)
        self.assertEqual(message["Subject"], subject)
        self.assertEqual(message.get_body(('plain',)).get_content().strip('\n'), body)

        attachment_filename = os.path.basename(attachment_path)
        attachment = message.get_payload()[1]
        self.assertEqual(attachment.get_filename(), attachment_filename)
        self.assertEqual(attachment.get_content_type(), "text/plain")

        os.remove(attachment_path)

if __name__ == '__main__':
    unittest.main()
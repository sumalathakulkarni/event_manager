import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings.config import settings
import logging

class SMTPClient:
    def __init__(self, server: str, port: int, username: str, password: str):
        self.server = settings.smtp_server
        self.port = settings.smtp_port
        self.username = settings.smtp_username
        self.password = settings.smtp_password

    async def send_email(self, subject: str, html_content: str, recipient: str):
        try:
            # Create the email message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.username
            message['To'] = recipient
            message.attach(MIMEText(html_content, 'html'))

            # Send the email using aiosmtplib
            async with aiosmtplib.SMTP(hostname=self.server, port=self.port, use_tls=True) as client:
                await client.login(self.username, self.password)
                await client.send_message(message)

            logging.info(f"Email sent to {recipient}")
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
            raise

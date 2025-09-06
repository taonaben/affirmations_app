import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.recipient_email = os.getenv("RECIPIENT_EMAIL")

        if not all([self.sender_email, self.sender_password, self.recipient_email]):
            logger.warning(
                "Email configuration incomplete. Some environment variables are missing."
            )

    def create_affirmation_email(self, affirmation: str) -> MIMEMultipart:
        """Create a beautifully formatted email with the daily affirmation."""

        # Create message container
        msg = MIMEMultipart("alternative")
        msg["From"] = self.sender_email
        msg["To"] = self.recipient_email
        msg["Subject"] = (
            f"💕 Your Daily Affirmation - {datetime.now().strftime('%B %d, %Y')}"
        )

        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Daily Affirmation</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 40px; text-align: center; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px);">
                    
                    <!-- Header -->
                    <div style="margin-bottom: 30px;">
                        <h1 style="color: #333; font-size: 28px; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">
                            💕 Here when I can't be there
                        </h1>
                        <p style="color: #666; font-size: 16px; margin: 10px 0 0 0;">
                            {datetime.now().strftime('%A, %B %d, %Y')}
                        </p>
                    </div>
                    
                    <!-- Affirmation Card -->
                    <div style="background: linear-gradient(45deg, #ff6b6b, #ee5a24); border-radius: 15px; padding: 30px; margin: 20px 0; color: white; box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);">
                        <p style="font-size: 20px; line-height: 1.6; margin: 0; font-weight: 500; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
                            {affirmation}
                        </p>
                    </div>
                    
                    <!-- Footer -->
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                        <p style="color: #888; font-size: 14px; margin: 0;">
                            Made with ❤️ by your baby
                        </p>
                        <p style="color: #aaa; font-size: 12px; margin: 5px 0 0 0;">
                            This message was sent automatically at {datetime.now().strftime('%I:%M %p')}
                        </p>
                    </div>
                    
                </div>
            </div>
        </body>
        </html>
        """

        # Create plain text version
        text_content = f"""
        💕 Here when I can't be there 💕
        
        {datetime.now().strftime('%A, %B %d, %Y')}
        
        Your daily affirmation:
        {affirmation}
        
        Made with ❤️ by your baby
        Sent at {datetime.now().strftime('%I:%M %p')}
        """

        # Attach parts
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")

        msg.attach(part1)
        msg.attach(part2)

        return msg

    def send_affirmation_email(self, affirmation: str) -> bool:
        """Send the daily affirmation email."""

        if not all([self.sender_email, self.sender_password, self.recipient_email]):
            logger.error("Cannot send email: Missing email configuration")
            return False

        try:
            # Create email message
            msg = self.create_affirmation_email(affirmation)

            # Create secure connection
            context = ssl.create_default_context()

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)

                # Send email
                text = msg.as_string()
                server.sendmail(self.sender_email, self.recipient_email, text)

            logger.info(
                f"Daily affirmation email sent successfully to {self.recipient_email}"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    def test_email_connection(self) -> bool:
        """Test the email configuration and connection."""
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
            logger.info("Email connection test successful")
            return True
        except Exception as e:
            logger.error(f"Email connection test failed: {str(e)}")
            return False

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr
from config import Config

class EmailSender:
    """Enhanced email sending service with better error handling and validation"""
    
    def __init__(self):
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
    
    def send_email(self, to_emails, subject, body, attachments=None):
        """Send email with comprehensive error handling and validation"""
        if not Config.SENDER_EMAIL or not Config.APP_PASSWORD:
            raise ValueError("Email configuration is incomplete")
        
        if isinstance(to_emails, str):
            to_emails = [email.strip() for email in to_emails.split(',')]
        
        valid_emails = [email for email in to_emails if self._is_valid_email(email)]
        if not valid_emails:
            raise ValueError("No valid email addresses found")
        
        msg = MIMEMultipart()
        msg["From"] = formataddr(("ChatBot SMTP", Config.SENDER_EMAIL))
        msg["To"] = ", ".join(valid_emails)
        msg["Subject"] = subject or "No Subject"
        msg.attach(MIMEText(body or "", "plain", "utf-8"))
        
        if attachments:
            self._attach_files(msg, attachments)
        
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(Config.SENDER_EMAIL, Config.APP_PASSWORD)
                server.send_message(msg)
            return True
        except smtplib.SMTPException as e:
            raise Exception(f"Failed to send email: {str(e)}")
    
    def _is_valid_email(self, email):
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _attach_files(self, msg, attachments):
        for path in attachments:
            if not os.path.isfile(path):
                continue
            try:
                with open(path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'
                msg.attach(part)
            except IOError as e:
                print(f"Warning: Could not read file {path}: {e}")

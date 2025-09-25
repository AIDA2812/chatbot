import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Centralized configuration management with environment variables"""
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    APP_PASSWORD = os.getenv("APP_PASSWORD")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    # Future enhancement: Add email provider-specific configurations
    # Idea: Support multiple email providers with automatic configuration detection

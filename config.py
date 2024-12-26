import os

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'

    # SQLAlchemy Database URI: PostgreSQL connection string
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://flask_user:1441@localhost/task_manager'  # Replace with your actual database URL

    # Disable tracking modifications (this helps with performance)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Enable or disable SQLAlchemy's debugging (recommended to be false in production)
    SQLALCHEMY_ECHO = False

    # Enable or disable SQLAlchemy's SQL logging (recommended to be false in production)
    SQLALCHEMY_RECORD_QUERIES = False

    # Flask-Mail configuration for Gmail
    MAIL_SERVER = 'smtp.gmail.com'  # Ensure this is the correct SMTP server
    MAIL_PORT = 587  # Port for TLS
    MAIL_USE_TLS = True  # Enable TLS for security
    MAIL_USE_SSL = False  # Do not use SSL for Gmail
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'rutviksingh36@gmail.com'  # Example: rutviksingh36@gmail.com
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')# Example: rutvik1234
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'rutviksingh36@gmail.com'  # Example: rutviksingh36@gmail.com
    
    # New configuration to handle socket.gaierror
    MAIL_DEBUG = True  # Enable debug mode for Flask-Mail
    MAIL_SUPPRESS_SEND = False  # Suppress sending emails in debug mode
    
    # New configuration to handle authentication errors
    MAIL_USE_AUTH = True  # Ensure authentication is used

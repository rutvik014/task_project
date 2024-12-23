import os

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'

    # SQLAlchemy Database URI: PostgreSQL connection string
    # Ensure that the username and password are correct, along with the database name
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:your_password@localhost:5432/task_manager'

    # Disable tracking modifications (this helps with performance)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Enable or disable SQLAlchemy's debugging (recommended to be false in production)
    SQLALCHEMY_ECHO = False

    # Enable or disable SQLAlchemy's SQL logging (recommended to be false in production)
    SQLALCHEMY_RECORD_QUERIES = False

    # Enable or disable SQLAlchemy's SQL logging (recommended to be false in production)
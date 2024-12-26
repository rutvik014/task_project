import logging
from flask import Flask, app, redirect, render_template, request, url_for
from flask_migrate import Migrate
import os
from models import db, User, Task, Comment, Attachment, TaskCategory  # Ensure TaskCategory is imported
from models.task import Task as TaskModel  # Ensure consistent import
from routes import task_bp  # Import the task_bp Blueprint
from auth import auth_bp  # Import the auth_bp Blueprint
from flask_login import LoginManager, login_required, current_user  # Ensure flask_login and login_required are imported
from extensions import mail  # Import mail from extensions.py
from flask_mail import Message  # Import Message from flask_mail
from config import Config  # Import Config from config.py

def create_app():
    app = Flask(__name__)

    # Configurations
    app.config.from_object(Config)  # Load configurations from Config class

    mail.init_app(app)  # Initialize mail with the app
    db.init_app(app)  # Initialize the db object with the app
    migrate = Migrate(app, db)  # Initialize Flask-Migrate with the app and db
    login_manager = LoginManager(app)  # Initialize Flask-Login
    login_manager.login_view = 'auth_bp.login'  # Redirect to login page if not authenticated

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints (Make sure this comes after db initialization)
    app.register_blueprint(task_bp)
    app.register_blueprint(auth_bp)

    # Home route: Redirect to dashboard if authenticated, otherwise to login
    @app.route('/')
    def home():
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('auth_bp.login'))

    # Dashboard route: Display user dashboard
    @app.route('/dashboard')
    @login_required  # Ensure user is logged in to access this route
    def dashboard():
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('task_bp.dashboard'))

    # Admin dashboard route: Display all users and their tasks
    @app.route('/admin')
    @login_required
    def admin_dashboard():
        if current_user.role != 'admin':
            return redirect(url_for('dashboard'))
        users = User.query.all()
        return render_template('admin_dashboard.html', users=users)

    # Test email route: Send a test email
    @app.route('/send-test-email')
    def send_test_email():
        try:
            msg = Message('Test Email', 
                          sender=os.environ.get('MAIL_DEFAULT_SENDER') or app.config['MAIL_USERNAME'],  # Explicitly set the sender
                          recipients=['recipient@example.com'])
            msg.body = 'This is a test email sent from Flask.'
            mail.send(msg)
            return 'Email sent successfully!'
        except Exception as e:
            return f'Error sending email: {e}'

    return app

# Run the app

if __name__ == '__main__':
    app.run(debug=True)

# Note: Replace 'recipient@example.com' with the actual recipient's email address
from flask import Flask, redirect, render_template, request
from flask_migrate import Migrate
import os
from models import db, User, Task  # Import db, User, and Task from models/__init__.py
from routes import task_bp  # Import the task_bp Blueprint
from auth import auth_bp  # Import the auth_bp Blueprint
from flask_login import LoginManager, login_required  # Ensure flask_login and login_required are imported

# Initialize Flask app
app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://flask_user:1441@localhost/task_manager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your_secret_key_here'  # Add a secret key

# Initialize the db object with the app
db.init_app(app)

# Initialize Flask-Migrate with the app and db
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'auth_bp.login'  # Redirect to login page if not authenticated

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints (Make sure this comes after db initialization)
app.register_blueprint(task_bp)
app.register_blueprint(auth_bp)

# Home route: Display all tasks
@app.route('/')
@login_required  # Ensure user is logged in to access this route
def index():
    tasks = Task.query.all()  # Fetch all tasks from the database
    return render_template('index.html', tasks=tasks)  # Render index.html and pass tasks to it

# Run the app
if __name__ == '__main__':
    app.run(debug=True)  # Enable debugging
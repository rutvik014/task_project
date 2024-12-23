from flask import Flask, redirect, render_template, request, url_for
from flask_migrate import Migrate
import os
from models import db, User, Task  # Import db, User, and Task from models/__init__.py
from routes import task_bp  # Import the task_bp Blueprint
from auth import auth_bp  # Import the auth_bp Blueprint
from flask_login import LoginManager, login_required, current_user  # Ensure flask_login and login_required are imported

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
    user_tasks = Task.query.filter_by(assignee_id=current_user.id).all()  # Fetch tasks assigned to the current user
    return render_template('dashboard.html', tasks=user_tasks)  # Render dashboard.html and pass tasks to it

# Admin dashboard route: Display all users and their tasks
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)  # Enable debugging
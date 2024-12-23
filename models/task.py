from . import db  # Import the db object from models/__init__.py
from models.user import User

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    assignee = db.relationship('User', backref=db.backref('assigned_tasks', lazy=True))  # Use 'assigned_tasks' as the backref name
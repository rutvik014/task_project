from sqlalchemy import Column, Integer, String, Text
from models import db
from .user import User  # Import the User model

class Task(db.Model):
    __tablename__ = 'task'
    __mapper_args__ = {'polymorphic_identity': 'models.task.Task'}
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    assignee = db.relationship('User', back_populates='assigned_tasks')  # Use back_populates
    comments = db.relationship('models.comment.Comment', back_populates='task', lazy=True)
    attachments = db.relationship('models.attachment.Attachment', back_populates='task', lazy=True)


    def __repr__(self):
        return f'Task({self.name}, {self.priority}, {self.status})'

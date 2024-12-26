from sqlalchemy import Column, Integer, String, ForeignKey
from models import db
from .task import Task  # Import the Task model
from .user import User  # Import the User model

class Attachment(db.Model):
    __tablename__ = 'attachment'
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('task.id'), nullable=False)
    user = db.relationship('models.user.User', back_populates='user_attachments')
    task = db.relationship('models.task.Task', back_populates='attachments')
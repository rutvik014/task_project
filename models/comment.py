from sqlalchemy import Column, Integer, Text
from models import db
from .user import User  # Import the User model
from .task import Task  # Import the Task model

class Comment(db.Model):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = Column(Integer, db.ForeignKey('task.id'), nullable=False)
    user = db.relationship('models.user.User', back_populates='user_comments')
    task = db.relationship('models.task.Task', back_populates='comments')
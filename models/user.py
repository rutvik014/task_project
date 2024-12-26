from sqlalchemy import Column, Integer, String
from models import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    role = Column(String(50), nullable=False, default='user')
    assigned_tasks = db.relationship('Task', back_populates='assignee')  # Ensure back_populates matches Task model
    user_comments = db.relationship('models.comment.Comment', back_populates='user')
    user_attachments = db.relationship('models.attachment.Attachment', back_populates='user')

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.role})'
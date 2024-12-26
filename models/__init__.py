from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .task import Task
from .comment import Comment
from .attachment import Attachment
from .task_category import TaskCategory
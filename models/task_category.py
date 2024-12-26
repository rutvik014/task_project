from . import db

class TaskCategory(db.Model):
    __tablename__ = 'task_category'  # Explicitly set the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<TaskCategory {self.name}>'

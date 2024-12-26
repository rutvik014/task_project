from app import create_app
from models import db
from models.task import Task  # Ensure you import Task with a fully module-qualified path

app = create_app()

with app.app_context():
    result = db.engine.execute("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'user';
    """)

    for row in result:
        print(row)

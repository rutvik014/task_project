from flask import Flask, request, Response

def add_security_headers(response: Response) -> Response:
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

app = Flask(__name__)
app.after_request(add_security_headers)

# Import your routes and other configurations
from routes import task_bp
app.register_blueprint(task_bp)

if __name__ == '__main__':
    app.run(debug=True)
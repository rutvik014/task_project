from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from models.user import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('user', 'User')], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('You are already a user.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], validators=[DataRequired()])
    status = SelectField('Status', choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Save')
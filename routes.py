from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, Task, User, Comment, Attachment, TaskCategory
from forms import TaskForm, CommentForm, AttachmentForm
import os
from werkzeug.utils import secure_filename
from flask_mail import Message
from extensions import mail

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/tasks')
@login_required
def tasks():
    categories = TaskCategory.query.filter_by(user_id=current_user.id).all()
    tasks = Task.query.filter_by(assignee_id=current_user.id).all()
    return render_template('tasks.html', tasks=tasks, categories=categories)

@task_bp.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        print(form.data)  # Add this line to debug
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            status=form.status.data,
            priority=form.priority.data,
            assignee_id=form.assignee.data,
            category_id=form.category.data
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('task_bp.tasks'))
    return render_template('add_task.html', form=form)

@task_bp.route('/update_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.assignee_id != current_user.id:
        flash('You do not have permission to edit this task.', 'danger')
        return redirect(url_for('task_bp.tasks'))

    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.status = form.status.data
        task.due_date = form.due_date.data
        task.category_id = form.category.data
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('task_bp.tasks'))

    return render_template('update_task.html', form=form, task=task)

@task_bp.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.assignee_id != current_user.id:
        flash('You do not have permission to delete this task.', 'danger')
        return redirect(url_for('task_bp.tasks'))

    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('task_bp.tasks'))

@task_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash('You do not have permission to delete users.', 'danger')
        return redirect(url_for('task_bp.tasks'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('task_bp.tasks'))

@task_bp.route('/admin/view_tasks', methods=['GET'])
@login_required
def view_all_tasks():
    if current_user.role != 'admin':
        flash('You do not have permission to view all tasks.', 'danger')
        return redirect(url_for('task_bp.tasks'))

    tasks = Task.query.all()
    return render_template('view_all_tasks.html', tasks=tasks)

@task_bp.route('/add_comment/<int:task_id>', methods=['POST'])
@login_required
def add_comment(task_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            task_id=task_id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
        send_notification(task_id, 'New comment added', f'A new comment has been added to task: {task_id}')
    return redirect(url_for('task_bp.view_task', task_id=task_id))

@task_bp.route('/add_attachment/<int:task_id>', methods=['POST'])
@login_required
def add_attachment(task_id):
    form = AttachmentForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        attachment = Attachment(
            filename=filename,
            filepath=filepath,
            task_id=task_id,
            user_id=current_user.id
        )
        db.session.add(attachment)
        db.session.commit()
        flash('Attachment uploaded successfully!', 'success')
        send_notification(task_id, 'New attachment added', f'A new attachment has been added to task: {task_id}')
    return redirect(url_for('task_bp.view_task', task_id=task_id))

@task_bp.route('/view_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    comment_form = CommentForm()
    attachment_form = AttachmentForm()
    return render_template('view_task.html', task=task, comment_form=comment_form, attachment_form=attachment_form)

@task_bp.route('/send-email', methods=['POST'])
def send_email():
    email = request.form['email']
    subject = request.form['subject']
    body = request.form['body']

    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)

    flash('Email sent successfully!', 'success')
    return redirect(url_for('index'))

@task_bp.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(assignee_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)

def send_notification(to, subject, body):
    msg = Message(subject, recipients=[to])
    msg.body = body
    mail.send(msg)
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, Task, User
from forms import TaskForm

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            status=form.status.data,
            due_date=form.due_date.data,
            category=form.category.data,
            assignee_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('dashboard'))  # Redirect to the dashboard
    return render_template('add_task.html', form=form)

@task_bp.route('/update_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.assignee_id != current_user.id:
        flash('You do not have permission to edit this task.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.status = form.status.data
        task.due_date = form.due_date.data
        task.category = form.category.data
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('dashboard'))  # Redirect to the dashboard
    
    return render_template('update_task.html', form=form, task=task)

@task_bp.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.assignee_id != current_user.id:
        flash('You do not have permission to delete this task.', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('dashboard'))  # Redirect to the dashboard

@task_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash('You do not have permission to delete users.', 'danger')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@task_bp.route('/admin/view_tasks', methods=['GET'])
@login_required
def view_all_tasks():
    if current_user.role != 'admin':
        flash('You do not have permission to view all tasks.', 'danger')
        return redirect(url_for('dashboard'))
    
    tasks = Task.query.all()
    return render_template('view_all_tasks.html', tasks=tasks)
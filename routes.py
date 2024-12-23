from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db, Task
from forms import TaskForm

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/add_task', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            status=form.status.data,
            due_date=form.due_date.data
        )
        db.session.add(new_task)
        db.session.commit()
        
        flash('Task added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_task.html', form=form)

@task_bp.route('/update_task/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.status = form.status.data
        task.due_date = form.due_date.data
        db.session.commit()
        
        flash('Task updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('update_task.html', form=form, task=task)

@task_bp.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))
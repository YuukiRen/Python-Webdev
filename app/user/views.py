# app/home/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import user
from .forms import TaskForm
from .. import db
from ..models import Task


# Task Views
@user.route('/tasks', methods=['GET', 'POST'])
@login_required
def list_tasks():

    tasks = Task.query.all()
    curr_usr = current_user
    return render_template('user/tasks/tasks.html',
                           tasks=tasks, title="Tasks",
                           curr_usr=curr_usr)


@user.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():

    add_task = True
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data,
                    description=form.description.data,
                    user_id=current_user.id)
        try:
            db.session.add(task)
            db.session.commit()
            flash('You have successfully added a new task.')
        except:
            abort(401)
        return redirect(url_for('user.list_tasks'))

    return render_template('user/tasks/task.html', action="Add",
                           add_task=add_task, form=form,
                           title="Add Task")

@user.route('/tasks/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    add_task = False

    task = Task.query.get_or_404(id)
    form = TaskForm(obj=task)
    
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the task.')

        return redirect(url_for('user.list_tasks'))

    form.description.data = task.description
    form.title.data = task.title
    return render_template('user/tasks/task.html', action="Edit",
                           add_task=add_task, form=form,
                           task=task, title="Edit Task")


@user.route('/tasks/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):

    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('You have successfully deleted the task.')

    return redirect(url_for('user.list_tasks'))
    return render_template(title="Delete Task")


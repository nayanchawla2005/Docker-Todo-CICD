
from flask import Blueprint, render_template, request, redirect, url_for
from app.database import db
from app.models import Task

main = Blueprint("main", __name__)


@main.route("/")
def index():

    tasks = Task.query.order_by(Task.id.desc()).all()

    total = Task.query.count()
    completed = Task.query.filter_by(completed=True).count()

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed=completed
    )


@main.route("/add", methods=["POST"])
def add_task():

    title = request.form.get("title", "").strip()

    if title and len(title) <= 200:
        task = Task(title=title)
        db.session.add(task)
        db.session.commit()

    return redirect(url_for("main.index"))


@main.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):

    task = db.session.get(Task, task_id)

    if task:
        task.completed = not task.completed
        db.session.commit()

    return redirect(url_for("main.index"))


@main.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):

    task = db.session.get(Task, task_id)

    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for("main.index"))

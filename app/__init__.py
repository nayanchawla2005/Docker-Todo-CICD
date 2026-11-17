
import os
from flask import Flask
from app.database import db


def create_app(test_config=None):

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg://todo_user:todo_password@localhost:5432/todo_db"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from app.models import Task
    from app.routes import main

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

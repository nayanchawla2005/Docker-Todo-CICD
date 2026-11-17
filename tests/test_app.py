
import pytest

from app import create_app
from app.database import db


@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"TaskFlow" in response.data


def test_add_task(client):
    response = client.post(
        "/add",
        data={"title": "Learn Docker"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Learn Docker" in response.data


def test_complete_task(client):
    client.post("/add", data={"title": "Test task"})

    with client.application.app_context():
        from app.models import Task
        task = Task.query.first()
        task_id = task.id

    response = client.post(
        f"/toggle/{task_id}",
        follow_redirects=True
    )

    assert response.status_code == 200

    with client.application.app_context():
        from app.models import Task
        task = db.session.get(Task, task_id)
        assert task.completed is True


def test_delete_task(client):
    client.post("/add", data={"title": "Delete me"})

    with client.application.app_context():
        from app.models import Task
        task = Task.query.first()
        task_id = task.id

    response = client.post(
        f"/delete/{task_id}",
        follow_redirects=True
    )

    assert response.status_code == 200

    with client.application.app_context():
        from app.models import Task
        assert db.session.get(Task, task_id) is None

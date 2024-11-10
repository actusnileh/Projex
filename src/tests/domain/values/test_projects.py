from datetime import datetime

from domain.entities.projects import Task
from domain.values.projects import (
    Text,
    Title,
)


def test_create_task_success_short_text():
    title = Title("Projex")
    text = Text("Create a new project")

    task = Task(title=title, text=text)

    assert task.text == text
    assert task.title == title

    assert task.created_at.date() == datetime.today().date()

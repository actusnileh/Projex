from datetime import datetime

import pytest

from domain.entities.projects import (
    Project,
    Task,
)
from domain.events.projects import NewTaskReceivedEvent
from domain.exceptions.projects import TitleTooLongException
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


def test_create_task_success_long_text():
    title = Title("Projex")
    text = Text("Create a new project" * 500)

    task = Task(title=title, text=text)

    assert task.text == text
    assert task.title == title

    assert task.created_at.date() == datetime.today().date()


def test_create_task_with_long_title():
    with pytest.raises(TitleTooLongException):
        title = Title("Projex" * 400)
        text = Text("Create a new project" * 500)

        task = Task(title=title, text=text)

        assert task.text == text
        assert task.title == title

        assert task.created_at.date() == datetime.today().date()


def test_create_project_success():
    title = Title("Project 1")

    project = Project(title=title)

    assert project.title == title
    assert not project.tasks
    assert project.created_at.date() == datetime.today().date()


def test_new_task_event():
    title_task = Title("Create")
    text_task = Text("Create a new project")
    task = Task(title=title_task, text=text_task)

    title_project = Title("Project 1")
    project = Project(title=title_project)

    project.add_task(task)
    events = project.pull_events()

    pulled_events = project.pull_events()

    assert not pulled_events, pulled_events
    assert len(events) == 1, events

    new_event = events[0]

    assert isinstance(new_event, NewTaskReceivedEvent), new_event
    assert new_event.task_oid == task.oid
    assert new_event.task_text == task.text.as_generic_type()
    assert new_event.project_oid == project.oid

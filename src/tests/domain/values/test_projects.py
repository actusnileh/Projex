from datetime import datetime
from uuid import uuid4

import pytest

from domain.entities.projects import (
    Project,
    Task,
)
from domain.events.projects import NewTaskReceivedEvent
from domain.exceptions.projects import TitleTooLongException
from domain.values.enums.projects import (
    TaskPriority,
    TaskStatus,
)
from domain.values.projects import (
    Priority,
    Status,
    Text,
    Title,
)


def test_create_task_success_short_text():
    title = Title("Projex")
    text = Text("Create a new project")

    task = Task(title=title, text=text, project_oid=str(uuid4()))

    assert task.text == text
    assert task.title == title

    assert task.created_at.date() == datetime.today().date()


def test_create_task_success_long_text():
    title = Title("Projex")
    text = Text("Create a new project" * 500)

    task = Task(title=title, text=text, project_oid=str(uuid4()))

    assert task.text == text
    assert task.title == title

    assert task.created_at.date() == datetime.today().date()


def test_create_task_with_long_title():
    with pytest.raises(TitleTooLongException):
        title = Title("Projex" * 400)
        text = Text("Create a new project" * 500)

        task = Task(title=title, text=text, project_oid=str(uuid4()))

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
    task = Task(title=title_task, text=text_task, project_oid=str(uuid4()))

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


def test_new_task_event_with_status():
    title_task = Title("Create")
    text_task = Text("Create a new project")
    status_task = Status(TaskStatus.IN_PROGRESS)
    task = Task(
        title=title_task,
        text=text_task,
        project_oid=str(uuid4()),
        status=status_task,
    )

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
    assert new_event.status == status_task.as_generic_type()


def test_new_task_event_with_priority():
    title_task = Title("Create")
    text_task = Text("Create a new project")
    priority_task = Priority(TaskPriority.HIGH)
    task = Task(
        title=title_task,
        text=text_task,
        project_oid=str(uuid4()),
        priority=priority_task,
    )

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
    assert new_event.priority == priority_task.as_generic_type()

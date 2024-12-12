from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class NewTaskReceivedEvent(BaseEvent):
    task_title: str
    task_text: str
    task_oid: str
    project_oid: str
    status: str
    priority: str


@dataclass
class NewProjectCreated(BaseEvent):
    project_oid: str
    project_title: str


@dataclass
class TaskStatusChangedEvent(BaseEvent):
    task_oid: str
    old_status: str
    new_status: str


@dataclass
class TaskPriorityChangedEvent(BaseEvent):
    task_oid: str
    old_priority: str
    new_priority: str

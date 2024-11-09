from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class NewTaskReceivedEvent(BaseEvent):
    task_title: str
    task_text: str
    task_oid: str
    project_oid: str


@dataclass
class NewProjectCreated(BaseEvent):
    project_oid: str
    project_title: str

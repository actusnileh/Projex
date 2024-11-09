from dataclasses import (
    dataclass,
    field,
)

from domain.entities.base import BaseEntity
from domain.events.project import (
    NewProjectCreated,
    NewTaskReceivedEvent,
)
from domain.values.project import (
    Text,
    Title,
)


@dataclass(eq=False)
class Task(BaseEntity):
    title: Title
    text: Text


@dataclass(eq=False)
class Project(BaseEntity):
    title: Title
    tasks: set[Task] = field(
        default_factory=set,
        kw_only=True,
    )

    @classmethod
    def create_project(cls, title: Title) -> "Project":
        new_project = cls(title=title)
        new_project.register_event(
            NewProjectCreated(
                project_oid=new_project.oid,
                project_title=new_project.title.as_generic_type(),
            ),
        )

        return new_project

    def add_task(self, task: Task) -> None:
        self.tasks.add(task)
        task.register_event(
            NewTaskReceivedEvent(
                task_title=task.title.as_generic_type(),
                task_text=task.text.as_generic_type(),
                task_oid=task.oid,
                project_oid=self.oid,
            ),
        )

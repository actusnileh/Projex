from dataclasses import (
    dataclass,
    field,
)

from domain.entities.base import BaseEntity
from domain.events.projects import (
    NewProjectCreated,
    NewTaskReceivedEvent,
    TaskPriorityChangedEvent,
    TaskStatusChangedEvent,
)
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


@dataclass(eq=False)
class Task(BaseEntity):
    project_oid: str
    title: Title
    text: Text
    status: Status = Status(TaskStatus.NO_STATUS)
    priority: Priority = Priority(TaskPriority.NO_PRIORITY)

    @classmethod
    def update_status(self, new_status: Status) -> None:
        self.status = Status(new_status)
        self.register_event(
            TaskStatusChangedEvent(
                task_oid=self.oid,
                old_status=self.status.as_generic_type(),
                new_status=new_status.as_generic_type(),
            ),
        )

    @classmethod
    def update_priority(self, new_priority: Priority) -> None:
        self.priority = Priority(new_priority)
        self.register_event(
            TaskPriorityChangedEvent(
                task_oid=self.oid,
                old_priority=self.status.as_generic_type(),
                new_priority=new_priority.as_generic_type(),
            ),
        )


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
        self.register_event(
            NewTaskReceivedEvent(
                task_title=task.title.as_generic_type(),
                task_text=task.text.as_generic_type(),
                task_oid=task.oid,
                project_oid=self.oid,
                status=task.status.as_generic_type(),
                priority=task.priority.as_generic_type(),
            ),
        )

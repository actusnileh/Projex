from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from api.schemas import BaseQueryResponseSchema
from domain.entities.projects import (
    Project,
    Task,
)
from domain.values.enums.projects import (
    TaskPriority,
    TaskStatus,
)


class CreateProjectRequestSchema(BaseModel):
    title: str


class CreateProjectResponseSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, project: Project) -> "CreateProjectResponseSchema":
        return cls(
            oid=project.oid,
            title=project.title.as_generic_type(),
        )


class CreateTaskRequestSchema(BaseModel):
    title: str
    text: str
    priority: Optional[TaskPriority] = TaskPriority.NO_PRIORITY
    status: Optional[TaskStatus] = TaskStatus.NO_STATUS


class CreateTaskResponseSchema(BaseModel):
    oid: str
    title: str
    text: str
    priority: str
    status: str

    @classmethod
    def from_entity(cls, task: Task) -> "CreateTaskResponseSchema":
        return cls(
            oid=task.oid,
            title=task.title.as_generic_type(),
            text=task.text.as_generic_type(),
            priority=task.priority.as_generic_type(),
            status=task.status.as_generic_type(),
        )


class TaskDetailSchema(BaseModel):
    oid: str
    title: str
    text: str
    priority: str
    status: str
    created_at: datetime

    @classmethod
    def from_entity(cls, task: Task) -> "TaskDetailSchema":
        return cls(
            oid=task.oid,
            title=task.title.as_generic_type(),
            text=task.text.as_generic_type(),
            priority=task.priority.value,
            status=task.status.value,
            created_at=task.created_at,
        )


class ProjectDetailSchema(BaseModel):
    oid: str
    title: str
    created_at: datetime

    @classmethod
    def from_entity(cls, project: Project) -> "ProjectDetailSchema":
        return cls(
            oid=project.oid,
            title=project.title.as_generic_type(),
            created_at=project.created_at,
        )


class GetTasksQueryResponseSchema(BaseQueryResponseSchema):
    items: list[TaskDetailSchema]

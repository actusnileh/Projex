from pydantic import BaseModel

from domain.entities.projects import (
    Project,
    Task,
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


class CreateTaskResponseSchema(BaseModel):
    oid: str
    title: str
    text: str

    @classmethod
    def from_entity(cls, task: Task) -> "CreateTaskResponseSchema":
        return cls(
            oid=task.oid,
            title=task.title.as_generic_type(),
            text=task.text.as_generic_type(),
        )

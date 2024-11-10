from domain.entities.projects import Project
from pydantic import BaseModel


class CreateProjectRequestSchema(BaseModel):
    title: str


class CreateProjectResponseSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, project: Project) -> "CreateProjectResponseSchema":
        return CreateProjectResponseSchema(
            oid=project.oid,
            title=project.title.as_generic_type(),
        )

from dataclasses import (
    dataclass,
    field,
)

from domain.entities.projects import Project
from infrastructure.repositories.projects.base import BaseProjectsRepository


@dataclass
class MemoryProjectsRepository(BaseProjectsRepository):
    _saved_projects: list[Project] = field(
        default_factory=list,
        kw_only=True,
    )

    async def get_project_by_oid(self, project_oid: str) -> Project | None:
        try:
            return (
                next(
                    project
                    for project in self._saved_projects
                    if project.oid == project_oid
                ),
            )

        except StopIteration:
            return False

    async def check_project_exists_by_title(self, title: str) -> bool:
        try:
            return bool(
                next(
                    project
                    for project in self._saved_projects
                    if project.title.as_generic_type() == title
                ),
            )
        except StopIteration:
            return False

    async def add_project(self, project: Project) -> None:
        self._saved_projects.append(project)

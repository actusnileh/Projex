from dataclasses import dataclass
from typing import Generic

from domain.entities.projects import Project
from infrastructure.repositories.projects.base import (
    BaseProjectsRepository,
    BaseTasksRepository,
)
from logic.exceptions.projects import ProjectNotFoundException
from logic.queries.base import (
    BaseQuery,
    BaseQueryHandler,
    QR,
    QT,
)


@dataclass(frozen=True)
class GetProjectDetailQuery(BaseQuery):
    project_oid: str


@dataclass(frozen=True)
class GetProjectDetailQueryHandler(BaseQueryHandler, Generic[QR, QT]):
    projects_repository: BaseProjectsRepository
    tasks_repository: BaseTasksRepository  # TODO: Забирать задачи отдельно

    async def handle(self, query: GetProjectDetailQuery) -> Project:
        project = await self.projects_repository.get_project_by_oid(
            project_oid=query.project_oid,
        )

        if not project:
            raise ProjectNotFoundException(project_oid=query.project_oid)

        return project

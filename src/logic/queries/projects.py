from dataclasses import dataclass
from typing import Iterable

from domain.entities.projects import (
    Project,
    Task,
)
from infrastructure.repositories.filters.projects import GetTasksInfraFilters
from infrastructure.repositories.projects.base import (
    BaseProjectsRepository,
    BaseTasksRepository,
)
from logic.exceptions.projects import ProjectNotFoundException
from logic.queries.base import (
    BaseQuery,
    BaseQueryHandler,
)


@dataclass(frozen=True)
class GetProjectDetailQuery(BaseQuery):
    project_oid: str


@dataclass(frozen=True)
class GetTasksQuery(BaseQuery):
    project_oid: str
    filters: GetTasksInfraFilters


@dataclass(frozen=True)
class GetProjectDetailQueryHandler(BaseQueryHandler):
    projects_repository: BaseProjectsRepository
    tasks_repository: BaseTasksRepository

    async def handle(self, query: GetProjectDetailQuery) -> Project:
        project = await self.projects_repository.get_project_by_oid(
            project_oid=query.project_oid,
        )

        if not project:
            raise ProjectNotFoundException(project_oid=query.project_oid)

        return project


@dataclass(frozen=True)
class GetTasksQueryHandler(BaseQueryHandler):
    tasks_repository: BaseTasksRepository

    async def handle(self, query: GetTasksQuery) -> Iterable[Task]:
        return await self.tasks_repository.get_tasks(
            project_oid=query.project_oid,
            filters=query.filters,
        )

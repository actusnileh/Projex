from dataclasses import dataclass
from typing import Optional

from domain.entities.projects import (
    Project,
    Task,
)
from domain.values.projects import (
    Priority,
    Status,
    Text,
    Title,
)
from infrastructure.repositories.projects.base import (
    BaseProjectsRepository,
    BaseTasksRepository,
)
from logic.commands.base import (
    BaseCommand,
    CommandHandler,
)
from logic.exceptions.projects import (
    ProjectNotFoundException,
    ProjectWithThatTitleExistsException,
)


@dataclass(frozen=True)
class CreateProjectCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateProjectCommandHandler(CommandHandler[CreateProjectCommand, Project]):
    projects_repository: BaseProjectsRepository

    async def handle(self, command: CreateProjectCommand) -> Project:
        if await self.projects_repository.check_project_exists_by_title(command.title):
            raise ProjectWithThatTitleExistsException(command.title)

        title = Title(value=command.title)

        new_project = Project.create_project(title=title)
        # TODO: считать ивенты
        await self.projects_repository.add_project(new_project)

        return new_project


@dataclass(frozen=True)
class CreateTaskCommand(BaseCommand):
    title: str
    text: str
    project_oid: str
    priority: Optional[str]
    status: Optional[str]


@dataclass(frozen=True)
class CreateTaskCommandHandler(CommandHandler[CreateTaskCommand, Task]):
    projects_repository: BaseProjectsRepository
    tasks_repository: BaseTasksRepository

    async def handle(self, command: CreateTaskCommand) -> Task:
        project = await self.projects_repository.get_project_by_oid(
            project_oid=command.project_oid,
        )

        if not project:
            raise ProjectNotFoundException(project_oid=command.project_oid)

        new_task = Task(
            title=Title(value=command.title),
            text=Text(value=command.text),
            priority=Priority(value=command.priority),
            status=Status(value=command.status),
            project_oid=command.project_oid,
        )

        project.add_task(task=new_task)
        await self.tasks_repository.add_task(
            task=new_task,
        )

        return new_task

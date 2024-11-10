from dataclasses import dataclass

from domain.entities.projects import Project
from domain.values.projects import Title
from infrastructure.repositories.projects.base import BaseProjectRepository
from logic.commands.base import (
    BaseCommand,
    CommandHandler,
)
from logic.exceptions.projects import ProjectWithThatTitleExistsException


@dataclass(frozen=True)
class CreateProjectCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateProjectCommandHandler(CommandHandler[CreateProjectCommand, Project]):
    project_repository: BaseProjectRepository

    async def handle(self, command: CreateProjectCommand) -> Project:
        if await self.project_repository.check_project_exists_by_title(command.title):
            raise ProjectWithThatTitleExistsException(command.title)

        title = Title(value=command.title)

        new_project = Project.create_project(title=title)
        # TODO: считать ивенты
        await self.project_repository.add_project(new_project)

        return new_project

from dataclasses import dataclass

from domain.entities.projects import Project
from domain.values.projects import Title
from infra.repositories.projects.base import BaseProjectRepository
from logic.commands.base import (
    BaseCommand,
    CommandHandler,
)
from logic.exceptions.project import ProjectWithThatTitleAlreadyExistsException


@dataclass(frozen=True)
class CreateProjectCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateProjectCommandHandler(CommandHandler[CreateProjectCommand, Project]):
    project_repository: BaseProjectRepository

    async def handle(self, command: CreateProjectCommand) -> Project:
        if await self.project_repository.check_project_exists_by_title(command.title):
            raise ProjectWithThatTitleAlreadyExistsException(command.title)

        title = Title(value=command.title)

        new_project = Project.create_project(title=title)

        await self.project_repository.add_project(new_project)

        return new_project

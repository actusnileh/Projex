import pytest
from domain.entities.projects import Project
from infrastructure.repositories.projects import BaseProjectRepository
from logic.commands.projects import CreateProjectCommand
from logic.mediator import Mediator


@pytest.mark.asyncio
async def test_create_project_command_success(
    project_repository: BaseProjectRepository,
    mediator: Mediator,
):
    # TODO: Сделать фейкер для генерации случайных текстов
    project: Project = (
        await mediator.handle_command(CreateProjectCommand(title="Project 1"))
    )[0]

    assert project_repository.check_project_exists_by_title(
        title=project.title.as_generic_type(),
    )

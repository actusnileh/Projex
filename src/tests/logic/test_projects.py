import pytest
from domain.entities.projects import Project
from faker import Faker
from infrastructure.repositories.projects import BaseProjectRepository
from logic.commands.projects import CreateProjectCommand
from logic.mediator import Mediator


@pytest.mark.asyncio
async def test_create_project_command_success(
    project_repository: BaseProjectRepository,
    mediator: Mediator,
):
    faker = Faker()
    random_title = faker.text(max_nb_chars=20)

    project: Project = (
        await mediator.handle_command(CreateProjectCommand(title=random_title))
    )[0]

    assert project_repository.check_project_exists_by_title(
        title=project.title.as_generic_type(),
    )

import pytest
from domain.entities.projects import Project
from domain.values.projects import Title
from faker import Faker
from infrastructure.repositories.projects import BaseProjectRepository
from logic.commands.projects import CreateProjectCommand
from logic.exceptions.projects import ProjectWithThatTitleExistsException
from logic.mediator import Mediator


@pytest.mark.asyncio
async def test_create_project_command_success(
    project_repository: BaseProjectRepository,
    mediator: Mediator,
    faker: Faker,
):
    project: Project
    project, *_ = await mediator.handle_command(
        CreateProjectCommand(title=faker.text(max_nb_chars=40)),
    )

    assert await project_repository.check_project_exists_by_title(
        title=project.title.as_generic_type(),
    )


@pytest.mark.asyncio
async def test_create_project_command_title_already_exists(
    project_repository: BaseProjectRepository,
    mediator: Mediator,
    faker: Faker,
):
    title_text = faker.text(max_nb_chars=40)

    project = Project(title=Title(title_text))

    await project_repository.add_project(project)

    assert project in project_repository._saved_projects

    with pytest.raises(ProjectWithThatTitleExistsException):
        await mediator.handle_command(CreateProjectCommand(title=title_text))

    assert len(project_repository._saved_projects) == 1

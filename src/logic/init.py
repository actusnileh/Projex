from infrastructure.repositories.projects import BaseProjectRepository
from logic.commands.projects import (
    CreateProjectCommand,
    CreateProjectCommandHandler,
)
from logic.mediator import Mediator


def init_mediator(
    mediator: Mediator,
    project_repository: BaseProjectRepository,
):
    mediator.register_command(
        CreateProjectCommand,
        [CreateProjectCommandHandler(project_repository=project_repository)],
    )

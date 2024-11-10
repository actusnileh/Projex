from infrastructure.repositories.projects import (
    BaseProjectRepository,
    MemoryProjectRepository,
)
from logic.init import init_mediator
from logic.mediator import Mediator
from pytest import fixture


@fixture(scope="package")
def project_repository() -> MemoryProjectRepository:
    return MemoryProjectRepository()


@fixture(scope="package")
def mediator(project_repository: BaseProjectRepository) -> Mediator:
    mediator = Mediator()
    init_mediator(
        mediator=mediator,
        project_repository=project_repository,
    )
    return mediator

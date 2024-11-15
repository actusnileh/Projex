from punq import Container
from pytest import fixture

from infrastructure.repositories.projects.base import BaseProjectsRepository
from logic.mediator import Mediator
from tests.fixtures import init_dummy_container


@fixture(scope="function")
def container() -> Container:
    return init_dummy_container()


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@fixture()
def project_repository(container: Container) -> BaseProjectsRepository:
    return container.resolve(BaseProjectsRepository)

from punq import (
    Container,
    Scope,
)

from infrastructure.repositories.projects.base import BaseProjectsRepository
from infrastructure.repositories.projects.memory import MemoryProjectsRepository
from logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(
        BaseProjectsRepository,
        MemoryProjectsRepository,
        scope=Scope.singleton,
    )

    return container

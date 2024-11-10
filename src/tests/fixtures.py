from punq import (
    Container,
    Scope,
)

from infrastructure.repositories.projects.base import BaseProjectRepository
from infrastructure.repositories.projects.memory import MemoryProjectRepository
from logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(
        BaseProjectRepository,
        MemoryProjectRepository,
        scope=Scope.singleton,
    )

    return container

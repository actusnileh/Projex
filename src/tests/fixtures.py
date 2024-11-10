from infrastructure.repositories.projects import (
    BaseProjectRepository,
    MemoryProjectRepository,
)
from logic.init import _init_container
from punq import (
    Container,
    Scope,
)


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(
        BaseProjectRepository,
        MemoryProjectRepository,
        scope=Scope.singleton,
    )

    return container

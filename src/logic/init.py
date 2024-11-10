from functools import lru_cache

from infrastructure.repositories.projects import (
    BaseProjectRepository,
    MemoryProjectRepository,
)
from logic.commands.projects import (
    CreateProjectCommand,
    CreateProjectCommandHandler,
)
from logic.mediator import Mediator
from punq import (
    Container,
    Scope,
)


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(
        BaseProjectRepository,
        MemoryProjectRepository,
        scope=Scope.singleton,
    )
    container.register(CreateProjectCommandHandler)

    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            CreateProjectCommand,
            [container.resolve(CreateProjectCommandHandler)],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container

from functools import lru_cache

from punq import Container
from src.infrastructure.repositories.projects import (
    BaseProjectRepository,
    MemoryProjectRepository,
)
from src.logic.commands.projects import (
    CreateProjectCommand,
    CreateProjectCommandHandler,
)
from src.logic.mediator import Mediator


@lru_cache(1)
def init_container() -> Container:
    container = Container()
    container.register(BaseProjectRepository, MemoryProjectRepository)
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

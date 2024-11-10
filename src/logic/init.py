from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from infrastructure.repositories.projects.base import BaseProjectRepository
from infrastructure.repositories.projects.mongo import MongoDBProjectRepository
from logic.commands.projects import (
    CreateProjectCommand,
    CreateProjectCommandHandler,
)
from logic.mediator import Mediator
from settings import Settings


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, instance=Settings(), scope=Scope.singleton)
    container.register(CreateProjectCommandHandler)

    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            CreateProjectCommand,
            [container.resolve(CreateProjectCommandHandler)],
        )

        return mediator

    def init_project_mongodb_repository():
        settings: Settings = container.resolve(Settings)
        client = AsyncIOMotorClient(settings.MONGO_URI, serverSelectionTimeoutMS=3000)

        return MongoDBProjectRepository(
            mongo_db_client=client,
            mongo_db_db_name=settings.MONGO_PROJECT_DATABASE,
            mongo_db_collection_name=settings.MONGO_PROJECT_COLLECTION,
        )

    container.register(
        BaseProjectRepository,
        factory=init_project_mongodb_repository,
        scope=Scope.singleton,
    )
    container.register(Mediator, factory=init_mediator)

    return container

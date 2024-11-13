from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from infrastructure.repositories.projects.base import (
    BaseProjectsRepository,
    BaseTasksRepository,
)
from infrastructure.repositories.projects.mongo import (
    MongoDBProjectsRepository,
    MongoDBPTasksRepository,
)
from logic.commands.projects import (
    CreateProjectCommand,
    CreateProjectCommandHandler,
    CreateTaskCommand,
    CreateTaskCommandHandler,
)
from logic.mediator import Mediator
from logic.queries.projects import (
    GetProjectDetailQuery,
    GetProjectDetailQueryHandler,
    GetTasksQuery,
    GetTasksQueryHandler,
)
from settings import Settings


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, instance=Settings(), scope=Scope.singleton)

    settings: Settings = container.resolve(Settings)

    def create_mongo_db_client():
        return AsyncIOMotorClient(settings.MONGO_URI, serverSelectionTimeoutMS=3000)

    container.register(
        AsyncIOMotorClient,
        factory=create_mongo_db_client,
        scope=Scope.singleton,
    )
    client = container.resolve(AsyncIOMotorClient)

    def init_projects_mongodb_repository() -> BaseProjectsRepository:
        return MongoDBProjectsRepository(
            mongo_db_client=client,
            mongo_db_db_name=settings.MONGO_PROJECT_DATABASE,
            mongo_db_collection_name=settings.MONGO_PROJECT_COLLECTION,
        )

    def init_tasks_mongodb_repository() -> BaseTasksRepository:
        return MongoDBPTasksRepository(
            mongo_db_client=client,
            mongo_db_db_name=settings.MONGO_PROJECT_DATABASE,
            mongo_db_collection_name=settings.MONGO_TASK_COLLECTION,
        )

    container.register(
        BaseProjectsRepository,
        factory=init_projects_mongodb_repository,
        scope=Scope.singleton,
    )
    container.register(
        BaseTasksRepository,
        factory=init_tasks_mongodb_repository,
        scope=Scope.singleton,
    )

    # Commands Handlers
    container.register(CreateProjectCommandHandler)
    container.register(CreateTaskCommandHandler)

    # Query Handlers
    container.register(GetProjectDetailQueryHandler)
    container.register(GetTasksQueryHandler)

    # Mediator
    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            command=CreateProjectCommand,
            command_handlers=[container.resolve(CreateProjectCommandHandler)],
        )
        mediator.register_command(
            command=CreateTaskCommand,
            command_handlers=[container.resolve(CreateTaskCommandHandler)],
        )

        mediator.register_query(
            query=GetProjectDetailQuery,
            query_handler=container.resolve(GetProjectDetailQueryHandler),
        )
        mediator.register_query(
            query=GetTasksQuery,
            query_handler=container.resolve(GetTasksQueryHandler),
        )
        return mediator

    container.register(Mediator, factory=init_mediator)

    return container

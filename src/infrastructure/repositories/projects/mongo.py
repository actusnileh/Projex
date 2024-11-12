from abc import ABC
from dataclasses import dataclass

from motor.core import AgnosticClient

from domain.entities.projects import (
    Project,
    Task,
)
from infrastructure.repositories.projects.base import (
    BaseProjectsRepository,
    BaseTasksRepository,
)
from infrastructure.repositories.projects.converters import (
    convert_project_document_to_entity,
    convert_project_to_document,
    convert_task_to_document,
)


@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][
            self.mongo_db_collection_name
        ]


@dataclass
class MongoDBProjectsRepository(BaseProjectsRepository, BaseMongoDBRepository):
    async def check_project_exists_by_title(self, title: str) -> bool:
        return bool(await self._collection.find_one(filter={"title": title}))

    async def get_project_by_oid(self, project_oid: str) -> Project | None:
        project_document = await self._collection.find_one(filter={"oid": project_oid})

        if not project_document:
            return None

        return convert_project_document_to_entity(project_document)

    async def add_project(self, project: Project) -> None:
        await self._collection.insert_one(convert_project_to_document(project))


@dataclass
class MongoDBPTasksRepository(BaseTasksRepository, BaseMongoDBRepository):
    async def add_task(self, project_oid: str, task: Task) -> None:
        await self._collection.update_one(
            filter={"oid": project_oid},
            update={
                "$push": {
                    "tasks": convert_task_to_document(task),
                },
            },
        )

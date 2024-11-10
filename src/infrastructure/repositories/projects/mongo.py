from dataclasses import dataclass

from motor.core import AgnosticClient

from domain.entities.projects import Project
from infrastructure.repositories.projects.base import BaseProjectRepository
from infrastructure.repositories.projects.converters import convert_project_to_document


@dataclass
class MongoDBProjectRepository(BaseProjectRepository):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    def _get_project_collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][
            self.mongo_db_collection_name
        ]

    async def check_project_exists_by_title(self, title: str) -> bool:
        collection = self._get_project_collection()
        return bool(await collection.find_one(filter={"title": title}))

    async def add_project(self, project: Project) -> None:
        collection = self._get_project_collection()
        await collection.insert_one(convert_project_to_document(project))

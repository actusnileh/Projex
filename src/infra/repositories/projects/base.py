from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.entities.project import Project


@dataclass
class BaseProjectRepository(ABC):
    @abstractmethod
    async def check_project_exists_by_title(self, title: str) -> bool: ...

    @abstractmethod
    async def add_project(self, project: Project) -> None: ...

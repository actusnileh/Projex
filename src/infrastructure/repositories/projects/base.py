from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.entities.projects import (
    Project,
    Task,
)


@dataclass
class BaseProjectsRepository(ABC):
    @abstractmethod
    async def check_project_exists_by_title(self, title: str) -> bool: ...

    @abstractmethod
    async def get_project_by_oid(self, project_oid: str) -> Project | None: ...

    @abstractmethod
    async def add_project(self, project: Project) -> None: ...


@dataclass
class BaseTasksRepository(ABC):
    @abstractmethod
    async def add_task(self, task: Task) -> None: ...

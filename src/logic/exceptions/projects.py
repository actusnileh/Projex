from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class ProjectWithThatTitleExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f"Проект с названием '{self.title}' уже существует."


@dataclass(eq=False)
class ProjectNotFoundException(LogicException):
    project_oid: str

    @property
    def message(self):
        return f"Проект с таким {self.project_oid=} не найден."

from dataclasses import dataclass

from src.logic.exceptions.base import LogicException


@dataclass(eq=False)
class ProjectWithThatTitleExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f"Проект с названием '{self.title}' уже существует."

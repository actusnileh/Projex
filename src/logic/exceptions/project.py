from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class ProjectWithThatTitleAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f"Проект с названием '{self.title}' уже существует."

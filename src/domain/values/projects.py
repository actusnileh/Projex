from dataclasses import dataclass

from domain.exceptions.projects import (
    EmptyTextException,
    TitleTooLongException,
)
from domain.values.base import BaseValueObject
from domain.values.enums.projects import (
    TaskPriority,
    TaskStatus,
)


@dataclass(frozen=True)
class Text(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Title(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 150:
            raise TitleTooLongException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Status(BaseValueObject):
    value: TaskStatus

    def validate(self):
        pass

    def as_generic_type(self) -> str:
        return self.value.value


@dataclass(frozen=True)
class Priority(BaseValueObject):
    value: TaskPriority

    def validate(self):
        pass

    def as_generic_type(self) -> str:
        return self.value.value

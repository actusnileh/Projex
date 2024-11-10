from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class EventHandlerNotRegisteredException(LogicException):
    event_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики события: {self.event_type}."


@dataclass(frozen=True, eq=False)
class CommandHandlerNotRegisteredException(LogicException):
    command_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики команды: {self.command_type}."

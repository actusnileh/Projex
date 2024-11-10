from dataclasses import dataclass

from src.logic.exceptions.base import LogicException


@dataclass(eq=False)
class EventHandlerNotRegisteredException(LogicException):
    event_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики события: {self.event_type}."


@dataclass(eq=False)
class CommandHandlerNotRegisteredException(LogicException):
    command_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики команды: {self.command_type}."

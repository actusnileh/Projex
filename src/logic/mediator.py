from collections import defaultdict
from dataclasses import (
    dataclass,
    field,
)
from typing import Iterable

from src.domain.events.base import BaseEvent
from src.logic.commands.base import (
    BaseCommand,
    CommandHandler,
    CR,
    CT,
)
from src.logic.events.base import (
    ER,
    ET,
    EventHandler,
)
from src.logic.exceptions.mediator import (
    CommandHandlerNotRegisteredException,
    EventHandlerNotRegisteredException,
)


@dataclass(eq=False)
class Mediator:
    events_map: dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    commands_map: dict[CT, CommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]):
        self.events_map[event].append(event_handlers)

    def register_command(
        self,
        command: CT,
        command_handlers: Iterable[CommandHandler[CT, CR]],
    ):
        self.commands_map[command].extend(command_handlers)

    async def handle_event(self, event: BaseEvent) -> Iterable[ER]:
        event_type = event.__class__
        handlers = self.events_map.get(event_type)

        if not handlers:
            raise EventHandlerNotRegisteredException(event_type)

        return [await handler.handle(event) for handler in handlers]

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.events_map.get(command_type)

        if not handlers:
            raise CommandHandlerNotRegisteredException(command_type)

        return [await handler.handle(command) for handler in handlers]

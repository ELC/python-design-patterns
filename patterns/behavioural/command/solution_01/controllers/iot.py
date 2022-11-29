from dataclasses import dataclass, field

from ..command import Command

from typing import Generic, TypeVar


T = TypeVar("T", covariant=True)


@dataclass
class IoTController(Generic[T]):
    _history: list[Command[T]] = field(default_factory=list)
    _command_queue: list[Command[T]] = field(default_factory=list)

    def add_command(self, command: Command[T]):
        self._command_queue.append(command)

    def execute(self):
        if not self._command_queue:
            raise ValueError("No commands are in queue")

        for command in self._command_queue:
            self._history.append(command)
            command.execute()
        self._command_queue = []

    def undo_last_command(self):
        last_command = self._history.pop()
        last_command.undo()
        
    def undo_all_commands(self):
        for undo_command in reversed(self._history):
            undo_command.undo()

from dataclasses import dataclass

from typing import Optional, TypeVar, Generic

from ..command import Command


T = TypeVar("T", covariant=True)

@dataclass
class RemoteController(Generic[T]):
    command: Optional[Command[T]] = None

    def add_command(self, command: Command[T]):
        self.command = command

    def execute(self):
        if self.command is None:
            raise ValueError("No Commands Set")

        self.command.execute()

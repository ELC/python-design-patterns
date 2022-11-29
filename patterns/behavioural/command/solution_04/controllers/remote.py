from dataclasses import dataclass

from typing import Optional

from ..command import Command


@dataclass
class RemoteController:
    command: Optional[Command] = None

    def add_command(self, command: Command):
        self.command = command

    def execute(self):
        if self.command is None:
            raise ValueError("No Commands Set")

        self.command()

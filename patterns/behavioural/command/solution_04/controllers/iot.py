from dataclasses import dataclass, field

from ..command import Command, UndoCommand


@dataclass
class IoTController:
    _history: list[Command] = field(default_factory=list)
    _command_queue: list[Command] = field(default_factory=list)
    _undo_queue: list[UndoCommand] = field(default_factory=list)

    def add_command(self, command: Command):
        self._command_queue.append(command)

    def execute(self):
        if not self._command_queue:
            raise ValueError("No commands are in queue")

        for command in self._command_queue:
            self._history.append(command)
            undo_command = command()
            self._undo_queue.append(undo_command)
        self._command_queue = []

    def undo_last_command(self):
        last_undo_command = self._undo_queue.pop()
        last_undo_command()
        
    def undo_all_commands(self):
        for undo_command in reversed(self._undo_queue):
            undo_command()
